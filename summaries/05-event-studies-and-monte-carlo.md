# Lecture 5 — Event Studies e Monte Carlo

> Resumo exportado das notas em Notion (18/11/2026).

## Lecture 5: Event Studies

### A ideia

- O event study é provavelmente o desenho de modelação mais antigo e simples. Num certo momento acontece um evento (um "tratamento"), e **o que muda entre antes e depois é o efeito desse evento**.
- Em finanças, serve para perceber se um evento no mercado ou na vida de uma empresa afetou o preço das ações.
- **Eventos corporativos:** IPO, aumentos de capital (SEO), fusões e aquisições, emissão de dívida.
- **Eventos de mercado:** anúncios de taxas de juro, COVID, crises financeiras, eleições presidenciais.
- Muitas superstições são event studies mal feitos: "usei as calças verdes e a minha equipa ganhou". Sem um termo de comparação, não se separa o efeito do evento do que teria acontecido de qualquer forma.

### Desenho de um event study

1. Definir o evento.
2. Critérios de seleção (que empresas entram).
3. Medir retornos normais e anormais.
4. Procedimento de estimação.
5. Procedimento de teste.
6. Resultados empíricos.
7. Interpretação.

**Linha temporal**

- **Janela de estimação** \[T\_0, T\_1\]: período antes do evento usado para estimar o comportamento "normal" da ação.
- **Janela do evento** \[T\_1+1, T\_2\]: começa uns dias **antes** do evento, para detetar fugas de informação.
- **Dia 0:** data do evento. Por exemplo, o anúncio de uma fusão ou de uma reexpressão de contas.
- **Janela pós-evento** \[T\_2+1, T\_3\]: desempenho depois do anúncio.

**Conceitos-chave**

- **Retorno anormal:** AR\_t = retorno observado − retorno normal (esperado sem o evento).
- **Retorno anormal acumulado:** CAR = soma dos AR ao longo da janela do evento.
- **Modelo de retorno constante:** o retorno "normal" é simplesmente a média da janela de estimação. Alternativas mais ricas usam o modelo de mercado, com alfa e beta.

### Exemplo: eleições nos EUA (5 nov. 2024, evento a 6 nov.)

- **"Vencedores" esperados:** bancos e private equity (JPM, MS, C, BAC, GS, WFC, BX, KKR), que beneficiam de desregulação.
- **"Perdedores" esperados:** energia limpa, infraestruturas e consumo (FSLR, NEE, AMT, CCI, IRM, SWK, PEP, FE, MDLZ).

```py
import numpy as np, matplotlib.pyplot as plt, pandas as pd, yfinance as yf, datetime as dt

winner_stocks = ['JPM','MS','C','BAC','GS','WFC','BX','KKR']
loser_stocks  = ['FSLR','NEE','AMT','CCI','IRM','SWK','PEP','FE','MDLZ']
df_winners = yf.download(winner_stocks, start="2024-01-01", end="2025-01-01",
                         auto_adjust=True, progress=False)['Close']
df_losers  = yf.download(loser_stocks,  start="2024-01-01", end="2025-01-01",
                         auto_adjust=True, progress=False)['Close']
df_winners = df_winners.apply(np.log).diff(1)     # log-retornos diários
df_losers  = df_losers.apply(np.log).diff(1)

estimation_window = [-100, -11]     # 100 a 11 dias antes do evento
event_window      = [-10, 10]       # 10 dias antes até 10 dias depois
event_date = dt.datetime(2024, 11, 6)

event_date_index = df_winners.index.tz_localize(None).get_loc(event_date)   # posição do dia 0
est_window_index   = range(event_date_index + estimation_window[0], event_date_index + estimation_window[1] + 1)
event_window_index = range(event_date_index + event_window[0],      event_date_index + event_window[1] + 1)

# Modelo de retorno constante: retorno normal = média na janela de estimação
mu_winners = np.mean(df_winners.iloc[est_window_index, :], axis=0)
mu_losers  = np.mean(df_losers.iloc[est_window_index, :], axis=0)

# Retornos anormais na janela do evento
df_w_event_window = df_winners.iloc[event_window_index, :] - mu_winners
df_l_event_window = df_losers.iloc[event_window_index, :] - mu_losers

# Desvio padrão entre ações em cada dia (dispersão cross-sectional)
std_w = df_w_event_window.std(axis=1)
std_l = df_l_event_window.std(axis=1)
horizon = np.arange(1, len(std_w) + 1)

# CAR médio e intervalo de confiança de 95%
CAR_w = np.mean(df_w_event_window.cumsum(), axis=1)
CAR_w_up  = CAR_w + 1.96*std_w*np.sqrt(horizon)
CAR_w_low = CAR_w - 1.96*std_w*np.sqrt(horizon)
CAR_l = np.mean(df_l_event_window.cumsum(), axis=1)
CAR_l_up  = CAR_l + 1.96*std_l*np.sqrt(horizon)
CAR_l_low = CAR_l - 1.96*std_l*np.sqrt(horizon)

event_timeline = df_winners.index[event_window_index]
plt.plot(event_timeline, CAR_w, event_timeline, CAR_l)
plt.fill_between(event_timeline, CAR_w_up, CAR_w_low, alpha=0.2)   # banda de confiança sombreada
plt.fill_between(event_timeline, CAR_l_up, CAR_l_low, alpha=0.2)
plt.plot([event_date, event_date], plt.ylim(), '--k')             # linha vertical no dia do evento
plt.xticks(rotation=45)
plt.legend(['Winners', 'Losers'])
```

**Explicações:**

- **`get_loc`** devolve a posição (número da linha) de uma data no índice. Assim as janelas definem-se em dias de negociação relativos ao evento.
- A janela de estimação **acaba 11 dias antes** do evento para não ser contaminada por ele.
- **`axis=0`** calcula a média de cada ação ao longo do tempo. **`axis=1`** calcula, em cada dia, entre ações.
- **`.cumsum()`** acumula os retornos anormais, o que dá o CAR de cada ação. A média entre ações dá o CAR do grupo.
- **Intervalo de confiança:** ±1,96 desvios padrão dá 95%. O √horizonte entra porque a variância de uma soma de retornos independentes cresce com o número de dias.
- **Como ler o gráfico:** se o CAR dos vencedores salta para cima no dia 0 e a banda de confiança não inclui zero, o evento teve um efeito positivo **estatisticamente significativo**. O mesmo, ao contrário, para os perdedores.


## Lecture 5: Simulação Monte Carlo

### Origem e ideia

- **Stanisław Ulam**, físico do Projeto Manhattan, perguntou-se, enquanto recuperava de uma cirurgia, qual seria a probabilidade de ganhar um jogo de paciência. Calcular isso com combinatória era muito difícil.
- A ideia dele foi **jogar muitas vezes e contar quantas se ganham**. Como isso levaria anos à mão, ele e von Neumann programaram a simulação no **ENIAC**.
- **Monte Carlo** é estimar uma quantidade desconhecida **gerando amostras aleatórias** e usando inferência estatística.

Para estimar a probabilidade P\[E\] de um evento E:

1. Gerar M réplicas aleatórias X\_1, …, X\_M.
2. Contar quantas vezes o evento acontece.
3. Estimar:

$$
\hat{P}[E] = \frac{1}{M}\sum_{i=1}^{M} \mathbb{1}_{X_i \in S}
$$

A **função indicadora** 𝟙 vale 1 se o evento ocorre e 0 caso contrário. Ou seja, a probabilidade estimada é a **proporção de vezes** em que o evento aconteceu.

### Exemplo: estimar π

- Um quarto de círculo de raio 1 tem área π/4 e cabe num quadrado unitário (área 1).
- "Disparam-se" pontos aleatórios (x, y) com 0 ≤ x, y ≤ 1. Um ponto está dentro do círculo se x² + y² ≤ 1.
- P(dentro) = área do quarto de círculo / área do quadrado = π/4. Logo:

$$
\pi \approx 4 \times \frac{\text{pontos dentro do círculo}}{\text{total de pontos}}
$$

```py
np.random.seed(17)     # semente → os mesmos números aleatórios em cada execução (reprodutível)

def compute_pi(N_points):
    x = np.random.random(size=N_points)        # uniformes entre 0 e 1
    y = np.random.random(size=N_points)
    N_circle = np.sum(x**2 + y**2 <= 1)        # True conta como 1
    return 4 * N_circle / N_points

compute_pi(5001)

# Visualizar
N_points = 10000
x = np.random.random(size=N_points); y = np.random.random(size=N_points)
in_circle = x**2 + y**2 <= 1
plt.scatter(x[in_circle], y[in_circle])           # pontos dentro
plt.scatter(x[~in_circle], y[~in_circle])         # pontos fora (~ = "não")
x_c = np.linspace(0, 1, 150)
plt.plot(x_c, np.sqrt(1 - x_c**2), 'k')           # arco do círculo
```

### Lei dos Grandes Números

Em ensaios independentes repetidos com a mesma probabilidade p, a fração de sucessos **converge para p** quando o número de ensaios tende para infinito. É isto que garante que o Monte Carlo funciona: mais simulações dão estimativas mais precisas. O erro diminui ao ritmo de 1/√M.

### Distribuições de probabilidade para simular

- **Uniforme:** quando só sabes o intervalo possível. Todos os valores no intervalo são igualmente prováveis.

```py
CFs = np.random.uniform(100, 200, size=500)   # 500 cash flows entre 100 e 200
plt.hist(CFs)
```

- **Bernoulli / Binomial:** a Bernoulli tem um só ensaio, com X = 1 com probabilidade p e X = 0 com probabilidade 1−p. A binomial soma N Bernoullis.

```py
p_recession = np.sum(data['USREC']) / data.shape[0]   # % de meses em recessão nos EUA (dados FRED)
x = np.random.binomial(n=1, p=p_recession, size=100)  # simula 100 meses: recessão (1) ou não (0)
x.mean()                                              # ≈ p_recession
```

- **Normal:** `np.random.normal(loc=média, scale=desvio_padrão)`. Usa-se para modelar retornos de ações.
- **t de Student:** `np.random.standard_t(df)`. Tem **caudas mais pesadas** (mais eventos extremos), por isso é mais realista para retornos.
- **Poisson:** modela a **chegada de eventos extremos** (quantos ocorrem num período).

### Cadeias de Markov

- **"Para onde vais a seguir depende só de onde estás agora."**
- São definidas por N estados e por uma **matriz de transição** P, em que P\_ij é a probabilidade de passar do estado i para o estado j.
- São úteis para simular o estado da economia, por exemplo expansão (boom) vs. recessão.
- **Limitação:** a simulação de Bernoulli acima trata cada mês como independente. Na realidade as recessões são **persistentes**: se estás em recessão este mês, é provável que continues no próximo. A cadeia de Markov capta isso.

```py
# Probabilidades condicionais estimadas com os dados (shift(-1) = mês seguinte)
p_r_r = np.sum((data['USREC'] == 1) & (data['USREC'].shift(-1) == 1)) / np.sum(data['USREC'] == 1)
p_r_b = 1 - p_r_r          # recessão → boom
p_b_b = np.sum((data['USREC'] == 0) & (data['USREC'].shift(-1) == 0)) / np.sum(data['USREC'] == 0)
p_b_r = 1 - p_b_b          # boom → recessão

def model_economy_states(transition_matrix, T):
    N = transition_matrix.shape[0]
    states = range(N)                      # 0 = boom, 1 = recessão
    T_start = 100                          # período de "burn-in" (aquecimento)
    T_all = T + T_start
    economy_state = np.zeros(T_all).astype(int)    # começa em boom
    for t in range(1, T_all):
        economy_state[t] = np.random.choice(states, size=1,
                               p=transition_matrix[economy_state[t-1], :])[0]
    return economy_state[T_start:]         # descarta o burn-in

transition_matrix = np.array([[p_b_b, p_b_r],
                              [p_r_b, p_r_r]])
economy_states = model_economy_states(transition_matrix, T=100)
plt.plot(economy_states)
```

**Explicações:**

- **`p_r_r`** é a probabilidade de continuar em recessão no mês seguinte, dado que se está em recessão. Conta-se os meses com recessão hoje e amanhã e divide-se pelo total de meses em recessão.
- Cada linha da matriz de transição soma 1 (de cada estado tens de ir para algum lado).
- **`np.random.choice(states, p=...)`** sorteia o próximo estado usando a linha da matriz correspondente ao estado atual.
- **Burn-in:** simulam-se 100 períodos extra no início e deitam-se fora, para que o resultado não dependa do estado inicial arbitrário (começar em boom).
- O gráfico mostra **blocos** de recessão e de expansão, em vez de meses isolados aleatórios, o que é mais parecido com a realidade.

### Ideias-chave das Lectures 3–5

1. **pandas** é o Excel do Python: Series (uma coluna) e DataFrames (tabelas), com `loc` para nomes e `iloc` para posições, filtros booleanos com `&` / `|`, `describe()` e `.plot()`.
2. **APIs** (FRED, yfinance, CoinGecko, requests) trazem os dados diretamente para o notebook.
3. Nos **portefólios**, os pesos somam 1 (ou 0 se self-financing). Manter pesos fixos obriga a rebalancear, e a 1/n é difícil de bater.
4. Para **avaliar uma estratégia**: beta (exposição ao mercado), alfa (valor acrescentado), Sharpe (retorno por risco total), Information ratio (alfa por risco idiossincrático) e drawdowns (pior perda desde o pico).
5. No **backtesting**, cuidado com look-ahead bias (usar `shift(1)` na posição), survivorship bias e custos de transação.
6. **Event studies:** retorno anormal = observado − normal. O CAR com intervalo de confiança diz se o evento teve efeito significativo.
7. **Monte Carlo:** simular muitas vezes e contar. A Lei dos Grandes Números garante a convergência. Escolhe a distribuição certa e usa cadeias de Markov quando há persistência.
