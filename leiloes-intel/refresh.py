"""Atualização INCREMENTAL AUTOMÁTICA do dataset do dashboard (cacarecos.streamlit.app).

Uma linha de comando faz tudo, derivando os inputs do estado da rodada anterior
(run_meta.json / banco) — não é preciso lembrar datas nem flags:

  1. Listagens AO VIVO (--no-cache): lances frescos + lotes novos em aberto.
  2. Finalizados INCREMENTAIS: varre o histórico das 800+ casas, mas só os leilões
     POSTERIORES à última atualização (cutoff automático = dias desde o último
     scrape de finalizados + margem de segurança). Idempotente: pula o que já está
     no banco.
  3. enrich -> metrics -> report: reprocessa e regenera lots.parquet + CSVs.
     Os sinais BUY_NOW/WATCH/AVOID passam a refletir SÓ os leilões atuais.
  4. Grava run_meta.json (data, cutoff usado, contagens, sinais, tempo por etapa):
     é a memória lida pelo dashboard e pela próxima execução automática.

Uso:
  python refresh.py                    # incremental automático (o caso normal / cron)
  python refresh.py --full-history     # varre TODO o histórico (primeira vez / rebuild)
  python refresh.py --skip-listings    # só finalizados + reprocess
  python refresh.py --no-finalizados   # só listagens ao vivo + reprocess
  python refresh.py --margin-days 7    # folga do cutoff (padrão 5)
  python refresh.py --workers 24
"""
import argparse
import json
import sys
import time
from datetime import datetime

import config


def _load_meta() -> dict:
    path = config.EXPORTS_DIR / "run_meta.json"
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            return {}
    return {}


def _last_finalizado_date():
    """Data do último scrape de finalizados: preferir run_meta, cair p/ o banco."""
    meta = _load_meta()
    stamp = meta.get("last_finalizado_scrape")
    if not stamp:
        import db
        row = db.connect().execute(
            "SELECT MAX(scraped_at) FROM lot_snapshots WHERE status='finalizado'").fetchone()
        stamp = row[0] if row else None
    if not stamp:
        return None
    try:
        return datetime.strptime(stamp[:10], "%Y-%m-%d").date()
    except ValueError:
        return None


def _run(module_name: str, argv: list[str]):
    """Roda o main() de um módulo com argv, como um subcomando (igual run_all.py)."""
    mod = __import__(module_name)
    old = sys.argv
    sys.argv = [module_name] + argv
    try:
        mod.main()
    finally:
        sys.argv = old


def main():
    ap = argparse.ArgumentParser(description="Atualização incremental do dashboard")
    ap.add_argument("--full-history", action="store_true",
                    help="varre todo o histórico de finalizados (ignora o cutoff)")
    ap.add_argument("--skip-listings", action="store_true", help="não coleta listagens ao vivo")
    ap.add_argument("--no-finalizados", action="store_true", help="não coleta finalizados")
    ap.add_argument("--margin-days", type=int, default=5,
                    help="folga somada ao cutoff p/ não perder leilões na borda")
    ap.add_argument("--workers", type=int, default=config.MAX_WORKERS)
    args = ap.parse_args()

    timings: dict[str, float] = {}
    today = datetime.now().date()

    # cutoff automático dos finalizados (dias desde a última atualização + margem)
    cutoff_days = None
    if not args.full_history:
        last = _last_finalizado_date()
        if last:
            cutoff_days = (today - last).days + args.margin_days
        else:
            print("[info] sem atualização anterior — varrendo histórico completo.")

    print(f"== refresh @ {today} | cutoff finalizados: "
          f"{'COMPLETO' if cutoff_days is None else f'{cutoff_days} dias'} ==")

    # 1. listagens ao vivo (lances frescos + lotes novos)
    if not args.skip_listings:
        print("\n== 1/4 listagens ao vivo (--no-cache) ==")
        t = time.time()
        _run("scrape_listings", ["--no-cache"])
        timings["listings_s"] = round(time.time() - t)

    # 2. finalizados incrementais (histórico das casas desde a última atualização)
    if not args.no_finalizados:
        print("\n== 2/4 finalizados incrementais (histórico das casas) ==")
        t = time.time()
        hist_argv = ["--workers", str(args.workers)]
        if cutoff_days is not None:
            hist_argv += ["--days", str(cutoff_days)]
        _run("scrape_historico", hist_argv)
        timings["finalizados_s"] = round(time.time() - t)

    # 3. reprocessamento offline
    import enrich
    import metrics
    import report

    print("\n== 3/4 enrich -> metrics ==")
    t = time.time()
    enrich.enrich_all()
    metrics.compute()
    timings["reprocess_s"] = round(time.time() - t)

    print("\n== 4/4 exportação + run_meta ==")
    t = time.time()
    report.export_and_meta = getattr(report, "export_and_meta", None)  # compat
    conn = report.db.connect()
    house_m, cat_m, opp, avoid = report.export_csvs(conn)
    report.write_report(conn, house_m, cat_m, opp, avoid)
    (config.EXPORTS_DIR / "data_dictionary.md").write_text(report.DATA_DICT, encoding="utf-8")
    meta = report.write_run_meta(conn, extra={
        "last_run": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "finalizados_cutoff_days": cutoff_days,
        "mode": "full-history" if args.full_history else "incremental",
        "stage_seconds": timings,
    })
    timings["export_s"] = round(time.time() - t)
    meta["stage_seconds"] = timings
    (config.EXPORTS_DIR / "run_meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    print("\n== resumo ==")
    print(f"  lotes: {meta.get('lots_total')} | ao vivo agora: {meta.get('live_now')} "
          f"| finalizados: {meta.get('finalizado_lots')}")
    print(f"  sinais: {meta.get('signals')}")
    print(f"  tempos (s): {timings}")


if __name__ == "__main__":
    main()
