"""LATAM Fare Discovery (V1)."""

from __future__ import annotations

from datetime import datetime

import pandas as pd
import requests
import streamlit as st

from services.combinator import combine_trips
from services.latam_api import fetch_month_prices
from utils.dates import WEEKDAY_NAMES_PT, month_range, weekday_name_to_int
from utils.formatting import fmt_brl, fmt_date_br


@st.cache_data(ttl=3600)
def cached_fetch_month_prices(origin, destination, month, year, direction):
    return fetch_month_prices(origin, destination, month, year, direction)


def _weekday_names_to_int(values: list[str]) -> list[int]:
    return [weekday_name_to_int(v) for v in values]


def _format_table(df: pd.DataFrame) -> pd.DataFrame:
    formatted = df.copy()
    formatted["departure_date"] = formatted["departure_date"].apply(fmt_date_br)
    formatted["return_date"] = formatted["return_date"].apply(fmt_date_br)
    formatted["departure_price"] = formatted["departure_price"].apply(fmt_brl)
    formatted["return_price"] = formatted["return_price"].apply(fmt_brl)
    formatted["total_price"] = formatted["total_price"].apply(fmt_brl)
    formatted["departure_low_price"] = formatted["departure_low_price"].map(lambda x: "✅" if x else "—")
    formatted["return_low_price"] = formatted["return_low_price"].map(lambda x: "✅" if x else "—")
    return formatted


st.set_page_config(page_title="LATAM Fare Discovery", layout="wide")

st.title("LATAM Fare Discovery")
st.caption("Encontre combinações vantajosas de ida e volta com base no calendário da LATAM.")

current = datetime.now()

st.sidebar.header("Configuração da busca")
outbound_origin = st.sidebar.text_input("Origem da ida", value="GRU").strip().upper()
outbound_destination = st.sidebar.text_input("Destino da ida", value="JFK").strip().upper()
inbound_origin = st.sidebar.text_input("Origem da volta", value="JFK").strip().upper()
inbound_destination = st.sidebar.text_input("Destino da volta", value="GRU").strip().upper()
start_month = st.sidebar.selectbox("Mês inicial", list(range(1, 13)), index=current.month - 1)
start_year = st.sidebar.number_input("Ano inicial", min_value=2024, value=current.year, step=1)
months_count = st.sidebar.slider("Quantidade de meses", min_value=1, max_value=6, value=2)

st.sidebar.header("Regras de combinação")
min_days = st.sidebar.number_input("Dias mínimos de viagem", min_value=1, value=3, step=1)
max_days = st.sidebar.number_input("Dias máximos de viagem", min_value=1, value=14, step=1)
outbound_days = st.sidebar.multiselect("Dias da semana — ida", WEEKDAY_NAMES_PT, default=WEEKDAY_NAMES_PT)
inbound_days = st.sidebar.multiselect("Dias da semana — volta", WEEKDAY_NAMES_PT, default=WEEKDAY_NAMES_PT)
top_n = st.sidebar.slider("Top N combinações", min_value=5, max_value=100, value=20)

sort_option = st.selectbox(
    "Ordenar por",
    ["Menor preço total", "Melhor score", "Menor preço de ida", "Menor preço de volta"],
)

if st.button("Buscar combinações"):
    months = month_range(start_month=int(start_month), start_year=int(start_year), n_months=months_count)
    outbound_frames = []
    inbound_frames = []

    try:
        with st.spinner("Buscando preços da LATAM..."):
            for month, year in months:
                outbound_frames.append(
                    cached_fetch_month_prices(
                        outbound_origin,
                        outbound_destination,
                        month,
                        year,
                        "OUTBOUND",
                    )
                )
                inbound_frames.append(
                    cached_fetch_month_prices(
                        inbound_origin,
                        inbound_destination,
                        month,
                        year,
                        "INBOUND",
                    )
                )
    except requests.HTTPError as e:
        st.error(f"Erro ao consultar LATAM: {e}")
        st.stop()
    except KeyError:
        st.error("Resposta inesperada da API. Veja dados brutos para debug.")
        st.stop()
    except Exception as e:
        st.error(f"Erro ao consultar LATAM: {e}")
        st.stop()

    outbound_df = pd.concat(outbound_frames, ignore_index=True) if outbound_frames else pd.DataFrame()
    inbound_df = pd.concat(inbound_frames, ignore_index=True) if inbound_frames else pd.DataFrame()

    combined = combine_trips(
        outbound_df=outbound_df,
        inbound_df=inbound_df,
        min_days=int(min_days),
        max_days=int(max_days),
        outbound_weekdays=_weekday_names_to_int(outbound_days) if outbound_days else None,
        inbound_weekdays=_weekday_names_to_int(inbound_days) if inbound_days else None,
        top_n=int(top_n),
    )

    if sort_option == "Melhor score":
        combined = combined.sort_values("score", ascending=True)
    elif sort_option == "Menor preço de ida":
        combined = combined.sort_values("departure_price", ascending=True)
    elif sort_option == "Menor preço de volta":
        combined = combined.sort_values("return_price", ascending=True)
    else:
        combined = combined.sort_values("total_price", ascending=True)

    if combined.empty:
        st.warning("Nenhuma combinação válida encontrada com os filtros aplicados.")
    else:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Menor preço total", fmt_brl(float(combined["total_price"].min())))
        col2.metric("Melhor ida isolada", fmt_brl(float(outbound_df["price"].min())) if not outbound_df.empty else "N/D")
        col3.metric("Melhor volta isolada", fmt_brl(float(inbound_df["price"].min())) if not inbound_df.empty else "N/D")
        col4.metric("N combinações", f"{len(combined)}")

        st.dataframe(_format_table(combined), use_container_width=True)

    with st.expander("Dados brutos de ida"):
        st.dataframe(outbound_df, use_container_width=True)
    with st.expander("Dados brutos de volta"):
        st.dataframe(inbound_df, use_container_width=True)
