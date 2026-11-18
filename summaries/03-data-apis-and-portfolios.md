# Lecture 3 — APIs, pandas e Estratégias de Portefólio

> Resumo exportado das notas em Notion (18/11/2026). As respostas das perguntas *Testa-te* estão escondidas: clica em **Resposta** para as ver.

## Lecture 3: APIs e pandas

**API** (Application Programming Interface) é uma forma de um programa pedir dados a outro serviço (FRED, Yahoo Finance, CoinGecko) sem descarregar ficheiros à mão. **pandas** é a biblioteca para trabalhar com tabelas de dados e é construída em cima do NumPy.

```py
import numpy as np
import pandas as pd
```

### FRED (Federal Reserve Economic Data)

```py
!pip install -q fredapi            # "!" corre um comando de terminal no notebook; -q = modo silencioso
from fredapi import Fred
fred = Fred(api_key='GET_YOUR_API_KEY')   # precisas de criar uma chave gratuita no site da FRED
data = fred.get_series('UNRATE')          # 'UNRATE' = ID da taxa de desemprego dos EUA (mensal)
```

### pandas Series: uma coluna de dados com índice

```py
s = pd.Series(np.random.rand(5), name='daily returns')   # índice por defeito: 0, 1, 2, 3, 4
s.index = ['AMZN', 'AAPL', 'MSFT', 'GOOG', 'TSLX']        # índice com nomes
s['MSFT']      # seleciona pelo NOME do índice
s.iloc[2]      # seleciona pela POSIÇÃO (2 = terceiro) → o mesmo valor
```

- Suporta as mesmas operações estatísticas e aritméticas que o NumPy, e mais algumas.

```py
sum_stats = data.describe()     # count, mean, std, min, 25%, 50%, 75%, max
sum_stats['50%']                # mediana
sum_stats['max']                # máximo
'iqr' in sum_stats              # False → verifica se um índice existe
'std' in sum_stats              # True
```

- Gráficos diretos (o pandas usa o Matplotlib por baixo):

```py
ax = data['2006':'2012'].plot(title='US Unemployment Rate', legend=False)   # fatia por datas!
ax.set_xlabel('year', fontsize=12)
ax.set_ylabel('%', fontsize=12)
```

Com um índice de datas, `data['2006':'2012']` seleciona o período diretamente pelas datas.

### Yahoo Finance (yfinance)

```py
import yfinance as yf
df = yf.download("TSLA",
                 start="2012-01-01", end="2024-12-31",
                 interval='1mo',          # dados mensais
                 progress=False)          # esconde a barra de progresso
print(f"Downloaded {len(df)} rows of data.")
```

- Vários tickers de uma vez: `["AAPL", "MSFT"]` ou `"AAPL MSFT"`.
- `auto_adjust=True` dá preços ajustados a dividendos e splits (hoje já é o padrão).
- `actions='inline'` também descarrega dividendos e stock splits.
- `interval` pode ser `1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo`. Os dados intradiários (`1m`) só existem para períodos com menos de 60 dias.
- **Atenção:** a data `end` **não é incluída**.

### pandas DataFrame: várias colunas

Um DataFrame é como uma **folha de Excel muito otimizada**: linhas e colunas com nomes.

```py
tesla_data = yf.Ticker("TSLA")
df = tesla_data.history()      # por defeito: dados diários dos últimos ~5 anos
```

#### Selecionar por posição e por nome

```py
df[2:5]                              # linhas 2, 3 e 4
df[['High', 'Low']]                  # colunas pelo nome (lista de strings)
df.iloc[2:5, 0:4]                    # iloc = só POSIÇÕES: linhas 2-4, colunas 0-3
df.loc[df.index[2:5], ['High', 'Low']]   # loc = NOMES (índice e colunas)
```

- **`iloc`** usa posições inteiras, como num array.
- **`loc`** usa rótulos: datas, nomes de colunas, ou máscaras booleanas.

#### Selecionar por condições (indexação booleana, como no NumPy)

```py
df[df.Open >= 450]                               # dias em que o preço de abertura ≥ 450
df[(df.Close - df.Open > 0) & (df.Open >= 450)]  # dias de subida E abertura ≥ 450
```

No pandas combina-se condições com **`&`** (e) e **`|`** (ou), **não** com `and` / `or`. Cada condição tem de ficar entre parênteses.

#### apply: aplicar uma função a cada coluna ou linha

```py
df[['Close', 'Volume']].apply(max)   # máximo de cada coluna → devolve uma Series
```

#### Informação da empresa

- `tesla_data.info`: dicionário com nome, descrição, bolsa, beta, etc. Exemplo: `tesla_data.info['website']`.
- `actions`: dividendos e splits.
- `major_holders` / `institutional_holders`: principais acionistas.
- `calendar`: próximos eventos (por exemplo, resultados trimestrais).
- `earnings` / `quarterly_earnings`: lucros anuais e trimestrais.
- `financials` / `quarterly_financials`: income before tax, net income, gross profit, EBIT, etc.

### Descarregar dados com requests (sem API própria)

No site da FRED, botão Download, copia-se o link do `.csv`:

```py
import requests
url = 'https://fred.stlouisfed.(...)'
source = requests.get(url).content.decode().split("\n")
# requests.get → pede o ficheiro ao servidor (pedido HTTP GET)
# .content     → bytes brutos da resposta
# .decode()    → converte bytes em texto
# .split("\n") → parte o texto em linhas (CSV = uma linha por registo)
source[0]      # cabeçalho → confirma que o download funcionou

data = pd.read_csv(url, index_col=0, parse_dates=True)
# index_col=0      → primeira coluna (datas) passa a ser o índice
# parse_dates=True → converte o índice em datas reais
data.head()                               # primeiras 5 linhas
pd.set_option('display.precision', 1)     # mostrar 1 casa decimal
data.describe()
```

### CoinGecko (cripto)

```py
!pip install -q pycoingecko
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()                       # cria o "cliente" para fazer pedidos

# OHLC (open, high, low, close) da Bitcoin; days só aceita 1/7/14/30/90/180/365/max
ohlc = cg.get_coin_ohlc_by_id(id="bitcoin", vs_currency="usd", days="14")
ohlc_df = pd.DataFrame(ohlc)
ohlc_df.columns = ["date", "open", "high", "low", "close"]
ohlc_df["date"] = pd.to_datetime(ohlc_df["date"], unit="ms")   # timestamp em milissegundos → data

cg.get_price(ids=["bitcoin", "ethereum"], vs_currencies=["usd", "eur"])   # preço atual
```

### Complementos do notebook (Lecture 3, Part 1)

#### Ferramentas e quando usar cada uma

| Fonte / ferramenta | Para quê | Linha-chave |
| --- | --- | --- |
| **FRED** (`fredapi`) | Séries macroeconómicas (desemprego, juros, inflação). Precisa de API key gratuita | `fred.get_series('UNRATE')` → Series |
| **Yahoo Finance** (`yfinance`) | Preços de ações, ETFs, índices; info da empresa | `yf.download(tickers, start, end, interval='1mo', auto_adjust=True)` |
| `yf.Ticker` | Histórico recente + dados da empresa | `yf.Ticker("TSLA").history()` |
| **requests** / `pd.read_csv(url)` | Quando não há package: qualquer CSV num URL | `pd.read_csv(url, index_col=0, parse_dates=True)` |
| **CoinGecko** (`pycoingecko`) | Cripto (OHLC, preço atual) | `cg.get_coin_ohlc_by_id(id="bitcoin", vs_currency="usd", days="14")` |

**No group assignment não podes entregar ficheiros de dados**, só código que os vai buscar.

#### As 4 checks (aplicar a TODOS os downloads)

```py
print(df.shape)                          # 1. quantas linhas/colunas? (2015–2024 mensal ≈ 120 linhas)
print(df.index[0], df.index[-1])         # 2. o período é o que pediste?
print(df.isna().sum())                   # 3. quantos NaN por coluna?
df.Close.plot()                          # 4. parecem preços/retornos ou lixo?
```

#### 3.3 Practice: o bug do colega (o exemplo mais importante da aula)

```py
tickers = ['AAPL', 'MSFT', 'NVDA', 'PLTR']
prices = yf.download(tickers, start='2015-01-01', end='2024-12-31',
                     interval='1mo', auto_adjust=True, progress=False)['Close']
prices = prices.dropna()                  # ← AQUI: apaga qualquer linha com UM NaN
rets = np.log(prices).diff(1).dropna()
```

A Palantir só entrou em bolsa em **setembro de 2020**, por isso a coluna PLTR é NaN antes disso. O `dropna()` apagou **5 anos de dados das 4 ações**, sem dar erro. As checks 1 e 2 (shape e date range) apanham-no logo. Soluções: retirar a PLTR, aceitar a amostra 2020–2024 conscientemente, ou `dropna(how='all')` e tratar cada ação separadamente. É parecido com survivorship bias: **as escolhas de limpeza definem a amostra**.

#### 3.5 Homework: EDP, Galp e Jerónimo Martins

O objetivo é escrever um **prompt** preciso para o assistente de IA (sufixo `.LS`, log vs. simple, mensal, ajustado, regra de dropna, fator de anualização). Cada ambiguidade no prompt volta como uma suposição silenciosa no código.

<details>
<summary>Solução possível</summary>

```py
import numpy as np
import yfinance as yf

tickers = ['EDP.LS', 'GALP.LS', 'JMT.LS']
prices = yf.download(tickers, start='2017-12-01', end='2025-01-01',   # dez/2017 para ter o retorno de jan/2018; end exclusivo
                     interval='1mo', auto_adjust=True, progress=False)['Close']

rets = np.log(prices).diff().dropna()     # log-returns mensais

# 4 checks
print(rets.shape)                         # esperado: ~84 linhas (7 anos × 12), 3 colunas
print(rets.index[0], rets.index[-1])      # jan/2018 → dez/2024
print(rets.isna().sum())                  # tudo 0
rets.plot()

vol = rets.std() * np.sqrt(12)            # volatilidade anualizada
print(vol)
```

Não corri este código: confirma no Colab. Ordem de grandeza esperada: a EDP (utility) mais baixa (\~20%/ano) e a Galp (petrolífera) mais alta (\~30%/ano).

</details>


## Lecture 3: Estratégias de Portefólio

### Portefólios e pesos

- Um portefólio é uma coleção de ativos, representada por um vetor de **pesos** w = (w\_1, …, w\_N). O peso w\_i diz quanto investes no ativo i relativamente aos outros.
- **Posição longa:** w\_i > 0. Num portefólio **long-only**, todos os pesos são positivos.
- **Posição curta (short):** w\_i \< 0. Pedes o ativo emprestado, vendes, e mais tarde recompras (esperando um preço mais baixo).
- **Ativo sem risco ("cash"):** w\_f > 0 quer dizer investir à taxa sem risco. w\_f \< 0 quer dizer pedir emprestado, ou seja, **alavancagem**.

**Os pesos somam 1** (quando investes o teu próprio dinheiro). Com 1.000 €:

- Long-only: 600 € em EDP e 400 € em CTT dá w\_E = 0,6 e w\_C = 0,4.
- Alavancado: 800 € em EDP, 500 € em CTT e −300 € no ativo sem risco dá w\_E = 0,8, w\_C = 0,5 e w\_f = −0,3. A soma continua a ser 1.

### Portefólios self-financing (os pesos somam 0)

- Começas com zero de dinheiro próprio. Pedes 1.000 € emprestados e investes-os: w\_E = 0,6, w\_C = 0,4 e w\_f = −1.
- Também podes vender ativos a descoberto em vez de pedir dinheiro emprestado. Por exemplo, vender 1.300 € de Galp a descoberto e investir 800 € em EDP e 500 € em CTT.
- Os pesos passam a representar a fração de cada **perna**: a perna longa soma +1 e a perna curta soma −1.
- **Na prática:** quase ninguém te empresta 10.000 € para investires sem dinheiro próprio. Mas é um conceito teórico útil para comparar o desempenho **relativo** de ativos.
- Só ganha dinheiro se **a perna longa bater a perna curta**.
- O **excess return** E\[R\_p\] − R\_f é exatamente o retorno de um portefólio self-financing que pede emprestado a R\_f e investe em p.

### Portefólio vs. estratégia

- **Portefólio** é um conceito **estático**: pesos fixos num momento do tempo.
- **Estratégia** é um conceito **dinâmico**: regras para mudar os pesos ao longo do tempo. **Rebalancear** é comprar e vender para voltar aos pesos-alvo.
- Uma estratégia **rules-based** segue regras pré-definidas em vez do julgamento do gestor. Exemplos: pesos fixos para sempre, ou comprar o S&P 500 na proporção da capitalização bolsista.

#### Exemplo: manter pesos fixos dá trabalho

Alvo: 60% EDP e 40% CTT, com 1.000 €.

- Hoje compras 150 ações da EDP a 4 € (600 €) e 80 ações dos CTT a 5 € (400 €).
- Um mês depois, a EDP está a 5 € e os CTT a 5,5 €. As posições passam a valer 750 € e 440 €, num total de 1.190 €.
- Os pesos derivaram para w\_E = 750/1.190 = **0,63** e w\_C = **0,37**.
- Para voltar a 60/40 tens de **vender** 150 − (1.190 × 0,6 / 5) = **7,2 ações da EDP** e **comprar** 1.190 × 0,4 / 5,5 − 80 = **6,5 ações dos CTT**.
- Mesmo uma estratégia "passiva" obriga a vender o que subiu e comprar o que desceu.

### A estratégia 1/n (pesos iguais)

- Dá o mesmo peso a todos os ativos.
- DeMiguel, Garlappi e Uppal (2007) mostram que é **difícil bater a 1/n** com métodos de alocação mais sofisticados, porque estes sofrem com erros de estimação.
- Com o pacote **quantstats** gera-se um **tear sheet**: um resumo, normalmente numa página, com todas as métricas de desempenho.

#### Passo a passo (setor financeiro dos EUA, mensal, 2010–2024)

```py
import yfinance as yf, numpy as np, pandas as pd
!pip -q install quantstats
import quantstats as qs

# 1. Tickers das maiores empresas do setor financeiro e preços de fecho
fs = yf.Sector('financial-services')
df = yf.download(list(fs.top_companies.index),
                 start='2010-12-01', end='2024-12-01', interval='1mo', auto_adjust=True)
df = df['Close']
df_benchmark = yf.download("^GSPC", start='2010-12-01', end='2024-12-01',
                           interval='1mo', auto_adjust=True)['Close']    # S&P 500

# 2. Gráfico de algumas ações (loc com nomes de colunas)
df.loc[:, ['GS', 'JPM', 'C', 'WFC', 'BAC', 'V', 'MA']].plot(title="Financial Services stocks")

# 3. Log-retornos e limpeza de dados em falta
returns = np.log(df) - np.log(df.shift(1))      # shift(1) = preço do mês anterior
ind_na = np.sum(returns.isna(), axis=0)         # nº de valores em falta por ação
returns = returns.iloc[:, list(ind_na <= 1)]    # fica só com ações com ≤1 NaN (o 1º mês)
returns = returns.dropna()
n_assets = returns.shape[1]                     # nº de ações que restam
portfolio_weights = np.ones(n_assets) * (1/n_assets)

sp500 = (np.log(df_benchmark) - np.log(df_benchmark.shift(1))).dropna()
sp500 = sp500.tz_localize(None)                 # remove o fuso horário das datas
returns = returns.tz_localize(None)              # (para os dois índices serem compatíveis)

# 4. Retornos do portefólio 1/n = soma ponderada dos retornos
portfolio_returns = pd.DataFrame(np.dot(portfolio_weights, returns.T),
                                 index=returns.index, columns=['ptf'])
```

- **Log-retorno:** ln(P\_t) − ln(P\_\{t−1\}). Para retornos pequenos é quase igual ao retorno simples e tem a vantagem de se poder **somar ao longo do tempo**.
- **`np.dot`** é o produto matricial: em cada mês, Σ w\_i × r\_i.

### Alfa e beta

Regressão do excess return da estratégia sobre o excess return do mercado:

$$
R^{ex}_t = \alpha + \beta \, R^{ex}_{M,t} + \varepsilon_t
$$

- **Beta (β):** exposição ao mercado. Com β = 0,5, se o mercado sobe 10% a estratégia sobe 5%, tudo o resto constante. Por exemplo, metade em ações e metade em cash.
- **Alfa (α):** retorno extra além do explicado pelo mercado. É o valor acrescentado pelo talento do gestor (ou pela sorte, porque é estimado com retornos realizados).
- **ε (risco idiossincrático):** parte específica da estratégia, com média zero e independente do mercado. Por exemplo, o desempenho relativo de ações de biotech face ao mercado.
- **Exemplo:** um hedge fund *market-neutral* (β = 0) com α = 6%/ano e taxa sem risco de 2% espera ganhar 8%/ano. O valor realizado pode ser muito diferente, consoante o choque idiossincrático.

Estimação sem regressão:

$$
\beta = \frac{cov(R^{ex}, R^{ex}_M)}{var(R^{ex}_M)} \qquad \alpha = \overline{R^{ex}} - \beta \, \overline{R^{ex}_M}
$$

#### Alfa e beta rolantes (janela de 60 meses)

Mais útil do que um único valor: estima-se com os primeiros 60 meses, avança-se a janela um mês, e assim sucessivamente.

```py
window = 60
s = sp500['^GSPC']
p = portfolio_returns['ptf']          # (assume-se r_f = 0)
rolling_beta = p.rolling(window).cov(s) / s.rolling(window).var()
rolling_alpha = p.rolling(window).mean() - rolling_beta * s.rolling(window).mean()

import matplotlib.pyplot as plt
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)   # 2 gráficos empilhados, mesmo eixo x
ax1.plot(rolling_beta, color='blue');   ax1.set_title('Rolling Beta')
ax2.plot(1200*rolling_alpha, color='green'); ax2.set_title('Rolling Alpha')
# ×1200 = ×12 (anualizar mensal) ×100 (em %)
plt.tight_layout(); plt.show()

# alternativa com quantstats (baseada em regressão OLS → mais suave e estável)
alpha_beta_rolling = qs.stats.rolling_greeks(p, benchmark=s, periods=60, prepare_returns=False)
```

**Como ler:**

- β > 1: mais volátil do que o S&P 500.
- β \< 1: mais estável.
- β ≈ 0: sem exposição ao mercado.
- β \< 0: move-se ao contrário do mercado.
- α > 0: a estratégia bate o retorno esperado dado o seu risco de mercado. α \< 0: fica abaixo.

### Rácios risco–retorno

O alfa não chega como medida, por duas razões: não diz **com que risco** foi obtido, e depende da escala (uma estratégia com 2× de alavancagem tem 2× o alfa, mas a qualidade é a mesma).

#### Sharpe ratio: retorno por unidade de risco total

$$
SR = \frac{E[R - R_f]}{\sigma(R - R_f)}
$$

```py
SR_qs = qs.stats.sharpe(p, periods=12, annualize=True)
r_f = 0
SR_monthly = (p.mean() - r_f) / p.std()
SR_annualized = (12*(p.mean() - r_f)) / (np.sqrt(12)*p.std())    # = √12 × SR mensal
```

- **Anualizar:** a média multiplica por 12 e o desvio padrão por √12 (a variância cresce linearmente com o tempo). Por isso o SR anual é √12 ≈ 3,46 vezes o mensal.
- Quanto maior, melhor. Mas é uma medida limitada quando os retornos são assimétricos ou há risco de crash.

#### Information ratio: talento por unidade de risco idiossincrático

O Sharpe dá crédito a todo o excess return, incluindo o que vem só de estar exposto ao mercado. O IR olha só para o alfa:

$$
IR = \frac{\alpha}{\sigma(\varepsilon)} \qquad \text{ou, face a um benchmark:} \qquad IR = \frac{E[R - R_b]}{\sigma(R - R_b)}
$$

- **Tracking error** é a diferença entre o retorno da estratégia e o do benchmark. O desvio padrão dessa diferença é o **tracking error risk**.
- O IR mede **com que consistência** a estratégia bate o benchmark.

```py
IR_qs = qs.stats.information_ratio(p, benchmark=s, prepare_returns=False)
tracking_error = p - s
IR_monthly = tracking_error.mean() / tracking_error.std()
IR_annualized = (12*tracking_error.mean()) / (np.sqrt(12)*tracking_error.std())
```

#### Drawdowns

- **High water mark (HWM):** o valor máximo atingido até agora.

$$
HWM_t = \max_{s \le t} P_s \qquad DD_t = \frac{HWM_t - P_t}{HWM_t} \qquad MDD = \max_t DD_t
$$

- Os hedge funds normalmente só cobram **performance fees acima do HWM**: depois de uma perda, têm de a recuperar primeiro.
- O **drawdown** é a perda desde o último pico. É zero no pico e positivo no resto do tempo.
- Grandes drawdowns custam caro: além da perda direta, levam a **resgates** de investidores e a reações das contrapartes (o prime broker sobe as margens ou corta o financiamento).
- O **maximum drawdown (MDD)** é a pior queda pico–vale num período.

```py
qs.reports.metrics(p, benchmark=s, periods_per_year=12, prepare_returns=False)   # tabela com todas as métricas
qs.plots.drawdowns_periods(portfolio_returns, title="1/n of Financial stocks")   # piores períodos de drawdown
```

### Complementos do notebook (Lecture 3, Part 2)

#### 3.6 Practice: "a IA escreveu, devo confiar?"

Pedido à IA: *"Calcula o Sharpe ratio anualizado de um portefólio equal-weighted das minhas ações, a partir do DataFrame df de preços mensais."*

```py
ptf_series = df.mean(axis=1)                    # "equal-weighted portfolio"
sharpe = ptf_series.mean() / ptf_series.std() * np.sqrt(12)
print(f"Annualized Sharpe ratio: {sharpe:.2f}")
```

- **Bug 1:** calcula o Sharpe dos **preços**, não dos retornos. Um preço que sobe sempre dá um rácio enorme e sem significado (nenhuma estratégia real tem Sharpe de 8: a plausibilidade também é uma check).
- **Bug 2:** fazer a média dos preços não é 1/n: dá mais peso às ações com preço alto (é um índice price-weighted, o defeito do Dow). A ponderação igual faz-se nos **retornos**: `rets.mean(axis=1)`.
- **Bug 3:** não subtrai a taxa sem risco.

```py
rets = np.log(df).diff(1).dropna()
ptf = rets.mean(axis=1)                       # 1/n nos retornos
rf = 0.0
sharpe = (12*ptf.mean() - rf) / (np.sqrt(12)*ptf.std())   # subtrair rf quando > 0
```

#### 3.7 Homework: a tua própria 1/n

Escolhe 8–15 ações de *outro* setor (ou um universo europeu, com sufixos `.LS`, `.DE`), 2011–2024, mensal. Constrói a 1/n e produz: beta rolante, Sharpe anualizado, information ratio face a um benchmark adequado (o S&P 500 ainda faz sentido para ações europeias?) e o gráfico de drawdowns.

### Armadilhas da Lecture 3

#### Part 1: pandas e APIs

- **`dropna()` apaga a linha inteira** se houver um único NaN. Com uma ação de histórico curto, encolhe a amostra de todas.
- **`&` / `|`, não `and` / `or`**, e cada condição **entre parênteses**.
- **`iloc` exclui o fim** (como em Python). `loc` com fatias de labels (ex.: `data['2006':'2012']`) **inclui** o fim.
- **`df['X']` → Series**; **`df[['X']]` → DataFrame**. `df[2:5]` seleciona **linhas**.
- No `yf.download`, a data **`end` não é incluída**. Para ter dezembro de 2024, usa `end='2025-01-01'`.
- **`auto_adjust=True`** → preços ajustados a dividendos e splits. Os retornos calculam-se sempre a partir destes.
- Com vários tickers, as colunas vêm em **MultiIndex** ('Close' + 'TSLA'), por isso faz-se `[...]['Close']`.
- `.diff()` / `.shift(1)` deixam o **primeiro valor NaN**: n preços dão n−1 retornos.
- `'x' in series` procura no **índice**, não nos valores.
- Tickers de Lisboa no Yahoo têm o sufixo **`.LS`**. CoinGecko devolve datas em **milissegundos** (`unit='ms'`).
- **Nunca escrevas a tua API key no notebook que entregas.**

#### Part 2: Portefólios

- **Pesos somam 1** num portefólio normal (mesmo com alavancagem: o cash fica negativo) e **0** num self-financing.
- **"Pesos fixos" não é "não fazer nada"**: os preços mexem e tens de rebalancear (vender o que subiu, comprar o que desceu).
- **Anualizar:** média × 12, desvio padrão × √12 → Sharpe/IR × √12 (não × 12).
- **Sharpe usa excess returns** (R − R\_f). Se vês `mean()/std()` chamado de Sharpe, pergunta onde está o R\_f.
- **Alfa escala com a alavancagem, o Sharpe não.** Por isso o alfa sozinho não chega para avaliar.
- **Sharpe vs. IR:** o Sharpe premeia todo o excess return (incluindo só estar exposto ao mercado); o IR só o que bate o benchmark, por unidade de tracking error.
- **β = 0,5**: mercado +10% → estratégia +5% (tudo o resto constante). β ≈ 0 é market-neutral, não "sem risco".
- **Drawdown é 0 no pico** e positivo depois; o MDD é a pior queda pico–vale.
- **1/n faz-se nos retornos**, não nos preços (média de preços = price-weighted).
- **`×1200`** no gráfico do alfa = ×12 (anualizar) × 100 (em %).
- **`tz_localize(None)`**: os índices do benchmark e das ações têm de ter o mesmo formato de datas para se alinharem.

### Números de referência da Lecture 3

| Exemplo | Resultado |
| --- | --- |
| 2015–2024 mensal | ≈ 120 linhas (se der muito menos, algo correu mal) |
| PLTR | dados só a partir de set/2020 |
| Anualizar mensal / diário | ×√12 ≈ 3,46 / ×√252 ≈ 15,9 |
| Rebalancear 60/40 EDP/CTT (1.000 € → 1.190 €) | pesos derivam para 0,63 / 0,37 · vender 7,2 EDP, comprar 6,5 CTT |
| Portefólio alavancado (800 EDP + 500 CTT − 300 cash) | pesos 0,8 + 0,5 − 0,3 = 1 |
| Hedge fund market-neutral, α = 6%, R\_f = 2% | retorno esperado 8%/ano |
| Janela rolante de alfa/beta | 60 meses |

### Testa-te: Lecture 3

**1.** O que devolve `df.iloc[2:5, 0:4]`?<br>(a) Linhas 2–5 e colunas 0–4 · (b) Linhas 2–4 e colunas 0–3 · (c) As linhas cujo label é 2 a 5 · (d) Um erro

<details>
<summary>Resposta</summary>

**(b)**. `iloc` usa posições e o fim é excluído, como em Python.

</details>

**2.** Qual destas linhas filtra corretamente os dias de subida com volume acima de 1 milhão?<br>(a) `df[df.Close > df.Open and df.Volume > 1e6]` · (b) `df[df.Close > df.Open & df.Volume > 1e6]` · (c) `df[(df.Close > df.Open) & (df.Volume > 1e6)]` · (d) `df[(df.Close > df.Open) and (df.Volume > 1e6)]`

<details>
<summary>Resposta</summary>

**(c)**. Em pandas usa-se `&` (não `and`), e cada condição tem de estar entre parênteses, porque `&` tem precedência maior do que `>`.

</details>

**3.** Descarregas preços mensais de 4 ações desde 2015. Uma delas só entrou em bolsa em 2020. Depois de `prices.dropna()`:<br>(a) Só a coluna dessa ação perde dados · (b) A amostra das 4 ações passa a começar em 2020 · (c) O Python dá erro · (d) Os NaN passam a 0

<details>
<summary>Resposta</summary>

**(b)**. `dropna()` apaga qualquer linha com pelo menos um NaN, por isso perdes os anos antes de 2020 para todas as ações, sem nenhum erro.

</details>

**4.** Uma estratégia tem Sharpe ratio mensal de 0,3. Qual é o Sharpe anualizado?<br>(a) 0,3 · (b) 1,04 · (c) 3,6 · (d) 0,09

<details>
<summary>Resposta</summary>

**(b)**. 0,3 × √12 ≈ 1,04. A média escala com 12 e o desvio padrão com √12, por isso o rácio escala com 12/√12 = √12. A (c) é o erro clássico de multiplicar por 12.

</details>

**5.** Com 1.000 € próprios, investes 800 € em EDP, 500 € em CTT e pedes 300 € emprestados. Quais são os pesos?<br>(a) 0,8 / 0,5 / 0,3 · (b) 0,8 / 0,5 / −0,3 · (c) 0,62 / 0,38 / 0 · (d) 0,8 / 0,5 / −1

<details>
<summary>Resposta</summary>

**(b)**. Pedir emprestado é um peso negativo no ativo sem risco, e a soma continua a dar 1 (0,8 + 0,5 − 0,3).

</details>

**6.** Uma estratégia tem β = 0,5. O mercado sobe 10%. Tudo o resto constante, a estratégia:<br>(a) Sobe 10% · (b) Sobe 5% · (c) Sobe 20% · (d) Não se mexe

<details>
<summary>Resposta</summary>

**(b)**. β mede a exposição ao mercado: 0,5 × 10% = 5% (por exemplo, metade em ações e metade em cash).

</details>

**7.** O valor de uma estratégia ao longo do tempo é 100, 120, 90, 110, 80, 130. Qual é o maximum drawdown?<br>(a) 25% · (b) 33,3% · (c) 40% · (d) 50%

<details>
<summary>Resposta</summary>

**(b)**. O high water mark é 120 de t = 1 a t = 4. O pior ponto é 80: (120 − 80) / 120 = 33,3%. Em 130 o drawdown volta a 0 (novo pico).

</details>

**8.** Porque é que o alfa sozinho não chega para comparar duas estratégias?<br>(a) Porque é sempre zero · (b) Porque não diz com que risco foi obtido e duplica com 2× de alavancagem · (c) Porque só se calcula com quantstats · (d) Porque ignora o mercado

<details>
<summary>Resposta</summary>

**(b)**. Por isso usam-se rácios risco–retorno como o Sharpe e o information ratio, que não mudam com a alavancagem.

</details>

**9. (aberta)** Um colega entrega o código do PLTR (3.3 Practice) e diz "corre sem erros, está pronto". Explica o que está errado, que checks o teriam revelado, e propõe duas soluções diferentes.

<details>
<summary>Resposta</summary>

- **Problema:** a PLTR só tem dados desde set/2020. `dropna()` apaga todas as linhas com algum NaN, por isso a amostra das 4 ações começa em 2020 em vez de 2015. Não há erro, é uma falha silenciosa.
- **Checks que apanham:** `prices.shape` (muito menos que \~120 linhas) e o date range (começa em 2020).
- **Soluções:** (1) retirar a PLTR e manter 2015–2024; (2) aceitar a amostra comum 2020–2024 e dizê-lo explicitamente; (3) `dropna(how='all')` e tratar o histórico de cada ação separadamente.
- **Ponto-chave:** todas são aceitáveis desde que a escolha seja consciente e reportada.

</details>

**10. (aberta)** A IA escreveu `sharpe = df.mean(axis=1).mean() / df.mean(axis=1).std() * np.sqrt(12)`, com `df` = preços mensais. Encontra os 3 problemas e escreve a versão correta.

<details>
<summary>Resposta</summary>

1. Usa **preços** em vez de retornos: o Sharpe é definido sobre retornos.
2. A média de preços entre ações não é 1/n: pesa mais as ações com preço alto (price-weighted). O 1/n faz-se com `rets.mean(axis=1)`.
3. Falta subtrair a **taxa sem risco**.

```py
rets = np.log(df).diff(1).dropna()
ptf = rets.mean(axis=1)
sharpe = (12*ptf.mean() - rf) / (np.sqrt(12)*ptf.std())
```

</details>

**Refaz no notebook, sem olhar para as soluções:** Part 1 — 3.3 Practice (o bug) e 3.5 Homework. Part 2 — a discussão do beta (abaixo, perto ou acima de 1?), 3.6 Practice (a IA) e 3.7 Homework.
