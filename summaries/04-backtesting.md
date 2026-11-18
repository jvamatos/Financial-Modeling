# Lecture 4 — Backtesting

> Resumo exportado das notas em Notion (18/11/2026). As respostas das perguntas *Testa-te* estão escondidas: clica em **Resposta** para as ver.

## Lecture 4: Backtesting

**Backtesting** é testar como uma estratégia de trading ou de investimento se teria comportado no passado, com dados históricos.

- Os hedge funds testam primeiro os **retornos brutos**: a ideia tem mérito?
- Se tiver, verificam se **sobrevive aos custos de transação** e se acrescenta valor ao investidor (retornos líquidos).
- Um backtest deve reproduzir fielmente como os mercados funcionam: como as ordens são executadas e que tipos de ordens existem.

### Enviesamentos e cuidados a ter

- **Look-ahead bias:** usar informação que ainda não era conhecida na altura. Exemplos: contas corrigidas depois de publicadas, stock splits.
- **Survivorship bias:** testar só com empresas que ainda existem hoje. Ficam de fora as que faliram, saíram de bolsa ou foram compradas, que em geral correram mal, e o resultado fica inflacionado.
- **Outliers:** distinguir os valores extremos que não são representativos dos que fazem parte do comportamento normal do mercado.
- **Período representativo:** a amostra deve refletir o regime de mercado atual e futuro (volatilidade, número de eventos extremos, volume de dados).
- **Objetivos e restrições ao longo do tempo:** uma estratégia pode acabar bem mas ter tido perdas ou volatilidade inaceitáveis pelo caminho. Usar métricas rolantes, como o Sharpe rolante.
- **Ambiente de trading realista:** custos de transação, **slippage** (diferença entre o preço esperado e o preço executado), contraparte para vendas a descoberto, comissões de corretagem, e o facto de nem sempre ser possível executar ao preço-alvo.

### Backtest vetorizado com pandas: estratégia de média móvel

**Regras:**

- Entrar **long** quando o preço de fecho está **acima da média móvel simples (SMA) de 20 dias**.
- Sair quando o preço cai abaixo da SMA de 20 dias.
- Sem vendas a descoberto.

A estratégia não depende de quantas ações compras, porque só interessam as variações percentuais. Ativo: Apple (AAPL), 2017–2024.

```py
import numpy as np, pandas as pd, matplotlib.pyplot as plt, yfinance as yf

# 1. Preços diários
data = yf.download('AAPL', start='2017-01-01', end='2025-01-01',
                   interval='1d', progress=False, auto_adjust=True)
df = data['Close'].copy()

# 2. Log-retornos e SMA de 20 dias
df.loc[:, 'log_rtn'] = np.log(df['AAPL']).diff(1)
df.loc[:, 'sma_20'] = df['AAPL'].rolling(window=20).mean()
df.dropna(inplace=True)          # remove os primeiros 20 dias (sem SMA)

# 3. Indicador de posição: 1 = investido, 0 = fora
df.loc[:, 'position'] = 0
long_position = df.AAPL > df.sma_20
df.loc[long_position, 'position'] = 1

# 4. Quantas vezes entrámos? (ontem 0, hoje 1)
np.sum((df['position'] == 1) & (df['position'].shift(1) == 0))

# 5. Retornos da estratégia vs. buy-and-hold
df.loc[:, 'strategy_rtn'] = df['position'].shift(1) * df['log_rtn']
df.loc[:, 'strategy_rtn_cum'] = df['strategy_rtn'].cumsum().apply(np.exp)
df.loc[:, 'bh_rtn_cum'] = df['log_rtn'].cumsum().apply(np.exp)
df[["bh_rtn_cum", "strategy_rtn_cum"]].plot(title="Cumulative returns")

# 6. Custos de transação (0,5% por cada mudança de posição)
transaction_cost = 0.005
df.loc[:, 'tc'] = df['position'].diff(1).abs() * transaction_cost
df.loc[:, 'strategy_rtn_cum_tc'] = (df['strategy_rtn'] - df['tc']).cumsum().apply(np.exp)
```

**Explicações:**

- **`.rolling(20).mean()`** é a média dos últimos 20 dias, recalculada em cada dia.
- **`position.shift(1)`** é o passo **mais importante**. Só ganhas o retorno de hoje se **ontem** já estavas posicionado. Usar a posição de hoje seria **look-ahead bias**, porque a decisão de hoje usa o preço de fecho de hoje, que só se conhece no fim do dia.
- **`.cumsum().apply(np.exp)`:** os log-retornos somam-se, e a exponencial converte a soma em crescimento acumulado (1,0 = valor inicial).
- **`position.diff(1).abs()`** vale 1 sempre que entras ou sais, e 0 se nada muda. Multiplicado por 0,5% dá o custo de cada transação.
- **Gráfico de 2024:** `plt.subplots(2, sharex=True)` com o preço e a SMA em cima (`ax[0]`) e a posição 0/1 em baixo (`ax[1]`).
- **Conclusão típica:** uma estratégia que parece boa em bruto pode perder para o buy-and-hold depois dos custos, porque muda de posição muitas vezes.

### Complementos do notebook (Lecture 4)

#### 4.1 "Uma estratégia que nos vai deixar ricos?" (o backtest com look-ahead bias)

O notebook começa com o mesmo backtest SMA-20 na Apple, mas com esta linha:

```py
df['strategy_rtn'] = df['position'] * df['log_rtn']          # ERRADO: sem shift
df['strategy_rtn'] = df['position'].shift(1) * df['log_rtn'] # CERTO
```

- O sinal do dia t precisa do **fecho do dia t**. O primeiro retorno que podes ganhar é o de t+1.
- A versão errada dá à estratégia o retorno do próprio dia que *gerou* o sinal. Como o dia em que o preço cruza acima da média é tipicamente um dia de subida forte, o backtest "colhe" exatamente esses dias e o resultado parece fantástico.
- **Que lag usar?** `lag = 0`: impossível (look-ahead bias). `lag = 1`: assume que transacionas ao fecho que usaste para o sinal (market-on-close, ligeiramente otimista). `lag = 2`: executas no dia seguinte, totalmente seguro.

#### 4.2 Practice

1. **SMA de 100 dias em vez de 20:** mudar `window=100` (a janela de NaN passa a 100 linhas). Menos cruzamentos, logo menos transações.
2. **Versão long-short:** só muda a atribuição da posição, com `df.loc[df.AAPL < df.sma_20, 'position'] = -1`. Está sempre no mercado, por isso também perde em tendências de queda quando o sinal falha (ver 2022).

#### 4.3 Custos de transação e o custo de breakeven

- A estratégia SMA-20 faz **mais de 150 transações**. Cada uma paga o **bid-ask spread**, eventualmente comissão e, para grandes investidores, **price impact** (a tua própria compra mexe o preço).
- 0,5% por mudança de posição é um valor conservador para um investidor de retalho numa ação líquida.
- **Breakeven:** o custo a partir do qual a estratégia deixa de bater o buy-and-hold.

```py
for c in np.arange(0, 0.0015, 0.0001):
    tc = df['position'].diff(1).abs() * c
    final = (df['strategy_rtn'] - tc).cumsum().apply(np.exp).iloc[-1]
    print(f"cost {c:.5f}: strategy {final:.2f}x vs buy-and-hold {df['bh_rtn_cum'].iloc[-1]:.2f}x")
```

O valor exato depende da amostra, mas a lição não: **turnover é um imposto sobre o sinal**. No group assignment, reporta o turnover e mostra o resultado líquido de custos.

#### Um pressuposto escondido: o 60/40

```py
ptf_60_40 = 0.6 * r_SPY + 0.4 * r_TBIL     # todos os dias
```

Manter os pesos **exatamente em 60/40 todos os dias** significa **rebalancear diariamente**: quando as ações sobem, um buy-and-hold ficaria acima de 60% em ações. A fórmula inocente esconde uma estratégia de trading diário sem custos.

#### 4.4 "A IA escreveu, devo confiar?" (momentum)

Pedido: *"cada mês, ter a ação com melhor retorno nos 12 meses anteriores, entre AAPL, NVDA, MSFT e AMZN; reportar o Sharpe anualizado."*

```py
momentum = prices.pct_change(12).dropna()
best = momentum.idxmax(axis=1)                                   # vencedora deste mês
strat_rets = pd.Series([rets.loc[m, best[m]] for m in best.index], index=best.index)
sharpe = strat_rets.mean() / strat_rets.std() * 12               # anualização
```

- **Bug 1, look-ahead bias (o maior):** escolhe a vencedora com o retorno a 12 meses que *inclui este mês* e depois ganha o retorno deste mesmo mês. Correção: `best = momentum.shift(1).idxmax(axis=1)`.
- **Bug 2, anualização errada:** ×12 em vez de ×√12. O Sharpe fica inflacionado por um fator de √12.
- **Bug 3, sem taxa sem risco:** usa retornos brutos e não excess returns.
- **O problema mais profundo, survivorship na própria pergunta:** AAPL, NVDA, MSFT e AMZN foram escolhidas *hoje* porque ganharam. A estratégia está contaminada antes de escrever uma linha de código, e nenhum assistente corrige isto por ti.

#### 4.5 Practice: SMA crossover (golden cross / death cross)

**Comprar** quando a SMA de 50 dias cruza acima da SMA de 200 dias (*golden cross*); **vender** quando cruza abaixo (*death cross*). NVIDIA, 2017–2024.

```py
df['sma_50'] = df['NVDA'].rolling(window=50).mean()
df['sma_200'] = df['NVDA'].rolling(window=200).mean()
df.dropna(inplace=True)
df['position'] = 0
df.loc[df.sma_50 > df.sma_200, 'position'] = 1
df['strategy_rtn'] = df['position'].shift(1) * df['log_rtn']
```

**Formas de o backtest ainda estar a mentir** (mesmo com o shift certo):

1. **Amostra não representativa:** um só ativo num só período. NVDA 2017–2024 é uma subida extraordinária; noutra ação ou década a regra pode falhar.
2. **Seleção / survivorship:** escolher a NVDA *porque* subiu.
3. **Data snooping coletivo:** 50/200 são os parâmetros mais famosos da análise técnica precisamente porque milhares de pessoas os procuraram nos mesmos dados históricos.
4. **Execução:** o cruzamento é detetado ao fecho; numa ação volátil, a abertura seguinte pode ficar longe do preço do backtest.

### Armadilhas da Lecture 4

- **Sem `shift(1)` = look-ahead bias.** A posição decidida com o fecho de hoje só ganha o retorno de amanhã.
- **O mesmo erro em sinais mensais:** num ranking de momentum, desfasar o sinal (`momentum.shift(1)`).
- **Survivorship bias** pode estar na própria escolha do universo (ações escolhidas hoje porque ganharam).
- **Retorno bruto ≠ retorno líquido:** com muitas transações, os custos podem apagar toda a vantagem.
- **`position.diff(1).abs()`** conta mudanças de posição: entrar e sair são **duas** transações (0 → 1 → 0 custa 2 × 0,5% = 1%). Na versão long-short, passar de +1 para −1 conta 2.
- **Log-retornos acumulam com `cumsum()` e `exp`**; retornos simples acumulam com `(1 + r).cumprod()`. Não misturar.
- **Sharpe anualizado:** ×√12 (mensal) ou ×√252 (diário), nunca ×12, e com excess returns.
- **`rolling(20)` deixa 19 NaN no início** (o NaN do `diff`, na linha 0, é um deles): por isso o `dropna`. Com SMA de 200, perdes \~200 dias.
- **Pesos fixos todos os dias = rebalanceamento diário** (o caso 60/40), que também teria custos.
- **Long-short está sempre no mercado**: também perde quando o sinal falha em tendências de queda.
- **Parâmetros famosos (50/200)** já foram otimizados por muita gente nos mesmos dados: data snooping.

### Números de referência da Lecture 4

| Item | Valor |
| --- | --- |
| SMA-20 na AAPL, 2017–2024 | mais de 150 transações |
| Custo por mudança de posição (retalho, conservador) | 0,5% |
| Grelha para o breakeven | `np.arange(0, 0.0015, 0.0001)` (0% a 0,14%) |
| Dias de bolsa por ano | 252 (anualizar com √252 ≈ 15,9) |
| Sharpe com ×12 em vez de ×√12 | inflacionado √12 ≈ 3,46 vezes |

Os resultados do backtest (múltiplos finais do buy-and-hold, bruto e líquido) dependem dos dados do Yahoo. Corre o notebook no Colab e anota-os aqui.

### Testa-te: Lecture 4

**1.** Porque é que o backtest usa `df['position'].shift(1) * df['log_rtn']`?<br>(a) Para os retornos ficarem anuais · (b) Porque a posição decidida com o fecho de hoje só pode ganhar o retorno de amanhã · (c) Para remover os NaN · (d) Para incluir os custos de transação

<details>
<summary>Resposta</summary>

**(b)**. Sem o shift, a estratégia ganha o retorno do próprio dia que gerou o sinal: look-ahead bias.

</details>

**2.** O que calcula `np.sum((df['position'] == 1) & (df['position'].shift(1) == 0))`?<br>(a) O número de dias investido · (b) O número de vezes que a estratégia **entra** numa posição long · (c) O número total de transações · (d) O retorno acumulado

<details>
<summary>Resposta</summary>

**(b)**. Dias em que hoje está investido e ontem não estava, ou seja, compras. As saídas são mais ou menos o mesmo número, por isso o total de transações é cerca do dobro.

</details>

**3.** Com `tc = df['position'].diff(1).abs() * 0.005`, quanto custa entrar numa posição e sair dela mais tarde?<br>(a) 0,5% · (b) 1% · (c) 0% · (d) 5%

<details>
<summary>Resposta</summary>

**(b)**. São duas mudanças de posição (0 → 1 e 1 → 0), cada uma com `abs(diff) = 1`, logo 2 × 0,5% = 1%.

</details>

**4.** Um código calcula `sharpe = r.mean() / r.std() * 12` com retornos mensais. O que está mal?<br>(a) Nada · (b) Devia ser ×√12 e usar excess returns · (c) Devia ser ×252 · (d) Devia dividir por 12

<details>
<summary>Resposta</summary>

**(b)**. O Sharpe escala com √12 (média ×12, desvio padrão ×√12), e o numerador deve ser o excess return (r − R\_f).

</details>

**5.** Backtestas uma estratégia de momentum só com AAPL, NVDA, MSFT e AMZN, escolhidas hoje. Que enviesamento está presente mesmo que o código esteja perfeito?<br>(a) Look-ahead bias no código · (b) Survivorship / seleção: o universo foi escolhido porque ganhou · (c) Outliers · (d) Nenhum

<details>
<summary>Resposta</summary>

**(b)**. A escolha do universo já contém hindsight. A IA responde à pergunta feita; a pergunta é que está contaminada.

</details>

**6.** O retorno diário de um portefólio é calculado como `0.6 * r_SPY + 0.4 * r_TBIL` todos os dias. Isto assume:<br>(a) Buy-and-hold · (b) Rebalanceamento diário para 60/40 · (c) Rebalanceamento anual · (d) Sem ações

<details>
<summary>Resposta</summary>

**(b)**. Manter os pesos exatamente fixos exige vender o que subiu e comprar o que desceu todos os dias, sem custos.

</details>

**7. (aberta)** Porque é que o backtest com look-ahead bias (sem `shift`) parece tão bom numa estratégia de média móvel?

<details>
<summary>Resposta</summary>

O dia em que o preço cruza acima da média é, tipicamente, um dia de subida forte: o cruzamento e a subida são o mesmo evento. Sem o `shift`, o backtest dá à estratégia exatamente esses retornos, que na realidade só conhecerias depois do fecho. É informação do futuro.

</details>

**8. (aberta)** Fizeste o backtest do SMA crossover 50/200 na NVDA, 2017–2024, com o `shift(1)` certo e custos de 0,5%. Dá três razões pelas quais o resultado ainda pode estar a mentir.

<details>
<summary>Resposta</summary>

1. **Amostra não representativa:** um ativo e um período (uma subida excecional).
2. **Seleção / survivorship:** a NVDA foi escolhida porque subiu.
3. **Data snooping:** os parâmetros 50/200 ficaram famosos por terem sido procurados por muita gente nos mesmos dados.
4. (Bónus) **Execução:** o sinal é ao fecho e a execução real na abertura seguinte pode ter um gap grande.

</details>

**Refaz no notebook, sem olhar para as soluções:** 4.1 (encontra o bug antes de abrir a solução), 4.2 Practice (SMA 100 ou long-short), 4.3 breakeven, 4.4 a IA (3 bugs + o problema da pergunta) e 4.5 SMA crossover completo.
