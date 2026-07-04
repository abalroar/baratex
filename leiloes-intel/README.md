# leiloes-intel — Inteligência de mercado da LeilõesBR

Pipeline de scraping ético + análise para decidir entre dois modelos de negócio
em arte/antiguidades/mobiliário modernista:

- **Modelo A** — casa de leilão / curadoria própria.
- **Modelo B** — garimpo + revenda curada (Instagram drops).

Coleta **preço de martelo real** de leilões finalizados (não proxy), lances ao
vivo por categoria, classifica designers/peças por regras determinísticas e
calcula margem, liquidez e sinais de compra **BUY_NOW / WATCH / AVOID**.

## Ética (regras duras)
- Só páginas públicas, sem login. Não burla CAPTCHA, rate limit ou bloqueio.
- 403 de uma casa = aquela casa é pulada (respeitada), não contornada.
- Rate limit global de 1,5s + cache em disco; user-agent identificável.
- Sem dados pessoais de arrematantes. Sem download de imagens (só URLs).
- Categorias sensíveis (armas, marfim, etc.) são marcadas e excluídas das métricas.

## Como rodar
```bash
pip install -r requirements.txt
python run_all.py                 # pipeline completo
python run_all.py --skip-scrape   # só re-processa dados já coletados
```

### Atualização incremental automática (o jeito recomendado)
`refresh.py` faz tudo derivando os inputs do estado da rodada anterior — não é
preciso lembrar datas nem flags. Ele lê `data/exports/run_meta.json` (a "memória"
da pipeline), calcula sozinho o **cutoff dos finalizados** (só leilões posteriores
à última atualização), coleta listagens ao vivo + finalizados incrementais das
800+ casas, reprocessa e regenera `lots.parquet` + `run_meta.json`.
```bash
python refresh.py                 # incremental automático (uso normal / cron)
python refresh.py --full-history  # varre TODO o histórico (primeira vez / rebuild)
python refresh.py --skip-listings # só finalizados + reprocess
python refresh.py --no-finalizados# só listagens ao vivo + reprocess
```
`run_meta.json` guarda data da última atualização, cutoff usado, contagens
(lotes, ao vivo agora, finalizados), distribuição de sinais e tempo por etapa —
e o dashboard mostra esse carimbo no topo. Como o SQLite de ~920MB não vai para
o git, o `refresh.py` deve rodar onde o banco persiste (este ambiente / seu Mac);
depois basta commitar `data/exports/` para o Streamlit Cloud redeployar.

**"Ao vivo agora" ≠ "andamento":** os sinais BUY_NOW/WATCH/AVOID cobrem só os
leilões **atualmente em aberto** (último snapshot do lote = andamento *e* visto na
coleta mais recente). Lotes de rodadas antigas cujo pregão já passou não entram
nos sinais, mesmo que ainda não tenham sido recapturados como finalizados. A
coluna `is_live_now` no parquet marca esse conjunto.

## Dashboard (deep dive)
```bash
streamlit run app.py
```
Lê os CSVs versionados em `data/exports/` (não exige re-scrape nem o SQLite).
Abas: Tendências (GMV/sell-through diário), Categorias (liquidez × ticket),
Casas (sourcing × benchmark), Designers (martelo real por venda), Preços &
competição, Oportunidades (BUY_NOW/WATCH/AVOID com link por lote) e Explorador
com download do recorte filtrado. Filtros globais por status, tipo, designer,
UF, casa, preço e busca textual.
Ou por fase:
```bash
python scrape_listings.py         # lances ao vivo por categoria
python scrape_finalizados.py      # martelo real dos finalizados (~15 dias)
python enrich.py                  # classificação semântica
python metrics.py                 # custos, margem, sinais
python report.py                  # CSVs + relatório
python validate.py                # auditoria
```

## Como funciona a coleta (descoberto por recon)
- Listagens ao vivo: `busca_andamento.asp?tp=|<HEX>|` (categoria em hex latin-1),
  paginado com `v=126`. Dá título, lance atual, nº de lances, data, UF.
- Finalizados: lista em `.../12hor/leiloes_passados.asp`; lotes de cada leilão em
  `<casa>/templates/catalogo/asp/catalogocontentload.asp?leilao=<id>&status=9` —
  JSON com `VALOR_VENDA` (martelo), `VALOR_CONTRATADO` (inicial), `QTDLANCE`,
  `MOSTRABTN_STATUS` (vendido/não vendido). Uma requisição = um leilão inteiro.

## Saídas (`data/exports/`)
`auctions.csv`, `lots.csv`, `auction_house_metrics.csv`, `category_metrics.csv`,
`opportunity_lots.csv`, `avoid_lots.csv`, `market_intelligence_report.md`,
`data_dictionary.md`. Store canônico: `data/leiloes.sqlite`.

Premissas econômicas e thresholds de sinal ficam em `assumptions.yaml` (o
relatório imprime as premissas usadas). Toda inferência guarda `matched_keywords`
e `matched_snippet` para auditoria.
```
```
