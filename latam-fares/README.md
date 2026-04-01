# LATAM Fare Discovery

Ferramenta para identificar combinações vantajosas de passagens aéreas
usando o endpoint de calendário interno da LATAM.

## Como instalar
pip install -r requirements.txt

## Como rodar
streamlit run app.py

## Uso rápido
1. Preencha origem/destino de ida e volta na sidebar
2. Ajuste período, regras de viagem e timeout por consulta
3. Se a API responder 403/timeout por sessão, cole o header `Cookie` no campo **Cookies (opcional)**
4. Clique em **Buscar combinações**
5. Veja os cards, tabela principal e dados brutos para debug

## Estrutura
latam-fares/
├── app.py               # UI Streamlit
├── services/
│   ├── latam_api.py     # Camada HTTP + parsing
│   └── combinator.py    # Lógica de combinação e ranking
└── utils/
    ├── dates.py
    └── formatting.py

## Limitações conhecidas
- O endpoint /bff/ é interno da LATAM e pode mudar sem aviso
- Requer headers de navegador válidos; pode precisar de cookies de sessão
- Preços do calendário são indicativos — o valor final pode diferir na checkout
- Sem histórico de preços nesta versão
- Sem alertas ou notificações nesta versão

## Como customizar headers/cookies
Ver seção CONFIGURAÇÃO em services/latam_api.py
