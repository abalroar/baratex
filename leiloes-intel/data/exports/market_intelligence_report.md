# Relatório de Inteligência de Mercado — LeilõesBR

_Gerado em 04/07/2026 03:49. Coleta de páginas públicas, sem login, com rate limit._

## 1. Resumo executivo

- **Lotes coletados:** 1.217.712 (12.835 ao vivo, 1.691.394 finalizados)
- **Casas/leiloeiros mapeados:** 845
- **Lotes vendidos com martelo observado:** 910.576 → **sell-through global 53,8%**
- **Janela de finalizados observada:** 14/01/2015 a 02/07/2026 (4188 dias).
- **Fonte de preço:** martelo REAL de leilões finalizados, não proxy. Lances ao vivo da busca por categoria.

> **Observed vs inferred.** Martelo, lance, nº de lances e status de venda são _observados_ no site. Tipo de peça, designer, força de atribuição, custos de frete/restauro, valor de revenda estimado, margem e sinais são _inferidos_ por regras determinísticas (ver `data_dictionary.md`).

## 2. Top categorias por sell-through (≥30 lotes finalizados)

| item_type | ofertados | vendidos | sell-through | martelo mediano | zero-bid |
|---|---|---|---|---|---|
| disco_vinil | 79374 | 60810 | 76,6% | R$ 42,00 | 22,9% |
| prata_metal | 76155 | 53000 | 69,6% | R$ 120,00 | 28,7% |
| conjunto_de_cadeiras | 2382 | 1598 | 67,1% | R$ 2.100,00 | 26,1% |
| carrinho_de_cha | 486 | 326 | 67,1% | R$ 1.000,00 | 25,1% |
| selo_filatelia | 36022 | 24011 | 66,7% | R$ 15,00 | 32,8% |
| sofa | 3176 | 2014 | 63,4% | R$ 2.600,00 | 28,0% |
| brinquedo | 135756 | 85776 | 63,2% | R$ 60,00 | 35,6% |
| par_de_poltronas | 3370 | 2126 | 63,1% | R$ 3.600,00 | 28,9% |
| mesa_lateral | 2866 | 1768 | 61,7% | R$ 460,00 | 31,5% |
| mesa_de_centro | 3269 | 1929 | 59,0% | R$ 1.100,00 | 34,8% |
| poltrona | 5811 | 3404 | 58,6% | R$ 2.100,00 | 33,6% |
| cama | 1427 | 832 | 58,3% | R$ 400,00 | 37,6% |

## 3. Top categorias por ticket (martelo mediano)

| item_type | martelo mediano | sell-through | ofertados |
|---|---|---|---|
| par_de_poltronas | R$ 3.600,00 | 63,1% | 3370 |
| sofa | R$ 2.600,00 | 63,4% | 3176 |
| conjunto_de_cadeiras | R$ 2.100,00 | 67,1% | 2382 |
| poltrona | R$ 2.100,00 | 58,6% | 5811 |
| mesa_de_jantar | R$ 1.900,00 | 55,6% | 1932 |
| escrivaninha | R$ 1.400,00 | 55,1% | 1054 |
| aparador | R$ 1.100,00 | 54,3% | 2868 |
| mesa_de_centro | R$ 1.100,00 | 59,0% | 3269 |
| carrinho_de_cha | R$ 1.000,00 | 67,1% | 486 |
| comoda | R$ 850,00 | 55,2% | 1154 |
| par_de_cadeiras | R$ 800,00 | 51,9% | 1818 |
| estante | R$ 650,00 | 55,5% | 2693 |

## 4. Categorias de baixa complexidade logística (foco operação solo)

| item_type | sell-through | martelo mediano | ofertados |
|---|---|---|---|
| prata_metal | 69,6% | R$ 120,00 | 76155 |
| mesa_lateral | 61,7% | R$ 460,00 | 2866 |
| mesa_de_centro | 59,0% | R$ 1.100,00 | 3269 |
| poltrona | 58,6% | R$ 2.100,00 | 5811 |
| espelho | 56,7% | R$ 350,00 | 4445 |
| cadeira | 55,4% | R$ 550,00 | 5946 |
| par_de_cadeiras | 51,9% | R$ 800,00 | 1818 |
| porcelana_ceramica | 51,1% | R$ 72,00 | 52532 |
| luminaria_lustre | 50,5% | R$ 200,00 | 14195 |
| objeto_decorativo | 47,9% | R$ 120,00 | 4766 |
| cristal_vidro | 41,0% | R$ 88,00 | 47051 |
| escultura | 33,8% | R$ 170,00 | 45444 |

## 5. Casas para sourcing (maior zero-bid + volume ≥50)

| casa | uf | finalizados | zero-bid | sell-through | martelo médio |
|---|---|---|---|---|---|
| Leilões Bruno Francesco | RJ | 270 | 100,0% | 0,0% | — |
| CH Collection - Numismática, Joias e Colecionáveis | PR | 386 | 100,0% | 0,0% | — |
| Sol Mar e Lua Leilões | SP | 233 | 100,0% | 0,0% | — |
| Casa de Leilões Guedes e Guedes | nan | 651 | 99,1% | 0,9% | R$ 157,50 |
| Coleções e Afins | MG | 600 | 98,7% | 1,3% | R$ 24,25 |
| 24K Joias Leilões | nan | 801 | 97,6% | 2,4% | R$ 1.625,79 |
| Oficina Cenário Leilões | nan | 452 | 96,5% | 3,1% | R$ 942,86 |
| Comitiva Artes e Leilões | nan | 2442 | 95,9% | 3,9% | R$ 1.770,83 |
| Vale Arte Leilões | SP | 518 | 95,8% | 4,2% | R$ 1.104,55 |
| Clássicos Modernos Leilões | RJ | 7860 | 95,4% | 4,4% | R$ 1.290,35 |
| Dell Fanny Jóias Leilões | RJ | 9625 | 95,3% | 4,4% | R$ 3.357,57 |
| Bons Tempos Leilões | RJ | 9936 | 94,5% | 5,2% | R$ 3.708,23 |
| Alvura Leilões Gestora de Ativos | PR | 4074 | 94,4% | 5,4% | R$ 336,40 |
| Eternno Leilões | RJ | 766 | 94,3% | 5,7% | R$ 1.318,41 |
| Castejón Branco Leilões | nan | 99 | 93,9% | 6,1% | R$ 131,67 |

_Zero-bid alto = mais chance de arrematar barato / pós-pregão._

## 6. Casas benchmark (maior sell-through, volume ≥50)

| casa | uf | finalizados | sell-through | martelo médio |
|---|---|---|---|---|
| Mania Comics | nan | 7276 | 100,0% | R$ 212,46 |
| Nossa Coleção | SP | 451 | 99,6% | R$ 107,07 |
| Vitrine das Antiguidades | SP | 258 | 99,2% | R$ 52,80 |
| Saturno Leilões | nan | 28500 | 99,1% | R$ 8,57 |
| Velho Armazém Leilões | nan | 220 | 99,1% | R$ 77,16 |
| Acervo Cult - Colecionismo Para Todos | nan | 5019 | 97,8% | R$ 100,31 |
| Filatélica MG Leilões | nan | 18052 | 97,7% | R$ 23,96 |
| Galeria República da Arte | PR | 200 | 97,5% | R$ 123,64 |
| Pariz Moedas | PR | 290 | 95,5% | R$ 89,35 |
| PRH Leilões | RS | 570 | 95,4% | R$ 47,49 |
| RH Leilões | nan | 600 | 95,3% | R$ 25,13 |
| Acervo do Garimpeiro | SP | 2856 | 95,1% | R$ 76,66 |
| Escafandro Discos - Antiguidades e Colecionáveis | nan | 12762 | 94,9% | R$ 120,25 |
| Colecionários | nan | 870 | 94,5% | R$ 54,88 |
| Ernani Leiloeiro Oficial | RJ | 953 | 93,7% | R$ 353,20 |

## 7. Oportunidades de compra (sinal BUY_NOW)

> **Como ler.** Estes são sinais de _triagem_, não lucros garantidos. A revenda é estimada pelo p25 (conservador) dos martelos de comparáveis × markup de varejo. O comp agrupa por (tipo, designer), então **não distingue o modelo/linha específico** (ex.: uma 'Poltrona Cimba' barata herda o comp de poltronas do mesmo designer). Trate margens altas em itens de lance muito baixo como candidatos a verificar peça a peça (use a coluna `lot_url` e a amostra de auditoria), não como certezas.

Total de lotes BUY_NOW: **20**. Top 25 por lucro estimado (conservador):

| título | tipo | designer | lance atual | revenda est. | margem | lance máx 40% | uf |
|---|---|---|---|---|---|---|---|
| Mesa estilo GIUSEPPE SCAPINELLI: Antiga base  | mesa_de_centro | giuseppe_scapinelli | R$ 100,00 | R$ 7.020,00 | 52,1% | R$ 544,76 | RJ |
| Mesa Auxiliar, Giuseppe Scapinelli - Produzid | mesa_lateral | giuseppe_scapinelli | R$ 900,00 | R$ 5.220,00 | 60,7% | R$ 1.509,43 | SP |
| Celina Zilberberg - Celina Decorações - Brasi | outro | celina | R$ 1.600,00 | R$ 6.030,00 | 48,4% | R$ 1.902,86 | RJ |
| Mesa Auxiliar, Giuseppe Scapinelli - Produzid | mesa_lateral | giuseppe_scapinelli | R$ 950,00 | R$ 5.220,00 | 59,0% | R$ 1.509,43 | SP |
| Par de poltronas em ferro tubular anos 60 ,na | par_de_poltronas | nan | R$ 390,00 | R$ 6.480,00 | 62,3% | R$ 929,05 | SP |
| Par de poltronas em ferro tubular anos 60 ,na | par_de_poltronas | nan | R$ 390,00 | R$ 6.480,00 | 62,3% | R$ 929,05 | SP |
| ATHOS BULCÃO  -  Gravura:  Aeroporto Internac | gravura | athos_bulcao | R$ 1.200,00 | R$ 4.383,00 | 52,9% | R$ 1.559,71 | nan |
| ATHOS BULCÃO  -  Gravura:  Aeroporto Internac | gravura | athos_bulcao | R$ 1.300,00 | R$ 4.383,00 | 49,3% | R$ 1.559,71 | nan |
| Espelho redondo de parede em madeira de jacar | espelho | sergio_rodrigues | R$ 1.500,00 | R$ 7.020,00 | 40,2% | R$ 1.507,88 | nan |
| Roberto Burle Marx - Serigrafia - Abstratos ( | gravura | burle_marx | R$ 675,00 | R$ 2.700,00 | 61,6% | R$ 1.120,00 | nan |
| Roberto Burle Marx - Serigrafia - Abstrato.   | gravura | burle_marx | R$ 675,00 | R$ 2.700,00 | 61,6% | R$ 1.120,00 | nan |
| Conjunto de sofá de três lugares e 2 poltrona | par_de_poltronas | nan | R$ 499,00 | R$ 6.480,00 | 46,0% | R$ 643,33 | RJ |
| Par de poltronas no formato Gondole no estilo | par_de_poltronas | nan | R$ 580,00 | R$ 6.480,00 | 42,6% | R$ 643,33 | RJ |
| Percival Lafer mesa de centro em madeira com  | mesa_de_centro | percival_lafer | R$ 350,00 | R$ 2.839,50 | 42,0% | R$ 443,05 | SP |
| Percival Lafer mesa de centro em madeira com  | mesa_de_centro | percival_lafer | R$ 410,00 | R$ 2.839,50 | 42,0% | R$ 443,05 | SP |
| cadeira design - poltrona antiga em acrilico, | poltrona | nan | R$ 190,00 | R$ 3.780,00 | 47,9% | R$ 299,05 | RJ |
| Par de cadeiras em plástico.  Altura: 0. 80 m | par_de_cadeiras | nan | R$ 10,00 | R$ 1.440,00 | 56,7% | R$ 113,14 | nan |
| Par de cadeiras medalhão, pés torneados e fri | par_de_cadeiras | nan | R$ 50,00 | R$ 1.440,00 | 50,2% | R$ 113,14 | RJ |
| Par de cadeiras com estofado bege em tecido a | par_de_cadeiras | nan | R$ 100,00 | R$ 1.440,00 | 42,1% | R$ 113,14 | RJ |
| Lote composto por cinco cadeiras avulsas de e | par_de_cadeiras | nan | R$ 100,00 | R$ 1.440,00 | 42,1% | R$ 113,14 | nan |

## 8. Carteira sugerida — estoque inicial

### R$ 30.000 — 20 peças, capital alocado R$ 12.567,45

| título | tipo | lance | lucro est. | margem | uf |
|---|---|---|---|---|---|
| Mesa estilo GIUSEPPE SCAPINELLI: Antiga ba | mesa_de_centro | R$ 100,00 | R$ 2.015,00 | 52,1% | RJ |
| Mesa Auxiliar, Giuseppe Scapinelli - Produ | mesa_lateral | R$ 900,00 | R$ 1.876,50 | 60,7% | SP |
| Celina Zilberberg - Celina Decorações - Br | outro | R$ 1.600,00 | R$ 1.830,00 | 48,4% | RJ |
| Mesa Auxiliar, Giuseppe Scapinelli - Produ | mesa_lateral | R$ 950,00 | R$ 1.824,00 | 59,0% | SP |
| Par de poltronas em ferro tubular anos 60  | par_de_poltronas | R$ 390,00 | R$ 1.583,00 | 62,3% | SP |
| Par de poltronas em ferro tubular anos 60  | par_de_poltronas | R$ 390,00 | R$ 1.583,00 | 62,3% | SP |
| ATHOS BULCÃO  -  Gravura:  Aeroporto Inter | gravura | R$ 1.200,00 | R$ 1.549,50 | 52,9% | nan |
| ATHOS BULCÃO  -  Gravura:  Aeroporto Inter | gravura | R$ 1.300,00 | R$ 1.444,50 | 49,3% | nan |
| Espelho redondo de parede em madeira de ja | espelho | R$ 1.500,00 | R$ 1.430,45 | 40,2% | nan |
| Roberto Burle Marx - Serigrafia - Abstrato | gravura | R$ 675,00 | R$ 1.331,25 | 61,6% | nan |
| Roberto Burle Marx - Serigrafia - Abstrato | gravura | R$ 675,00 | R$ 1.331,25 | 61,6% | nan |
| Conjunto de sofá de três lugares e 2 poltr | par_de_poltronas | R$ 499,00 | R$ 1.168,55 | 46,0% | RJ |
| Par de poltronas no formato Gondole no est | par_de_poltronas | R$ 580,00 | R$ 1.083,50 | 42,6% | RJ |
| Percival Lafer mesa de centro em madeira c | mesa_de_centro | R$ 350,00 | R$ 711,50 | 42,0% | SP |
| Percival Lafer mesa de centro em madeira c | mesa_de_centro | R$ 410,00 | R$ 711,50 | 42,0% | SP |
| cadeira design - poltrona antiga em acrili | poltrona | R$ 190,00 | R$ 690,50 | 47,9% | RJ |
| Par de cadeiras em plástico.  Altura: 0. 8 | par_de_cadeiras | R$ 10,00 | R$ 367,50 | 56,7% | nan |
| Par de cadeiras medalhão, pés torneados e  | par_de_cadeiras | R$ 50,00 | R$ 325,50 | 50,2% | RJ |
| Par de cadeiras com estofado bege em tecid | par_de_cadeiras | R$ 100,00 | R$ 273,00 | 42,1% | RJ |
| Lote composto por cinco cadeiras avulsas d | par_de_cadeiras | R$ 100,00 | R$ 273,00 | 42,1% | nan |

**Lucro bruto potencial da carteira (estimativa conservadora, a verificar peça a peça): R$ 23.403,00** (margem agregada 65,1%). Driver: peças de designer (Sergio Rodrigues, Burle Marx) com lance ainda baixo — confirme modelo/linha e autenticidade antes de arrematar.

### R$ 50.000 — 20 peças, capital alocado R$ 12.567,45

| título | tipo | lance | lucro est. | margem | uf |
|---|---|---|---|---|---|
| Mesa estilo GIUSEPPE SCAPINELLI: Antiga ba | mesa_de_centro | R$ 100,00 | R$ 2.015,00 | 52,1% | RJ |
| Mesa Auxiliar, Giuseppe Scapinelli - Produ | mesa_lateral | R$ 900,00 | R$ 1.876,50 | 60,7% | SP |
| Celina Zilberberg - Celina Decorações - Br | outro | R$ 1.600,00 | R$ 1.830,00 | 48,4% | RJ |
| Mesa Auxiliar, Giuseppe Scapinelli - Produ | mesa_lateral | R$ 950,00 | R$ 1.824,00 | 59,0% | SP |
| Par de poltronas em ferro tubular anos 60  | par_de_poltronas | R$ 390,00 | R$ 1.583,00 | 62,3% | SP |
| Par de poltronas em ferro tubular anos 60  | par_de_poltronas | R$ 390,00 | R$ 1.583,00 | 62,3% | SP |
| ATHOS BULCÃO  -  Gravura:  Aeroporto Inter | gravura | R$ 1.200,00 | R$ 1.549,50 | 52,9% | nan |
| ATHOS BULCÃO  -  Gravura:  Aeroporto Inter | gravura | R$ 1.300,00 | R$ 1.444,50 | 49,3% | nan |
| Espelho redondo de parede em madeira de ja | espelho | R$ 1.500,00 | R$ 1.430,45 | 40,2% | nan |
| Roberto Burle Marx - Serigrafia - Abstrato | gravura | R$ 675,00 | R$ 1.331,25 | 61,6% | nan |
| Roberto Burle Marx - Serigrafia - Abstrato | gravura | R$ 675,00 | R$ 1.331,25 | 61,6% | nan |
| Conjunto de sofá de três lugares e 2 poltr | par_de_poltronas | R$ 499,00 | R$ 1.168,55 | 46,0% | RJ |
| Par de poltronas no formato Gondole no est | par_de_poltronas | R$ 580,00 | R$ 1.083,50 | 42,6% | RJ |
| Percival Lafer mesa de centro em madeira c | mesa_de_centro | R$ 350,00 | R$ 711,50 | 42,0% | SP |
| Percival Lafer mesa de centro em madeira c | mesa_de_centro | R$ 410,00 | R$ 711,50 | 42,0% | SP |
| cadeira design - poltrona antiga em acrili | poltrona | R$ 190,00 | R$ 690,50 | 47,9% | RJ |
| Par de cadeiras em plástico.  Altura: 0. 8 | par_de_cadeiras | R$ 10,00 | R$ 367,50 | 56,7% | nan |
| Par de cadeiras medalhão, pés torneados e  | par_de_cadeiras | R$ 50,00 | R$ 325,50 | 50,2% | RJ |
| Par de cadeiras com estofado bege em tecid | par_de_cadeiras | R$ 100,00 | R$ 273,00 | 42,1% | RJ |
| Lote composto por cinco cadeiras avulsas d | par_de_cadeiras | R$ 100,00 | R$ 273,00 | 42,1% | nan |

**Lucro bruto potencial da carteira (estimativa conservadora, a verificar peça a peça): R$ 23.403,00** (margem agregada 65,1%). Driver: peças de designer (Sergio Rodrigues, Burle Marx) com lance ainda baixo — confirme modelo/linha e autenticidade antes de arrematar.

## 9. Lances máximos por tipo de peça (para margem de 40%)

| item_type | lance máx mediano (40% margem) |
|---|---|
| outro | R$ 1.902,86 |
| mesa_lateral | R$ 1.509,43 |
| espelho | R$ 1.507,88 |
| gravura | R$ 1.339,86 |
| par_de_poltronas | R$ 786,19 |
| mesa_de_centro | R$ 443,05 |
| poltrona | R$ 299,05 |
| par_de_cadeiras | R$ 113,14 |

## 10. Modelo A (casa de leilão) vs Modelo B (garimpo + revenda)

- **GMV observado** nas casas amostradas (martelo × vendidos): ~R$ 99.726.978,00 na janela de 14/01/2015 a 02/07/2026 (4188 dias) — denso e pulverizado entre muitas casas.
- **Modelo A** com take de 15,0%: para cobrir OPEX de R$ 10.000 / 15.000 / 25.000 ao mês, a casa precisaria de GMV mensal de ~R$ 66.666,67 / R$ 100.000,00 / R$ 166.666,67 respectivamente. Exige curadoria, captação de consignação e base de compradores — difícil para operação solo no início.
- **Modelo B** já é acionável hoje: 20 lotes BUY_NOW com margem ≥ 40,0%, capital inicial de R$ 30k aloca 20 peças. Giro depende de logística — por isso o foco em peças small/medium/large.

**Recomendação:** começar pelo **Modelo B** (menor capital travado, risco operacional menor, lucro por peça verificável com os dados). Migrar para **Modelo A** quando o GMV mensal de revenda ultrapassar consistentemente ~R$ 100.000,00 e houver fluxo de consignação — aí o take fixo da casa passa a compensar o OPEX.

## 11. Limitações e vieses

- Janela de finalizados observada: 14/01/2015 a 02/07/2026 (4188 dias); sazonalidade anual não capturada.
- Algumas casas usam plataforma distinta (≈10% de falhas 404/JSON) e ficam fora da amostra.
- Lotes ao vivo têm só título (descrição completa não disponível sem por-leilão); atribuição de designer pode ter falso-negativo quando o nome só aparece na descrição.
- Valor de revenda assume preço de mercado = mediana de martelo de comparáveis; é conservador para venda de varejo no Instagram e tem baixa confiança onde há poucos comps.
- Custos de frete/restauro são premissas (`assumptions.yaml`), não cotações.

## 12. Premissas usadas (`assumptions.yaml`)

```yaml
buyer_premium_pct: 0.05
resale_channel_fee_pct: 0.0
shipping_brl:
  small: 80
  medium: 180
  large: 350
  xl: 600
packaging_brl:
  small: 40
  medium: 90
  large: 200
  xl: 350
restoration_brl:
  none: 0
  light: 300
  heavy: 1200
resale:
  min_comps: 5
  retail_markup_over_hammer: 1.8
  fallback_markup_over_hammer: 1.8
signals:
  buy_now:
    min_margin_pct: 0.4
    max_logistics_size: large
    min_attribution_for_designer_claim: STATED
    max_bid_count: 8
    min_confidence: 0.55
  watch:
    min_margin_pct: 0.25
    min_confidence: 0.4
capital_scenarios_brl:
- 30000
- 50000
```