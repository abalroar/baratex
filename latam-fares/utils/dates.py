"""Utilitários de datas para filtros e intervalos."""

from __future__ import annotations

WEEKDAY_NAMES_PT = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]


def month_range(start_month: int, start_year: int, n_months: int) -> list[tuple[int, int]]:
    """Retorna lista de (month, year) para n_months meses a partir de start."""
    if n_months < 1:
        return []

    items: list[tuple[int, int]] = []
    month = start_month
    year = start_year

    for _ in range(n_months):
        items.append((month, year))
        month += 1
        if month > 12:
            month = 1
            year += 1

    return items


def weekday_name_to_int(name: str) -> int:
    """'segunda' → 0, 'terça' → 1, ..., 'domingo' → 6."""
    normalized = name.strip().lower()
    mapping = {
        "segunda": 0,
        "segunda-feira": 0,
        "terça": 1,
        "terca": 1,
        "terça-feira": 1,
        "terca-feira": 1,
        "quarta": 2,
        "quarta-feira": 2,
        "quinta": 3,
        "quinta-feira": 3,
        "sexta": 4,
        "sexta-feira": 4,
        "sábado": 5,
        "sabado": 5,
        "domingo": 6,
    }

    if normalized not in mapping:
        raise ValueError(f"Dia da semana inválido: {name}")

    return mapping[normalized]
