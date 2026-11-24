# Lecture 5 — Event Studies e Monte Carlo

> Resumo exportado das notas em Notion (18/11/2026). Complementos dos notebooks, armadilhas e Testa-te acrescentados a 24/11/2026.

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

### Complementos do notebook (Lecture 5)

#### 5.1 π com dardos: precisão custa caro

- Com 1.000 pontos, a estimativa de π costuma errar já na **segunda casa decimal**.
- Cada **×100** pontos só reduz o erro **×10**: o erro do Monte Carlo cai com 1/√M. Para 10× mais precisão precisas de **100×** mais simulações.
- **Precisão ≠ exatidão.** A simulação converge muito bem para a resposta implícita nos pressupostos, estejam eles certos ou errados. Nenhum número de simulações corrige um modelo errado.

#### 5.2 Recessões com dados anuais (USREC, 1855–2025)

- O notebook lê o `USREC` diretamente como CSV do FRED (`fredgraph.csv`, frequência anual), sem chave de API.
- Com uma moeda independente por ano, as recessões aparecem isoladas. Na realidade aparecem **em blocos**: é isso que a cadeia de Markov acrescenta.
- A escolha entre moeda independente e cadeia de Markov é uma decisão de desenho da simulação que o trabalho de grupo tem de **declarar e justificar**.

#### 5.3 Simular a reforma

Investir **6.000 €/ano durante 40 anos**, com retornos anuais N(7%, 18%), 10.000 simulações.

```py
for i in range(n_sim):
    wealth = 0.0
    r = np.random.normal(mu, sigma, T)        # 40 retornos anuais
    for t in range(T):
        wealth = (wealth + contribution) * (1 + r[t])
    final_wealth[i] = wealth
```

- Com 7% certos todos os anos, a riqueza final é **≈ 1,28 M€**.
- A **média** das simulações fica perto desse valor. A **mediana** fica bem abaixo, e cerca de **dois terços** das vidas simuladas acabam abaixo de 1,28 M€.
- Porquê? A capitalização é **multiplicativa**, por isso a distribuição da riqueza final é assimétrica à direita: poucos caminhos espetaculares puxam a média para cima.
- O gráfico em leque (`fill_between` entre percentis 5–95 e 25–75) mostra o risco que o plano determinístico esconde.
- **Sequence-of-returns risk (trabalho de casa):** os mesmos retornos ordenados do pior para o melhor (`np.sort(r)`) dão **mais** riqueza a quem poupa, porque as quedas apanham o pote ainda pequeno. Para um reformado que **levanta** dinheiro é ao contrário: quedas no início são fatais.

#### 5.4 LBO simples: TascaCo

| Item | Valor |
| --- | --- |
| EBITDA hoje | 100 M€ |
| Preço | 9 × EBITDA = 900 M€ |
| Financiamento | 540 M€ de dívida a 8% + 360 M€ de capital próprio |
| Cash conversion | 60% do EBITDA vira FCF antes de juros; todo o FCF amortiza dívida (cash sweep) |
| Saída | ano 5, a 10 × EBITDA |
| Hurdle do fundo | 15% de IRR |

```py
for t in range(n_years):
    EBITDA = EBITDA * (1 + e_growth)
    fcf = cash_conversion*EBITDA - interest_rate*debt    # FCF depois de juros
    debt = max(debt - fcf, 0)                            # cash sweep
equity_exit = exit_multiple*EBITDA - debt
irr_base = (equity_exit / equity_in)**(1/n_years) - 1   # só há dois cash flows
```

- **Caso base (determinístico, 4% de crescimento):** IRR de **17,8%**, acima do hurdle.
- **Monte Carlo:** o crescimento do EBITDA depende do estado da economia (cadeia de Markov da 5.2): N(+8,2%, 8%) em boom, N(−6%, 8%) em recessão. O múltiplo de saída é N(10×, 1,5×), com mínimo de 5× (venda forçada).
- **O capital próprio não pode valer menos de zero:** `max(..., 0)`. Se o valor de saída não cobre a dívida, o IRR é −100% (wipeout).
- **Resultados:** a mediana do IRR fica quase em cima do caso base. Mas só cerca de **6 em cada 10** mundos batem o hurdle, cerca de **1 em 10** perde dinheiro e há uma pequena fatia de wipeouts, que no modelo determinístico nem existe.
- **Sem dívida** (900 M€ de capital, FCF acumula em caixa): mediana do IRR mais baixa, mas probabilidade de perder dinheiro muito menor.
- **Mensagem:** a alavancagem não cria valor, **estica a distribuição**. Melhora o meio e a direita, engorda e alonga a cauda esquerda.
- **Explore:** com 75% de dívida, a probabilidade de wipeout sobe cerca de dez vezes. Se o múltiplo de saída cai 2× quando o ano 5 é recessão, a cauda esquerda engorda: assumir um múltiplo **independente** da economia é discretamente otimista.

#### 5.5 "A IA escreveu, devo confiar?"

```py
monthly_rets = np.random.normal(mu_annual/12, sigma_annual/12, (n_sim, n_months))   # errado
monthly_rets = np.random.normal(mu_annual/12, sigma_annual/np.sqrt(12), (n_sim, n_months))  # certo
```

- A média escala com o tempo (/12), mas a **volatilidade escala com a raiz do tempo** (/√12). Volatilidade mensal = 18%/√12 ≈ 5,2%, não 1,5%.
- Com o bug, o mundo simulado é ~3,5 vezes calmo demais e a probabilidade de perder dinheiro em 10 anos sai quase zero. Corrigido, é **≈ 17%**, cerca de uma em seis.
- **Teste de plausibilidade:** se uma simulação diz que o risco é (quase) zero, o modelo está partido até prova em contrário.

#### Prática: avaliar um empréstimo privado (OID + PIK)

Contrato: *"5-year unitranche, 6% cash + 4% PIK, issued at 97"*.

- **Face value 100 M€**, mas o fundo só adiantou **97 M€** (3 pontos de **OID**, original issue discount).
- Todos os anos o devedor paga **6% do saldo em dinheiro**. Outros **4% não são pagos: somam-se ao saldo** (**PIK**, payment-in-kind), que por isso cresce.
- No ano 5 o devedor paga o saldo todo, já crescido: 100 × 1,04⁵.

```py
t = np.arange(1, maturity+1)
loan_balances = principal * (1+pik_rate)**(t - 1)        # saldo no início de cada ano
flows = np.zeros(maturity+1)
flows[0] = -principal*(1-OID)                            # o fundo paga 97
flows[1:] = cash_rate * loan_balances                    # juros em dinheiro sobre o saldo
flows[-1] += principal * (1+pik_rate)**maturity          # reembolso do saldo crescido
y = fsolve(lambda r: np.sum(flows / (1 + r)**times), 0.10)[0]     # yield prometida (IRR)
value = np.sum(flows[1:] / (1 + r_req)**times[1:])                # valor à taxa exigida
```

- **Taxa exigida** = yield do Treasury a 5 anos (FRED `GS5`, último valor) + spread de crédito de 4,5%.
- **Yield prometida ≈ 10,75%**, acima dos 10% de cupão total, por causa do OID (pagas 97 e recebes juros e capital sobre 100).
- Com o Treasury a 4,93%, a taxa exigida é 9,43% e o empréstimo vale **≈ 102,36**, contra os 97 pagos.
- **Promised ≠ realized:** a parte PIK só chega em dinheiro no fim, *se* chegar. Se o devedor falhar no ano 5, os juros PIK que o fundo contabilizou todos os anos valem zero.
- O valor depende da taxa do dia em que corres o notebook, porque o `GS5` vem do FRED.

### Ideias-chave das Lectures 3–5

1. **pandas** é o Excel do Python: Series (uma coluna) e DataFrames (tabelas), com `loc` para nomes e `iloc` para posições, filtros booleanos com `&` / `|`, `describe()` e `.plot()`.
2. **APIs** (FRED, yfinance, CoinGecko, requests) trazem os dados diretamente para o notebook.
3. Nos **portefólios**, os pesos somam 1 (ou 0 se self-financing). Manter pesos fixos obriga a rebalancear, e a 1/n é difícil de bater.
4. Para **avaliar uma estratégia**: beta (exposição ao mercado), alfa (valor acrescentado), Sharpe (retorno por risco total), Information ratio (alfa por risco idiossincrático) e drawdowns (pior perda desde o pico).
5. No **backtesting**, cuidado com look-ahead bias (usar `shift(1)` na posição), survivorship bias e custos de transação.
6. **Event studies:** retorno anormal = observado − normal. O CAR com intervalo de confiança diz se o evento teve efeito significativo.
7. **Monte Carlo:** simular muitas vezes e contar. A Lei dos Grandes Números garante a convergência. Escolhe a distribuição certa e usa cadeias de Markov quando há persistência.

### Armadilhas da Lecture 5

- **Janela de estimação a sobrepor o evento:** se a janela de estimação chega ao dia 0, o "retorno normal" já contém o efeito do evento. Por isso acaba no dia −11.
- **`axis=0` vs. `axis=1`:** a média de cada ação ao longo do tempo é `axis=0`; a média entre ações em cada dia é `axis=1`. Trocar dá números sem sentido.
- **A banda de confiança cresce com √horizonte**, não com o horizonte.
- **Retorno constante vs. modelo de mercado:** num evento que mexe com o mercado todo (eleições, COVID), o modelo de retorno constante atribui ao evento também o movimento do mercado. O modelo de mercado (alfa + beta × mercado) separa as duas coisas.
- **Sem `np.random.seed`**, cada execução dá números diferentes. Não é um bug, mas impede comparar resultados.
- **Erro do Monte Carlo ∝ 1/√M:** 10× mais precisão custa 100× mais simulações.
- **Precisão ≠ exatidão:** mais simulações não corrigem uma distribuição errada.
- **Volatilidade escala com √t:** σ mensal = σ anual / √12, nunca / 12.
- **Cada linha da matriz de transição soma 1.** `p_r_b = 1 − p_r_r`, não `1 − p_b_b`.
- **`shift(-1)` olha para o período seguinte.** Aqui é o que queremos (contar transições). Num backtest seria look-ahead bias.
- **Burn-in:** sem ele, todas as simulações começam em boom e os primeiros períodos ficam enviesados.
- **Média ≠ mediana** em riqueza capitalizada: a distribuição é assimétrica à direita, por isso o "resultado esperado" não é o resultado típico.
- **Capital próprio com responsabilidade limitada:** `max(valor − dívida, 0)`. Sem o `max`, o IRR de um wipeout fica mal definido.
- **Yield prometida ≠ retorno realizado** (OID e PIK): o PIK só se recebe no fim, se o devedor pagar.

### Números de referência da Lecture 5

| Item | Valor |
| --- | --- |
| Janela de estimação / evento (eleições EUA) | \[−100, −11\] (90 dias) / \[−10, +10\] (21 dias) |
| Intervalo de confiança de 95% | ±1,96 desvios padrão |
| Reforma: 6.000 €/ano, 40 anos, 7% certos | ≈ 1,28 M€ |
| Reforma simulada: P(abaixo de 1,28 M€) | cerca de dois terços |
| LBO TascaCo: IRR do caso base | 17,8% (hurdle 15%) |
| LBO simulado: P(bater o hurdle) / P(perder dinheiro) | ≈ 6 em 10 / ≈ 1 em 10 |
| Volatilidade mensal com 18% anual | 18% / √12 ≈ 5,2% |
| P(perder dinheiro em 10 anos), N(7%, 18%) | ≈ 17% |
| Empréstimo 6% cash + 4% PIK a 97: yield prometida | ≈ 10,75% |

### Testa-te: Lecture 5

**1.** Porque é que a janela de estimação acaba no dia −11 e não no dia −1?<br>(a) Para ter exatamente 90 dias · (b) Para não ser contaminada pelo evento, nem por fugas de informação antes dele · (c) Porque o yfinance não tem dados recentes · (d) Para a banda de confiança ser mais estreita

<details>
<summary>Resposta</summary>

**(b)**. A janela do evento começa no dia −10 precisamente para apanhar fugas de informação. Se a estimação incluísse esses dias, o "retorno normal" já teria parte do efeito.

</details>

**2.** O CAR médio dos "vencedores" sobe 4% no dia 0, mas a banda de 95% ainda inclui o zero. O que concluis?<br>(a) O evento teve um efeito significativo · (b) Não há evidência estatística suficiente de efeito · (c) O evento teve efeito negativo · (d) O modelo está errado

<details>
<summary>Resposta</summary>

**(b)**. O efeito estimado é positivo, mas com a dispersão entre ações não se consegue excluir zero a 95%.

</details>

**3.** Com 10.000 simulações o erro de uma estimativa é 0,02. Quantas precisas para um erro de 0,002?<br>(a) 100.000 · (b) 1.000.000 · (c) 20.000 · (d) 10.000.000

<details>
<summary>Resposta</summary>

**(b)**. O erro cai com 1/√M: 10× menos erro exige 100× mais simulações.

</details>

**4.** Num ano de recessão, a probabilidade de o ano seguinte também ser recessão é 0,3. A probabilidade de passar de boom a recessão é 0,1. Qual é a matriz de transição (estado 0 = boom, 1 = recessão)?<br>(a) \[\[0,9; 0,1\]; \[0,7; 0,3\]\] · (b) \[\[0,1; 0,9\]; \[0,3; 0,7\]\] · (c) \[\[0,9; 0,3\]; \[0,1; 0,7\]\] · (d) \[\[0,7; 0,3\]; \[0,9; 0,1\]\]

<details>
<summary>Resposta</summary>

**(a)**. A linha i é o estado atual e cada linha soma 1: de boom, 0,9 fica e 0,1 vai para recessão; de recessão, 0,7 volta a boom e 0,3 fica.

</details>

**5.** Na simulação da reforma, porque é que a mediana da riqueza final fica bem abaixo da média?<br>(a) Por causa da semente · (b) Porque a capitalização é multiplicativa e a distribuição é assimétrica à direita · (c) Porque os retornos são uniformes · (d) Porque há poucas simulações

<details>
<summary>Resposta</summary>

**(b)**. Poucos caminhos com retornos espetaculares puxam a média para cima; o poupador típico (a mediana) fica abaixo.

</details>

**6.** Um código simula retornos mensais com `np.random.normal(0.07/12, 0.18/12, ...)`. O que está mal?<br>(a) Nada · (b) A média devia ser 0,07/√12 · (c) A volatilidade devia ser 0,18/√12 · (d) Devia usar a t de Student

<details>
<summary>Resposta</summary>

**(c)**. A variância escala com o tempo, logo o desvio padrão escala com √t. Com /12 o mundo simulado é ~3,5 vezes calmo demais.

</details>

**7.** Um empréstimo de face 100 é emitido a 97, com 6% em dinheiro e 4% PIK durante 5 anos. A yield prometida é:<br>(a) 6% · (b) 10% · (c) acima de 10% · (d) abaixo de 10%

<details>
<summary>Resposta</summary>

**(c)**. ≈ 10,75%. O cupão total é 10% sobre um saldo que começa em 100, mas o fundo só pagou 97: o OID acrescenta yield.

</details>

**8. (aberta)** No LBO, a versão alavancada tem uma mediana de IRR mais alta do que a versão sem dívida. Então a dívida cria valor?

<details>
<summary>Resposta</summary>

Não. A empresa e os mundos simulados são os mesmos; só muda o financiamento. A dívida **estica a distribuição**: mais IRR no meio e à direita, mas uma cauda esquerda mais longa (mais probabilidade de perder dinheiro e wipeouts que sem dívida não existem). A mediana mais alta é a compensação por esse risco, não valor criado.

</details>

**9. (aberta)** Porque é que um múltiplo de saída independente do estado da economia é um pressuposto otimista?

<details>
<summary>Resposta</summary>

Na realidade, operações fracas e preços de saída baixos chegam juntos: em recessão o EBITDA cai **e** os compradores pagam múltiplos mais baixos, e muitas vezes o fundo é obrigado a vender. Tratá-los como independentes faz com que os maus anos sejam muitas vezes "salvos" por um bom múltiplo, o que encolhe a cauda esquerda.

</details>

**Refaz no notebook, sem olhar para as soluções:** 5.1 Practice (π 10.000 vezes), o trabalho de casa da sequência de retornos, os dois Explore do LBO, o bug da IA (5.5) e o empréstimo privado (explica cada linha de código).
