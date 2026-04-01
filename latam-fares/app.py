"""LATAM Fare Discovery (V1)."""

from __future__ import annotations

from datetime import datetime

import pandas as pd
import requests
import streamlit as st

from services.combinator import combine_trips
from services.latam_api import fetch_month_prices, parse_cookie_string, parse_headers_string
from utils.dates import WEEKDAY_NAMES_PT, month_range, weekday_name_to_int
from utils.formatting import fmt_brl, fmt_date_br, fmt_percentile


@st.cache_data(ttl=3600)
def cached_fetch_month_prices(
    origin,
    destination,
    month,
    year,
    direction,
    timeout_sec,
    cookie_items,
    header_items,
):
    cookies = dict(cookie_items)
    headers = dict(header_items)
    return fetch_month_prices(
        origin,
        destination,
        month,
        year,
        direction,
        timeout=timeout_sec,
        cookies=cookies,
        headers=headers,
    )


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
st.markdown(
    """
    <style>
    .stApp { background: #0e0f11; color: #e4e6ea; }
    section[data-testid="stSidebar"] { background: #141619; border-right: 1px solid #32363d; }
    .stMetric { background: #141619; border: 1px solid #32363d; border-radius: 12px; padding: 12px; }
    .stButton>button { background: #3ec9d6; color: #0e0f11; border: none; border-radius: 10px; font-weight: 600; }
    .stButton>button:hover { background: #2ab5c2; color: #0e0f11; }
    .stSelectbox [data-baseweb="select"] > div { background: #1a1d21; border-color: #32363d; }
    .stTextInput input, .stNumberInput input { background: #1a1d21 !important; color: #e4e6ea !important; }
    .stMultiSelect [data-baseweb="tag"] { background: #1a3035; color: #3ec9d6; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("LATAM Fare Discovery")
st.caption("Encontre combinações vantajosas de ida e volta com base no calendário da LATAM.")

current = datetime.now()

st.sidebar.header("Configuração da busca")
outbound_origin = st.sidebar.text_input("Origem da ida", value="GRU").strip().upper()
outbound_destination = st.sidebar.text_input("Destino da ida", value="JFK").strip().upper()
inbound_origin = st.sidebar.text_input("Origem da volta", value="JFK").strip().upper()
inbound_destination = st.sidebar.text_input("Destino da volta", value="GRU").strip().upper()
if st.sidebar.button("Trocar ida/volta"):
    outbound_origin, inbound_origin = inbound_origin, outbound_origin
    outbound_destination, inbound_destination = inbound_destination, outbound_destination
start_month = st.sidebar.selectbox("Mês inicial", list(range(1, 13)), index=current.month - 1)
start_year = st.sidebar.number_input("Ano inicial", min_value=2024, value=current.year, step=1)
months_count = st.sidebar.slider("Quantidade de meses", min_value=1, max_value=6, value=2)

st.sidebar.header("Regras de combinação")
min_days = st.sidebar.number_input("Dias mínimos de viagem", min_value=1, value=3, step=1)
max_days = st.sidebar.number_input("Dias máximos de viagem", min_value=1, value=14, step=1)
outbound_days = st.sidebar.multiselect("Dias da semana — ida", WEEKDAY_NAMES_PT, default=WEEKDAY_NAMES_PT)
inbound_days = st.sidebar.multiselect("Dias da semana — volta", WEEKDAY_NAMES_PT, default=WEEKDAY_NAMES_PT)
top_n = st.sidebar.slider("Top N combinações", min_value=5, max_value=100, value=20)
timeout_sec = st.sidebar.slider("Timeout por consulta (s)", min_value=10, max_value=60, value=25)
cookie_input = st.sidebar.text_area(
    "Cookies (opcional)",
    value="",
    help="Cole o header Cookie completo do cURL/browser quando a LATAM exigir sessão.",
    height=110,
)
headers_input = st.sidebar.text_area(
    "Headers extras (opcional)",
    value="",
    help="Um header por linha. Ex.: x-foo: bar",
    height=110,
)

try:
    cookies_dict = parse_cookie_string(cookie_input)
except Exception:
    st.sidebar.error("Cookie inválido. Use formato: chave1=valor1; chave2=valor2")
    cookies_dict = {}
try:
    headers_dict = parse_headers_string(headers_input)
except Exception:
    st.sidebar.error("Headers inválidos. Use formato: Header-Name: valor")
    headers_dict = {}
if cookie_input.strip() and cookies_dict:
    st.sidebar.caption(f"Cookies parseados: {len(cookies_dict)}")
if headers_input.strip() and headers_dict:
    st.sidebar.caption(f"Headers parseados: {len(headers_dict)}")
st.sidebar.caption("Use somente cookies da sua própria sessão; proteções do provedor não são contornadas pelo app.")

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
                        timeout_sec,
                        tuple(sorted(cookies_dict.items())),
                        tuple(sorted(headers_dict.items())),
                    )
                )
                inbound_frames.append(
                    cached_fetch_month_prices(
                        inbound_origin,
                        inbound_destination,
                        month,
                        year,
                        "INBOUND",
                        timeout_sec,
                        tuple(sorted(cookies_dict.items())),
                        tuple(sorted(headers_dict.items())),
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
    with st.expander("Como o ranking é calculado"):
        st.markdown(
            "- **Score**: `total_price * (1 + avg_percentile) * 0.95` quando ambas as pernas são low price.\n"
            "- Percentis exibidos como referência de posição no mês."
        )
        if not combined.empty:
            preview = combined.copy()
            preview["departure_percentile"] = preview["departure_percentile"].apply(fmt_percentile)
            preview["return_percentile"] = preview["return_percentile"].apply(fmt_percentile)
            st.dataframe(
                preview[
                    [
                        "departure_date",
                        "return_date",
                        "departure_percentile",
                        "return_percentile",
                        "score",
                    ]
                ],
                use_container_width=True,
            )
