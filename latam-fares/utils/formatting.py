"""Formatações de exibição para UI."""

from __future__ import annotations

from datetime import date, datetime


def _pt_br_number(value: float) -> str:
    base = f"{value:,.2f}"
    return base.replace(",", "X").replace(".", ",").replace("X", ".")


def fmt_brl(value: float) -> str:
    """R$ 1.670,34 — padrão brasileiro obrigatório em todos os displays."""
    return f"R$ {_pt_br_number(value)}"


def fmt_date_br(d: date) -> str:
    """03/05/2026 (dom)."""
    if isinstance(d, datetime):
        parsed = d.date()
    else:
        parsed = d
    weekdays = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]
    return f"{parsed.strftime('%d/%m/%Y')} ({weekdays[parsed.weekday()]})"


def fmt_percentile(p: float) -> str:
    """0.03 → 'top 3%'."""
    return f"top {round(p * 100):.0f}%"
