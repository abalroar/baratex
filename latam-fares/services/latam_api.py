"""Camada HTTP e parsing do calendário da LATAM."""

from __future__ import annotations

from urllib.parse import urlencode

import pandas as pd
import requests

# ─── CONFIGURAÇÃO DA CAMADA HTTP ─────────────────────────────────────
# Altere aqui se precisar customizar sem tocar no resto do código

BASE_URL = "https://www.latamairlines.com/bff/web-products-searchbox/v1/calendar"

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Accept-Language": "pt-BR,pt;q=0.9",
    "Referer": "https://www.latamairlines.com/",
}

# Para passar cookies de sessão quando necessário:
# DEFAULT_COOKIES = {"session_id": "...", "token": "..."}
DEFAULT_COOKIES: dict = {}
# ─────────────────────────────────────────────────────────────────────


def build_url(origin: str, destination: str, month: int, year: int) -> str:
    """Monta a URL completa com parâmetros."""
    params = {
        "origin": origin,
        "destination": destination,
        "month": month,
        "year": year,
        "isRoundTrip": "true",
        "extended": "true",
    }
    return f"{BASE_URL}?{urlencode(params)}"


def fetch_calendar(
    origin: str,
    destination: str,
    month: int,
    year: int,
    headers: dict | None = None,
    cookies: dict | None = None,
    timeout: int = 15,
) -> dict:
    """Faz o GET e retorna o JSON bruto. Lança exceção em caso de erro."""
    params = {
        "origin": origin,
        "destination": destination,
        "month": month,
        "year": year,
        "isRoundTrip": "true",
        "extended": "true",
    }
    request_headers = {**DEFAULT_HEADERS, **(headers or {})}
    request_cookies = {**DEFAULT_COOKIES, **(cookies or {})}

    try:
        response = requests.get(
            BASE_URL,
            params=params,
            headers=request_headers,
            cookies=request_cookies,
            timeout=timeout,
        )
    except requests.Timeout as exc:
        raise TimeoutError(
            f"Timeout ao consultar LATAM para {origin}-{destination} {month:02d}/{year}"
        ) from exc

    response.raise_for_status()

    try:
        return response.json()
    except ValueError as exc:
        raise ValueError("Resposta não é JSON válido") from exc


def _extract_direction_payload(raw: dict, direction: str) -> dict:
    if isinstance(raw, dict) and raw.get("direction") == direction:
        return raw

    data_key_candidates = ["data", "calendars", "results"]
    for key in data_key_candidates:
        candidate = raw.get(key)
        if isinstance(candidate, list):
            for item in candidate:
                if isinstance(item, dict) and item.get("direction") == direction:
                    return item

    if isinstance(raw, list):
        for item in raw:
            if isinstance(item, dict) and item.get("direction") == direction:
                return item

    raise KeyError(f"Direction '{direction}' não encontrada no payload: {raw}")


def parse_calendar(raw: dict, direction: str) -> pd.DataFrame:
    """
    Extrai detailsCalendar para um DataFrame normalizado.
    direction: "OUTBOUND" ou "INBOUND"
    Colunas resultantes: date, price, currency, formatted_amount,
                         percentile, enabled, low_price, origin, destination
    """
    payload = _extract_direction_payload(raw, direction)

    if "detailsCalendar" not in payload:
        raise KeyError(f"'detailsCalendar' ausente no payload: {payload}")

    details = payload["detailsCalendar"]
    if not details:
        return pd.DataFrame(
            columns=[
                "date",
                "price",
                "currency",
                "formatted_amount",
                "percentile",
                "enabled",
                "low_price",
                "origin",
                "destination",
            ]
        )

    rows = []
    for item in details:
        fare = item.get("fare", {})
        rows.append(
            {
                "date": pd.to_datetime(item.get("date")).date(),
                "price": float(fare.get("amount", 0.0)),
                "currency": fare.get("currency"),
                "formatted_amount": item.get("formattedAmount"),
                "percentile": item.get("percentile"),
                "enabled": bool(item.get("enabled", False)),
                "low_price": bool(item.get("lowPrice", False)),
                "origin": payload.get("origin"),
                "destination": payload.get("destination"),
            }
        )

    return pd.DataFrame(rows)


def fetch_month_prices(
    origin: str,
    destination: str,
    month: int,
    year: int,
    direction: str,
    headers: dict | None = None,
    cookies: dict | None = None,
) -> pd.DataFrame:
    """Orquestra fetch + parse para um mês e direção. Retorna apenas enabled=True."""
    raw = fetch_calendar(
        origin=origin,
        destination=destination,
        month=month,
        year=year,
        headers=headers,
        cookies=cookies,
    )
    df = parse_calendar(raw=raw, direction=direction)
    if df.empty:
        return df
    return df[df["enabled"]].reset_index(drop=True)
