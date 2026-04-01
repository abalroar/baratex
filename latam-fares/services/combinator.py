"""Combinação e ranking de trechos de ida e volta."""

from __future__ import annotations

import pandas as pd


def combine_trips(
    outbound_df: pd.DataFrame,
    inbound_df: pd.DataFrame,
    min_days: int,
    max_days: int,
    outbound_weekdays: list[int] | None = None,
    inbound_weekdays: list[int] | None = None,
    top_n: int = 50,
) -> pd.DataFrame:
    """
    Combina datas de ida e volta seguindo as regras:
    - data_volta > data_ida
    - (data_volta - data_ida).days entre min_days e max_days
    - filtros de dia da semana quando fornecidos
    Retorna as top_n combinações ordenadas por total_price.
    """
    if outbound_df.empty or inbound_df.empty:
        return pd.DataFrame(
            columns=[
                "departure_date",
                "return_date",
                "departure_price",
                "return_price",
                "trip_length_days",
                "total_price",
                "departure_low_price",
                "return_low_price",
                "departure_percentile",
                "return_percentile",
                "score",
            ]
        )

    out = outbound_df.copy()
    inn = inbound_df.copy()

    out["date"] = pd.to_datetime(out["date"])
    inn["date"] = pd.to_datetime(inn["date"])

    if outbound_weekdays is not None:
        out = out[out["date"].dt.weekday.isin(outbound_weekdays)]
    if inbound_weekdays is not None:
        inn = inn[inn["date"].dt.weekday.isin(inbound_weekdays)]

    combinations = out.assign(key=1).merge(inn.assign(key=1), on="key", suffixes=("_out", "_in")).drop(
        columns=["key"]
    )

    combinations["trip_length_days"] = (combinations["date_in"] - combinations["date_out"]).dt.days
    combinations = combinations[
        (combinations["trip_length_days"] >= min_days)
        & (combinations["trip_length_days"] <= max_days)
        & (combinations["date_in"] > combinations["date_out"])
    ]

    if combinations.empty:
        return pd.DataFrame(
            columns=[
                "departure_date",
                "return_date",
                "departure_price",
                "return_price",
                "trip_length_days",
                "total_price",
                "departure_low_price",
                "return_low_price",
                "departure_percentile",
                "return_percentile",
                "score",
            ]
        )

    combinations["total_price"] = combinations["price_out"] + combinations["price_in"]
    combinations["avg_percentile"] = (combinations["percentile_out"] + combinations["percentile_in"]) / 2
    combinations["both_low_price"] = combinations["low_price_out"] & combinations["low_price_in"]

    # Score: menor é melhor
    # Combina preço total com percentis médios
    # low_price em ambas as pernas dá desconto de 5%
    combinations["score"] = combinations["total_price"] * (1 + combinations["avg_percentile"]) * (
        0.95 * combinations["both_low_price"].astype(int) + 1.0 * (~combinations["both_low_price"]).astype(int)
    )

    result = combinations[
        [
            "date_out",
            "date_in",
            "price_out",
            "price_in",
            "trip_length_days",
            "total_price",
            "low_price_out",
            "low_price_in",
            "percentile_out",
            "percentile_in",
            "score",
        ]
    ].rename(
        columns={
            "date_out": "departure_date",
            "date_in": "return_date",
            "price_out": "departure_price",
            "price_in": "return_price",
            "low_price_out": "departure_low_price",
            "low_price_in": "return_low_price",
            "percentile_out": "departure_percentile",
            "percentile_in": "return_percentile",
        }
    )

    return result.sort_values("total_price", ascending=True).head(top_n).reset_index(drop=True)
