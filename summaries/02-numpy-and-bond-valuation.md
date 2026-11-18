# Lecture 2 — NumPy e Bond Valuation

> Resumo exportado das notas em Notion (18/11/2026). As respostas das perguntas *Testa-te* estão escondidas: clica em **Resposta** para as ver.

## Lecture 2 (Part 1): Data Structures and NumPy

Os tipos de dados parecem o tema mais aborrecido da programação, mas é aí que acontecem os erros mais **caros**: comparar floats com `==`, multiplicar uma lista quando se queria um array, um slice que altera os dados originais sem avisar. O notebook é uma sequência de pequenas previsões. Antes de correr cada célula, tenta adivinhar o resultado.

### 2.1 Números, booleanos e strings

#### int vs. float

```py
maturity = 10       # int
maturity = 10.0     # float
type(5/4)           # float: a divisão / devolve SEMPRE float, até 4/4 = 1.0
```

#### Previsão: 0.1 + 0.2 == 0.3?

```py
0.1 + 0.2 == 0.3    # False!
print(0.1 + 0.2)    # 0.30000000000000004
```

**Explicação:** os computadores guardam floats em binário. Escrever 0.1 em binário é tão impossível como escrever 1/3 em decimal, por isso há pequenos erros de arredondamento. Daqui saem duas regras:

1. **Nunca comparar floats com `==`.** Usa `abs(a - b) < 1e-9`.
2. Os sistemas de pagamento reais evitam o problema contando em **cêntimos inteiros**.

#### Booleanos

```py
4 > 3                  # True
4 <= 3                 # False
5 == 4                 # False  (== compara; = atribui!)
5 != 4                 # True
(4 > 3) and (3 > 2)    # True
True or False, not True   # True, False
```

São a base dos sinais de trading, por exemplo "o preço está acima da média móvel?".

#### Strings (texto: tickers, nomes de colunas, ficheiros, relatórios)

```py
txt = 'financial modelling'
txt.capitalize()      # 'Financial modelling'
txt.upper()           # 'FINANCIAL MODELLING'
txt.split()           # ['financial', 'modelling']
txt.find('model')     # 10  (posição onde começa)
txt.find('2270')      # -1  → find() devolve -1 quando o texto NÃO existe
txt.replace(' ', '@') # 'financial@modelling'
```

#### f-strings: formatar números como um profissional

```py
portfolio_value = 1234567.8912
f"{portfolio_value:,.2f} EUR"   # '1,234,567.89 EUR'  (separador de milhares, 2 casas decimais)
f"{0.0834:.1%}"                 # '8.3%'  (percentagem com 1 casa decimal)
```

### 2.2 Contentores: tuple e list

- **tuple** `( )`: não pode ser alterado (imutável). Serve para registos fixos.
- **list** `[ ]`: pode ser alterada (mutável). Serve para coleções que crescem.
- **dict** `{chave: valor}`: mutável. Serve para procurar valores por nome.
- **set** `{ }`: mutável. Guarda elementos únicos.

```py
myTuple = (2026, 2270, 'Financial Modelling')
myTuple[2]          # 'Financial Modelling' (índice 2 = TERCEIRO elemento), tipo str
myList = [2026, 2270, 'Financial Modelling']
myList[-1]          # 'Financial Modelling' (índice negativo conta do fim)
```

#### Slicing: `a:b` vai de a até b−1 (o fim não entra)

```py
myList[0:2]   # [2026, 2270]
myList[0:1]   # [2026]  → uma LISTA com um elemento...
myList[0]     # 2026    → ...não é o mesmo que o próprio elemento
myList[1:]    # [2270, 'Financial Modelling']
myList[3]     # IndexError! A lista tem 3 elementos, o último índice é 2
```

#### A armadilha da multiplicação

Um colega quer duplicar os retornos diários, guardados numa lista, para simular alavancagem:

```py
returns = [1, 2, 3]
returns * 2      # [1, 2, 3, 1, 2, 3]  !!
returns + [4]    # [1, 2, 3, 4]
```

**Explicação:** nas listas, `*` significa **repetir** e `+` significa **concatenar**. Não há aritmética nenhuma. Um backtest que "duplica posições" assim não dá erro, simplesmente repete os dados em silêncio. A solução é o NumPy, onde `*` multiplica mesmo.

#### Porque é que as listas não chegam em finanças

- Aceitam tipos misturados, o que as torna flexíveis mas lentas e pesadas em memória.
- O slicing não consegue escolher "o 1º, o 4º e o 5º elemento" nem "todos os retornos positivos".
- A matemática não funciona elemento a elemento.
- Os dados financeiros são muitas vezes 2D (ativos × datas).

### 2.3 Arrays NumPy

Um `ndarray` tem um só tipo para todos os elementos, faz matemática elemento a elemento, tem indexação muito mais poderosa e pode ter várias dimensões.

```py
import numpy as np
myVec = np.array([1, 2, 3])
myVec * 2                       # [2 4 6] → aqui multiplica mesmo

myMat = np.array([[1, 2, 3],
                  [5, 6, 7]])   # lista de listas → matriz 2D
myOneRowMat = np.array([[1, 2, 3]])     # matriz 1×3 (repara nos parênteses retos duplos)
myOneColMat = myOneRowMat.transpose()   # matriz 3×1 (troca linhas e colunas)

np.zeros((2, 3))   # 2×3 de zeros
np.ones((3, 4))    # 3×4 de uns
np.eye(4)          # matriz identidade 4×4
```

#### Prática: a maturidade que desapareceu

Um aluno precisa das 4 datas de cupão semestrais de uma obrigação a 2 anos (0.5, 1.0, 1.5, 2.0):

```py
maturities = np.arange(0.5, 2, 0.5)
print(maturities)    # [0.5 1.  1.5] → falta o 2.0!
```

**Solução:** `np.arange` **exclui o limite superior**, tal como o slicing. A obrigação perdeu o último cash flow, que é precisamente o que inclui o reembolso do capital. Há duas formas de corrigir:

```py
np.linspace(0.5, 2, 4)          # preferível: dizes QUANTOS pontos queres
np.arange(0.5, 2 + 1e-10, 0.5)  # ou empurras o limite um pouco acima de 2
```

- `np.linspace(início, fim, quantos)` **inclui** o fim. `np.arange(início, fim, passo)` **exclui-o**.
- Verificar `.shape` logo a seguir a criar um array é o teste mais rápido que há: `np.linspace(0.5, 2, 4).shape` dá `(4,)`.

#### Fancy indexing: escolher dados como um analista

```py
maturities = np.linspace(0.5, 2, 4)        # [0.5 1.  1.5 2. ]
rates = np.array([5.0, 5.8, 6.5, 6.8])

maturities[[1, 3]]           # [1. 2.]      → posições 1 e 3
maturities[[0, -1]]          # [0.5 2. ]    → primeira e última
maturities[maturities < 2]   # [0.5 1.  1.5] → condição sobre o próprio array
maturities[rates < 6]        # [0.5 1. ]    → condição num array escolhe elementos de OUTRO
```

A última linha responde numa só linha, sem ciclo, a "dá-me as maturidades em que a taxa está abaixo de 6%". O mesmo padrão vai servir para "dá-me os retornos dos dias em que o preço estava acima da média", que é a base de uma estratégia de trading.

#### Indexação 2D: `M[linha, coluna]`, e `:` quer dizer "tudo nesta dimensão"

```py
myMatrix = np.array([[1,  8, 7, 4],
                     [5,  6, 9, 0],
                     [3, 11, 0, 4]])
myMatrix[0, 1]      # 8   (linha 0, coluna 1)
myMatrix[2, -1]     # 4   (último elemento da última linha)
myMatrix[0:2, 2:4]  # [[7 4]
                    #  [9 0]]   → forma 2×2 (linhas 0–1, colunas 2–3)
myMatrix[:, 2:3]    # [[7]
                    #  [9]
                    #  [0]]     → todas as linhas, coluna 2, mantida como COLUNA (3×1)
```

Nota: `myMatrix[:, 2]` daria `[7 9 0]`, um vetor 1D. O `2:3` mantém a forma de coluna.

#### Prática: o portefólio que se alterou sozinho

```py
maturities = np.array([1, 5, 9, 4, 5, 6])
first_maturities = maturities[0:3]
first_maturities[0] = 2          # editar "a cópia"
print(first_maturities)          # [2 5 9]
print(maturities)                # [2 5 9 4 5 6]  → o original também mudou!
```

**Solução:** um slice NumPy é uma **view**, não uma cópia. Os dois nomes apontam para a mesma memória, por isso editar o "extrato" corrompeu os dados de origem. Num projeto real é um bug terrível: nada dá erro e o estrago só aparece três passos depois, nos números de outra pessoa.

```py
first_maturities = maturities[0:3].copy()    # cópia independente
```

A indexação booleana (`maturities[maturities < 5]`) devolve uma **cópia**, não uma view. É mais uma razão para a usar.

### 2.4 Operações matemáticas com arrays

#### Estatísticas por eixo

- `axis=0` calcula ao longo das linhas, ou seja, um resultado por coluna.
- `axis=1` calcula ao longo das colunas, ou seja, um resultado por linha.
- Se as linhas forem datas e as colunas ativos, `axis=0` dá a média de cada ativo ao longo do tempo.

```py
myMatrix.mean()                       # 4.83  (média global)
myMatrix.mean(axis=0)                 # [3.   8.33 5.33 2.67] → 4 números (um por coluna)
myMatrix.mean(axis=1)                 # [5.  5.  4.5]          → 3 números (um por linha)
myMatrix.mean(axis=1, keepdims=True)  # igual, mas mantido como coluna 3×1
```

#### Aritmética elemento a elemento

```py
np.sqrt(A)   # raiz quadrada de cada elemento
A * 2        # multiplica cada elemento por 2 (compara com a "surpresa" das listas)
A + B        # soma elemento a elemento (mesma forma)
```

#### Broadcasting

Arrays com formas *diferentes* podem às vezes combinar-se: o NumPy "estica" o mais pequeno ao longo das dimensões de tamanho 1.

```py
v = np.array([2, 2, 2, 2])
A + v        # v é somado a CADA linha de A (3×4 + 4 → 3×4)
```

Uso típico: subtrair a média de retorno de cada ativo à respetiva coluna (`R - R.mean(axis=0)`).

### 2.5 Corrida de velocidade: listas vs. arrays

```py
big_list = list(range(1_000_000))
big_array = np.arange(1_000_000)
%timeit [x * 2 for x in big_list]   # ciclo Python
%timeit big_array * 2               # NumPy
```

O NumPy é tipicamente **50 a 200× mais rápido**, e a diferença aumenta com operações mais complexas. `%timeit` é um comando "mágico" do Jupyter/Colab que mede o tempo médio de execução. **Conselho:** antes de escreveres um ciclo sobre dados, pergunta se uma operação com arrays faz o mesmo.

### 2.6 Exercício: proibido usar ciclos

Preços de fecho fictícios de uma ação:

```py
prices = np.array([100.0, 102.0, 101.5, 105.0, 103.0, 99.0, 98.5, 104.0, 107.0, 106.0])
```

#### Solução completa

```py
# 1. Retornos simples diários r_t = P_t / P_{t-1} - 1
returns = prices[1:] / prices[:-1] - 1
# prices[1:]  = preços do dia 1 ao 9 (hoje)
# prices[:-1] = preços do dia 0 ao 8 (ontem)
# → 9 retornos: [2.00% -0.49% 3.45% -1.90% -3.88% -0.51% 5.58% 2.88% -0.93%]

# 2. Pior retorno e média
print(f"worst: {returns.min():.2%}, average: {returns.mean():.2%}")
# worst: -3.88%, average: 0.69%

# 3. Nº de dias positivos (True conta como 1, False como 0)
print("positive days:", (returns > 0).sum())      # 4

# 4. Média dos dias positivos vs. negativos
print(f"avg up-day:   {returns[returns > 0].mean():.2%}")   # 3.48%
print(f"avg down-day: {returns[returns < 0].mean():.2%}")   # -1.54%

# 5. Retorno médio nos dias em que o preço de ONTEM estava acima de 101
print(f"{returns[prices[:-1] > 101].mean():.2%}")           # -0.15%
```

**Explicações:**

- **(1)** Dividir dois slices desfasados de um dia é a forma vetorizada de calcular retornos. `prices[1:]` e `prices[:-1]` têm ambos 9 elementos, por isso emparelham.
- **(3)** Somar um array booleano conta os `True`. É um truque muito usado.
- **(4)** Há 4 dias de subida e 5 de descida. As subidas são maiores em média, por isso a média total fica positiva.
- **(5)** `prices[:-1]` está alinhado com `returns`: o elemento i é o preço da véspera do retorno i. Isto é, estruturalmente, a **avaliação completa de um sinal de trading**: condicionar na informação de ontem e medir o retorno de hoje. Neste caso o sinal "preço > 101" seria mau (−0,15% em média).

### Ideias-chave da Lecture 2 (Part 1)

1. Floats têm erros de arredondamento: nunca usar `==`.
2. Listas: `*` repete e `+` concatena. Arrays: `*` e `+` fazem aritmética.
3. `arange` exclui o fim e `linspace` inclui-o. Verifica sempre `.shape`.
4. Slices de arrays são **views**: usa `.copy()` quando precisares de uma cópia independente.
5. Indexação booleana entre arrays alinhados é a ferramenta central (filtros, sinais de trading).
6. `axis=0` dá um resultado por coluna e `axis=1` um por linha. Broadcasting aplica um vetor a cada linha.
7. Vetorizar é muito mais rápido do que fazer ciclos.


## Lecture 2 (Part 2): Bond Valuation

### 2.0 Porque obrigações, e porque é que um banco faliu

- O mercado obrigacionista é o **maior mercado de valores mobiliários**, maior do que o de ações.
- Uma obrigação (bond) não é mais do que uma **sequência de cash flows prometidos**: cupões periódicos mais o reembolso do capital (face value ou principal) na maturidade. Já sabemos avaliá-la com o valor presente da Lecture 1.
- Além do preço interessa o **risco**: *quanto muda o preço quando as taxas de juro mudam?* A resposta é a **duration**.
- Em março de 2023, o **Silicon Valley Bank** (40 anos, cerca de 200 mil milhões de dólares em ativos) colapsou em cerca de 48 horas. A causa, no fundo, é a derivada da fórmula do preço de uma obrigação em ordem a r.

**Vocabulário**

- **Face value / par:** o valor reembolsado na maturidade (por exemplo 100 ou 1.000).
- **Coupon rate:** juro anual pago em % do face value.
- **Market rate / yield:** a taxa que o mercado exige hoje, usada para descontar.
- **A desconto / ao par / com prémio:** preço abaixo / igual / acima do face value.

### 2.1 Avaliar uma obrigação (vetorizado)

Pagamentos C\_t, t = 1,…,N (os primeiros N−1 são cupões e C\_N inclui também o capital), descontados à taxa r:

$$
P = \sum_{t=1}^{N} \frac{C_t}{(1+r)^t}
$$

Assume-se uma estrutura temporal de taxas **plana**: a mesma taxa para todos os prazos.

#### Exemplo: obrigação a 2 anos, cupão de 6% semestral, descontada a 7%

Pergunta: o preço é (a) acima de 100, (b) exatamente 100 ou (c) abaixo de 100?

```py
import numpy as np
face_value = 100
coupon_rate = 0.06
semi_annual_coupon = coupon_rate / 2 * face_value    # 3 por semestre

times = np.linspace(0.5, 2, 4)      # [0.5 1. 1.5 2.] → linspace, não arange!
r = 0.07

N = times.size
cash_flows = semi_annual_coupon * np.ones(N)   # [3. 3. 3. 3.]
cash_flows[-1] += face_value                   # [3. 3. 3. 103.]  (a += b é a = a + b)

discounted_cash_flows = cash_flows / (1 + r/2)**(2*times)   # taxa semestral 3,5%, 2×t semestres
bond_price = discounted_cash_flows.sum()
print(f"Bond Price is ${bond_price:.2f}")      # $98.16
```

**Resposta: (c), abaixo de 100.** Uma obrigação que paga menos do que o mercado exige tem de ser vendida **a desconto**.

**Regra de verificação** (todo o preço que o teu código produzir deve passar este teste):

- cupão \< taxa de mercado → preço \< face value (desconto)
- cupão > taxa de mercado → preço > face value (prémio)
- cupão = taxa de mercado → preço = face value (par)

Com cupões semestrais, a taxa por período é r/2 e o expoente conta semestres (2t).

#### Prática: Bond A vs. Bond B (face value 1.000 €, 10 anos, taxa de mercado 7%)

- **Bond A:** acabada de emitir, cupão de 7%.
- **Bond B:** emitida há 5 anos com cupão de 13% (as taxas eram mais altas).

**Solução com ciclo:**

```py
n_years_B = 10
face_value_B = 1000
coupon_rate_B = 0.13
interest_rate = 0.07

bond_price_B = face_value_B / (1 + interest_rate)**n_years_B         # PV do capital
for t in range(1, n_years_B + 1):                                    # t = 1, ..., 10
    bond_price_B += coupon_rate_B * face_value_B / (1 + interest_rate)**t   # + PV de cada cupão
print(f"The price of Bond B is {bond_price_B:.2f} Euro.")            # 1421.41
```

**Solução vetorizada (NumPy):**

```py
times_B = np.arange(1, n_years_B + 1)                       # [1 2 ... 10]
coupons_B = coupon_rate_B * face_value_B * np.ones(n_years_B)   # 130 em cada ano
coupons_B[-1] += face_value_B                               # último ano: 130 + 1000
bond_price_B = np.sum(coupons_B / (1 + interest_rate)**times_B)
print(f"The price of Bond B is {bond_price_B:.2f} Euro.")   # 1421.41
```

**Explicação:**

- A **Bond A vale exatamente 1.000 €**, ao par, sem cálculos, porque o cupão é igual à taxa de mercado.
- A **Bond B vale cerca de 1.421 €**. Paga 13% quando o mercado oferece 7%, por isso tem de custar mais do que o face value. Ninguém oferece cupões de 13% ao par.

### 2.2 Duration

A **Macaulay duration** é a *média ponderada pelo tempo* do momento em que o dinheiro chega. O peso de cada data é a fração do preço que esse pagamento representa:

$$
D = \frac{1}{P} \sum_{t=1}^{N} \frac{t\,C_t}{(1+r)^t}
$$

#### Discussão: ordenar as durations (maturidade 10 anos, taxa 7%)

```py
def duration_bond(F, c, r, n):
    times = np.arange(1, n + 1)
    coupons = c * F * np.ones(n)
    coupons[-1] += F
    P = np.sum(coupons / (1 + r)**times)
    return np.sum(times * coupons / (1 + r)**times) / P

duration_zero = duration_bond(1000, 0.00, 0.07, 10)   # 10.00 anos
duration_A    = duration_bond(1000, 0.07, 0.07, 10)   #  7.52 anos
duration_B    = duration_bond(1000, 0.13, 0.07, 10)   #  6.75 anos
```

**Explicação:**

- A **zero-coupon** tem duration exatamente igual à maturidade (10): todo o dinheiro chega no ano 10.
- Os cupões puxam dinheiro para mais cedo, por isso a duration desce quando o cupão sobe. Ordem: **B \< A \< zero**.
- Mesma maturidade e três durations diferentes: **a maturidade não mede o risco de taxa de juro, a duration mede.**

**Função `def`:** `def nome(argumentos): ... return valor` cria uma função reutilizável. Aqui evita repetir o mesmo código para cada obrigação.

#### Duration como sensibilidade do preço

Derivando a fórmula do preço em ordem a r:

$$
\frac{dP}{dr} = \sum_{t=1}^{N} \frac{-t\,C_t}{(1+r)^{t+1}} = -\frac{D\,P}{1+r} \quad\Rightarrow\quad \frac{dP}{P} = -D\,\frac{dr}{1+r}
$$

- A duration é a **elasticidade do preço** em relação a (1+r).
- Uma obrigação com duration 7 perde cerca de **7% do valor quando as taxas sobem 1 ponto percentual** (a partir de níveis baixos).
- É *o* número de risco em qualquer mesa de fixed income.
- O sinal negativo quer dizer que, quando as taxas sobem, os preços descem.

#### Discussão: o risco é simétrico?

Bond A (duration ≈ 7,5). As taxas sobem de 7% para 9% (+2pp) ou descem para 5% (−2pp).

```py
def price_bond(F, c, r, n):
    times = np.arange(1, n + 1)
    coupons = F * c * np.ones(n)
    coupons[-1] += F
    return np.sum(coupons / (1 + r)**times)

P0   = price_bond(1000, 0.07, 0.07, 10)   # 1000.00
P_up = price_bond(1000, 0.07, 0.09, 10)   # −12.84%
P_dn = price_bond(1000, 0.07, 0.05, 10)   # +15.44%
approx = duration_A * 0.02 / 1.07         # ±14.05% (previsão da duration)
```

**Explicação:**

- O **ganho (+15,4%) é maior do que a perda (−12,8%)**, e a previsão da duration (±14%) fica no meio.
- A relação preço–taxa é uma **curva**, não uma reta. A duration é apenas o declive num ponto, uma aproximação de primeira ordem.
- Essa curvatura chama-se **convexidade** e joga a favor do obrigacionista: ganhas mais com a descida das taxas do que perdes com a subida.
- Para variações pequenas a duration é excelente. Para choques como os de 2008 ou 2022 é preciso contar com a curva.

#### Padrões da duration

**Duration em função do cupão:**

```py
import matplotlib.pyplot as plt
coupon_rates = np.linspace(0, 0.17, 20)
durations = np.zeros(len(coupon_rates))
for i in range(len(coupon_rates)):
    durations[i] = duration_bond(1000, coupon_rates[i], 0.07, 10)
plt.plot(coupon_rates, durations, 'b-', linewidth=2)
plt.ylabel("Duration"); plt.xlabel("Coupon rate"); plt.grid(True)
```

A curva é **decrescente**: vai de 10 (zero-coupon) até cerca de 6,5 (cupão de 17%). Cupões maiores antecipam o dinheiro.

**O caso difícil: duration em função da maturidade** (cupão de 4%, taxa de mercado de 15%):

```py
maturities = np.arange(1, 61, 1)
durations = np.zeros(len(maturities))
for i in range(len(maturities)):
    durations[i] = duration_bond(1000, 0.04, 0.15, maturities[i])
plt.plot(maturities, durations, 'g-', linewidth=2)
```

- "Maior maturidade implica maior duration" **nem sempre é verdade**.
- Aqui a duration sobe até um máximo de cerca de **9,05 anos (maturidade 19)** e depois **desce** até cerca de 7,7 anos na maturidade 60.
- Com taxas altas e cupões baixos, o capital distante vale tão pouco em PV que esticar a maturidade quase não mexe no "tempo médio de chegada", e a duration pode até cair.

#### Discussão: "a obrigação mais arriscada tem maior duration"?

**Não necessariamente.** Uma obrigação corporativa tem **risco de crédito (default)** que uma obrigação do Estado não tem. Mais risco de default leva a cupões prometidos mais altos (o investidor exige compensação), e cupões mais altos **baixam** a duration. Logo, a obrigação mais arriscada em termos de crédito pode ter **menor** duration. A duration mede apenas o **risco de taxa de juro**, não o risco total.

### 2.3 O trade do SVB

Versão estilizada do balanço do SVB em 2021:

- O banco usou os depósitos (muitos, mas voláteis, porque podem ser levantados a qualquer dia) para comprar obrigações longas (cerca de **10 anos**), seguras e garantidas pelo Estado, com yields de cerca de **1,6%**.
- Em 2022-23 a Fed subiu as taxas quase **5 pontos percentuais**, um dos ciclos de subida mais rápidos da história.

**Pergunta:** as obrigações eram *sem risco de default*. Quanto do valor de mercado poderia a subida de taxas destruir? (a) \~4% (b) \~10% (c) \~23% (d) zero

```py
portfolio = 91_000      # milhões de dólares (carteira held-to-maturity do SVB, aprox.)
r_2021 = 0.016
coupon = r_2021         # compradas ao par (cupão = taxa da altura)
r_2023 = 0.045
maturity = 10
face_value = 100

P_2021 = price_bond(face_value, coupon, r_2021, maturity)   # 100.00
P_2023 = price_bond(face_value, coupon, r_2023, maturity)   # 77.05
loss_pct = P_2023/P_2021 - 1                                # −22.9%
D = duration_bond(face_value, coupon, r_2021, maturity)     # 9.3 anos
print(f"Mark-to-market loss: {loss_pct*100:.1f}% = ${abs(loss_pct)*portfolio:,.0f} million")
# −22.9% = $20,882 million
```

**Resposta: (c), cerca de −23%**, perto de **21 mil milhões de dólares** em obrigações *sem risco de default*.

- A duration de cerca de 9,3 previa uma perda de ≈ 9,3 × 2,9pp / 1,016 ≈ **−27%**. A diferença para os −23% reais é a **convexidade**.
- "Sem risco de default" só quer dizer que recebes tudo **se esperares até à maturidade**. Se precisares de vender antes, vendes ao preço de mercado.
- **O ingrediente fatal foi o desfasamento (mismatch):** ativos com duration de cerca de 9 financiados por depósitos com duration de cerca de 0 (dinheiro que pode sair hoje à noite).
- Quando os depositantes perceberam o buraco, pediram **42 mil milhões de dólares num só dia** (9 de março de 2023). O banco teve de vender obrigações a estes preços desvalorizados e 48 horas depois tinha desaparecido.

#### Prática

**(1) Qual teria sido a perda com obrigações a 3 anos?**

```py
maturity = 3
P_2023 = price_bond(100, 0.016, 0.045, 3)
loss_pct = P_2023/100 - 1
print(f"Mark-to-market loss: {loss_pct*100:.1f}% = ${abs(loss_pct)*portfolio:,.0f} million")
# −8.0% = $7,255 million
```

Com 3 anos a perda seria de cerca de **8%**, quase três vezes menor, porque a duration é muito mais curta.

**(2) A que taxa de mercado a carteira a 10 anos perderia exatamente 10%?**

```py
r_2023 = 0.0276
P_2023 = price_bond(100, 0.016, r_2023, 10)
loss_pct = P_2023/100 - 1     # ≈ −10.0%
```

A cerca de **2,76%**. Bastava uma subida de apenas \~1,2pp (de 1,6% para 2,76%) para destruir 10% do valor. A taxa encontra-se por tentativa e erro com a função de preço, ou com `fsolve` como na Lecture 1.

### 2.4 Imunização: tornar uma promessa de pagamento à prova de taxas

Uma empresa deve 1.000 € (em valor presente) com vencimento a **10 anos**, e a taxa atual é de 6%. Quer comprar obrigações *hoje* de modo que, **aconteça o que acontecer às taxas**, o valor no ano 10 cubra a dívida. Uma carteira com esta propriedade diz-se **imunizada**.

**Porque é difícil:** depois de uma mudança de taxas há duas forças opostas.

- **Risco de reinvestimento:** os cupões recebidos são reinvestidos à *nova* taxa, o que prejudica quando as taxas **descem**.
- **Risco de preço:** o preço de revenda das obrigações move-se com as taxas, o que prejudica quando as taxas **sobem**.

**Resultado clássico:** as duas forças anulam-se quando a **duration da carteira = horizonte da responsabilidade**. É uma aproximação de primeira ordem e assume uma estrutura de taxas plana que se desloca em paralelo.

Há três obrigações candidatas, todas com face value de 1.000 €:

- **Bond 1:** 10 anos, cupão de 6,5%.
- **Bond 2:** 15 anos, cupão de 7%.
- **Bond 3:** 30 anos, cupão de 5,5%.

A resposta "óbvia" seria a Bond 1, porque vence exatamente no ano 10. Mas a maturidade não mede o risco de taxa de juro...

```py
r = 0.06; n = 10; PV = 1_000
FV = PV * (1 + r)**n                 # 1790.85 € → valor da dívida no ano 10

n1, c1, F1 = 10, 0.065, 1_000        # atribuição múltipla: a ordem conta!
n2, c2, F2 = 15, 0.070, 1_000
n3, c3, F3 = 30, 0.055, 1_000

P_bond1 = price_bond(F1, c1, r, n1)  # 1036.80
P_bond2 = price_bond(F2, c2, r, n2)  # 1097.12
P_bond3 = price_bond(F3, c3, r, n3)  #  931.18

w1, w2, w3 = PV/P_bond1, PV/P_bond2, PV/P_bond3   # unidades para investir 1000 € em cada
# 0.965, 0.911, 1.074

d1 = duration_bond(F1, c1, r, n1)    #  7.70 anos
d2 = duration_bond(F2, c2, r, n2)    # 10.00 anos
d3 = duration_bond(F3, c3, r, n3)    # 14.83 anos
```

**A obrigação que imuniza é a Bond 2, a de 15 anos**, porque tem duration ≈ 10, igual ao horizonte. A Bond 1 tem duration de apenas 7,7 porque os cupões chegam cedo. Muitos departamentos de tesouraria reais também escolheriam a Bond 1.

#### Valor de cada posição no ano 10

No ano 10 cada posição vale **cupões recebidos, reinvestidos à taxa em vigor, mais o preço de mercado da obrigação que ainda falta pagar**.

```py
coupon_FV_times = np.linspace(n-1, 0, n)   # [9 8 ... 0] = anos que cada cupão passa a render

P10_bond1 = w1*(F1*c1*np.sum((1+r)**coupon_FV_times) + F1)                          # vence no ano 10
P10_bond2 = w2*(F2*c2*np.sum((1+r)**coupon_FV_times) + price_bond(F2, c2, r, n2-n)) # faltam 5 anos
P10_bond3 = w3*(F3*c3*np.sum((1+r)**coupon_FV_times) + price_bond(F3, c3, r, n3-n)) # faltam 20 anos
# a 6% inalterado: as três valem 1790.85 = exatamente a dívida
```

- O cupão do ano 1 rende 9 anos e o do ano 10 rende 0, daí `linspace(9, 0, 10)`.
- Se as taxas não mudam, qualquer investimento de 1.000 € a 6% vale 1.790,85 € no ano 10.

#### As taxas descem para 5% logo após a compra (e ficam lá)

```py
r_new = 0.05
# (mesmo código com r_new)
# Bond 1: 1753.05  → SUBFINANCIA (−37,80 €)
# Bond 2: 1792.91  → praticamente igual à dívida (+2,06 €)
# Bond 3: 1883.74  → SOBREFINANCIA (+92,89 €)
```

**Explicação:**

- **Bond 1:** venceu no ano 10, por isso já não tem risco de preço. Só sofre o reinvestimento dos cupões a 5%, e o **risco de reinvestimento ganha**.
- **Bond 3:** ainda faltam 20 anos. Com taxas mais baixas o preço de revenda sobe muito, e o **risco de preço ganha** (a favor).
- **Bond 2:** as duas forças anulam-se.

#### Visão completa para todas as taxas

```py
r_all = np.linspace(0, 0.15, 16)
p1 = np.zeros(len(r_all)); p2 = np.zeros(len(r_all)); p3 = np.zeros(len(r_all))
for i in range(len(r_all)):
    p1[i] = w1*(F1*c1*np.sum((1+r_all[i])**coupon_FV_times) + F1)
    p2[i] = w2*(F2*c2*np.sum((1+r_all[i])**coupon_FV_times) + price_bond(F2, c2, r_all[i], n2-n))
    p3[i] = w3*(F3*c3*np.sum((1+r_all[i])**coupon_FV_times) + price_bond(F3, c3, r_all[i], n3-n))

plt.plot(r_all, p1, '-d', r_all, p2, '-o', r_all, p3, '-s', linewidth=2)
plt.axhline(FV, color='k', linestyle=':')          # linha horizontal = a dívida
plt.legend(['Bond 1 (D=7.7)', 'Bond 2 (D=10.0)', 'Bond 3 (D=14.8)', 'Obligation'])
```

- A **Bond 1 sobe** com a taxa (ganha com reinvestimento) e fica abaixo da dívida quando as taxas descem.
- A **Bond 3 desce** com a taxa (perde preço) e fica abaixo da dívida quando as taxas sobem.
- A **Bond 2** tem forma de U, toca a dívida a 6% e **nunca fica abaixo dela**. É a convexidade outra vez.

**Conclusão:** para imunizar, casa a **duration**, não a maturidade. O casamento é só de primeira ordem: para choques grandes as curvas afastam-se.

#### Linearidade da duration

A duration de uma carteira é a **média ponderada pelo valor** das durations das obrigações. Por isso uma *mistura* da Bond 1 (D = 7,7) com a Bond 3 (D = 14,8) também chega a 10:

$$
w_1 D_1 + (1-w_1) D_3 = 10 \quad\Rightarrow\quad w_1 = \frac{D_3 - 10}{D_3 - D_1}
$$

```py
w_bond1 = (d3 - n) / (d3 - d1)       # 0.678
print(f"Invest in Bond 1: {1000*w_bond1:.0f} Euro, in Bond 3: {1000*(1-w_bond1):.0f} Euro")
# Bond 1: 678 €, Bond 3: 322 €
```

#### Prática: barbell vs. bullet

**1. Valor no ano 10 da carteira de duas obrigações se a taxa cair para 5%:**

```py
P10_ptf_new = w_bond1*P10_bond1_new + (1-w_bond1)*P10_bond3_new
print(f"Year-10 value of bond portfolio at 5%: {P10_ptf_new:.2f} Euro")   # 1795.17
```

Vale **1.795,17 € > 1.790,85 €**, por isso **cobre a dívida**, com uma margem até maior do que a da Bond 2 sozinha (1.792,91 €).

**2. Gráfico: carteira barbell vs. Bond 2**

```py
p_ptf = w_bond1*p1 + (1-w_bond1)*p3
plt.plot(r_all, p2, '-d', r_all, p_ptf, '-s', linewidth=2)
plt.axhline(FV, color='k', linestyle=':')
plt.legend(['Bond 2', 'Barbell portfolio (Bonds 1+3)'])
```

Valores no ano 10 (a dívida é 1.790,85 €):

- Taxa de 0%: Bond 2 ≈ 1.869 €, barbell ≈ 1.996 €.
- Taxa de 4%: Bond 2 ≈ 1.799 €, barbell ≈ 1.809 €.
- Taxa de 8%: Bond 2 ≈ 1.799 €, barbell ≈ 1.806 €.
- Taxa de 15%: Bond 2 ≈ 1.962 €, barbell ≈ 2.043 €.

**Explicação:**

- A **barbell** (uma obrigação curta mais uma longa) fica mais acima da dívida **nos dois sentidos**. Tem a mesma duration mas **mais convexidade**: cash flows mais espalhados no tempo dão uma curva mais acentuada.
- A **bullet** (uma única obrigação com a duration certa) é menos convexa.
- Na prática o mercado sabe isto e faz-te pagar pela convexidade (yields mais baixas), mas isso já é tema de um curso de fixed income.

### Ideias-chave da Lecture 2 (Part 2)

1. **Preço de uma obrigação** = PV dos cupões + PV do capital. Cupão \< yield → desconto. Cupão > yield → prémio. Iguais → par.
2. **Duration** é o tempo médio ponderado de chegada do dinheiro e também a sensibilidade do preço às taxas: ΔP/P ≈ −D·Δr/(1+r).
3. Cupões mais altos dão duration mais baixa. Maturidade mais longa *geralmente* dá duration mais alta, mas nem sempre (cupão baixo com taxa alta).
4. **Convexidade:** a relação preço–taxa é curva, os ganhos com descidas de taxas são maiores do que as perdas com subidas, e a duration falha em choques grandes.
5. **"Sem risco de default" ≠ "sem risco"**: o SVB perdeu cerca de 23% em obrigações do Estado por causa do desfasamento de duration entre ativos (≈9) e passivos (≈0).
6. **Imunização:** casar a duration da carteira com o horizonte da dívida, não a maturidade. A duration é linear, por isso podes combinar obrigações para chegar à duration alvo.
7. **Barbell vs. bullet:** com a mesma duration, a barbell tem mais convexidade e protege melhor contra grandes choques de taxas.
8. **Python:** `def` para funções, `np.ones`, `+=`, `np.linspace` para datas de cupão, ciclos `for` com `range(len(...))` para preencher arrays e `plt.axhline` para linhas de referência.

### Armadilhas da Lecture 2

#### Part 1: Python e NumPy

- **`0.1 + 0.2 == 0.3` é `False`**: compara floats com `abs(a - b) < 1e-9`.
- **`=` atribui, `==` compara.** `/` devolve sempre float (`4/4 = 1.0`).
- **`find()` devolve −1** quando não encontra (não dá erro).
- **Listas: `*` repete** (`[1,2,3]*2 = [1,2,3,1,2,3]`) e `+` concatena. Em arrays, fazem aritmética.
- **`myList[0:1]` é uma lista** (`[2026]`); `myList[0]` é o elemento (`2026`). Índice fora do tamanho → `IndexError`.
- **`np.arange` exclui o fim** (perde o último cupão!); `np.linspace` inclui-o.
- **Slice NumPy = view**: alterar o slice altera o original. Usa `.copy()`. Indexação booleana devolve cópia.
- **`axis=0` → um valor por coluna**; `axis=1` → um por linha. Numa matriz 3×4, `mean(axis=0)` tem 4 valores.
- **`M[:, 2]` → 1D** (`[7 9 0]`); `M[:, 2:3]` → coluna 3×1.
- **`np.max(a)` ≠ `np.maximum(a, b)`**: o primeiro dá um número, o segundo compara elemento a elemento.
- **Retornos vetorizados:** `prices[1:] / prices[:-1] - 1`. n preços dão n−1 retornos.

#### Part 2: Obrigações

- **Teste de sanidade do preço:** cupão \< yield → abaixo do par; cupão > yield → acima; iguais → par (sem calcular nada).
- **Cupões semestrais:** taxa r/2, cupão c/2 × F e expoente 2t (semestres).
- **Zero-coupon: duration = maturidade.** Com cupões, duration \< maturidade.
- **Cupão mais alto → duration mais baixa.** Maturidade mais longa → duration *geralmente* mais alta, mas não com cupão baixo e taxa alta.
- **Aproximação da duration:** ΔP/P ≈ −D · Δr / (1+r). Não te esqueças do (1+r) nem do sinal.
- **Convexidade:** a subida do preço quando as taxas descem é maior do que a queda quando sobem. A duration sobrestima perdas e subestima ganhos em choques grandes.
- **Sem risco de default ≠ sem risco:** há risco de taxa de juro se tiveres de vender antes da maturidade (SVB).
- **Mais risco de crédito pode dar menos duration** (cupões mais altos). Duration só mede risco de taxa de juro.
- **Imunizar = casar a duration com o horizonte**, não a maturidade (Bond 2 de 15 anos, não a Bond 1 de 10 anos).
- **Risco de reinvestimento** dói quando as taxas descem; **risco de preço** dói quando sobem.
- **Duration é linear** nos pesos (em valor): w₁D₁ + w₃D₃ = alvo.
- **Barbell** tem mais convexidade do que a **bullet** com a mesma duration.

### Números de referência da Lecture 2

| Exemplo | Resultado |
| --- | --- |
| `0.1 + 0.2` | 0.30000000000000004 |
| Exercício sem ciclos (10 preços) | 9 retornos · pior −3,88% · média 0,69% · 4 dias positivos |
| Bond 2 anos, cupão 6% semestral, 7% | \$98,16 (desconto) |
| Bond A (cupão 7%, yield 7%, 10 anos) | 1.000 € (par) · D = 7,52 |
| Bond B (cupão 13%, yield 7%, 10 anos) | 1.421,41 € (prémio) · D = 6,75 |
| Zero-coupon 10 anos | D = 10,00 |
| Bond A com ±2pp | +15,44% / −12,84% (duration previa ±14,05%) |
| SVB (10 anos, 1,6% → 4,5%) | −22,9% ≈ \$20,9 mil milhões · D ≈ 9,3 · com 3 anos: −8,0% |
| SVB: perda de 10% | basta a taxa subir para ≈ 2,76% |
| Imunização (dívida 1.000 € PV, 10 anos, 6%) | FV da dívida 1.790,85 € · D₁ = 7,70 · D₂ = 10,00 · D₃ = 14,83 |
| Taxas descem para 5% | Bond 1: 1.753,05 · Bond 2: 1.792,91 · Bond 3: 1.883,74 |
| Barbell com D = 10 | 678 € na Bond 1 + 322 € na Bond 3 · a 5% vale 1.795,17 € |

### Testa-te: Lecture 2

**1.** O que dá `returns = [1, 2, 3]; returns * 2`?<br>(a) \[2, 4, 6\] · (b) \[1, 2, 3, 1, 2, 3\] · (c) 12 · (d) Um erro

<details>
<summary>Resposta</summary>

**(b)**. Numa lista, `*` repete. Para multiplicar cada elemento usa um array NumPy: `np.array([1, 2, 3]) * 2` dá `[2 4 6]`.

</details>

**2.** Queres as datas de cupão semestrais de uma obrigação a 2 anos. Qual linha está certa?<br>(a) `np.arange(0.5, 2, 0.5)` · (b) `np.linspace(0.5, 2, 4)` · (c) `range(0.5, 2, 0.5)` · (d) `np.linspace(0.5, 2, 0.5)`

<details>
<summary>Resposta</summary>

**(b)**. Dá `[0.5 1. 1.5 2.]`. A (a) perde o 2.0 (o arange exclui o fim), a (c) dá erro (range só aceita inteiros) e a (d) pede 0,5 pontos.

</details>

**3.** `M` é uma matriz 3×4 (linhas = datas, colunas = ativos). Qual é o shape de `M.mean(axis=0)`?<br>(a) (3,) · (b) (4,) · (c) (3, 4) · (d) (1,)

<details>
<summary>Resposta</summary>

**(b)**. `axis=0` calcula ao longo das linhas: um valor por coluna, ou seja, a média de cada um dos 4 ativos.

</details>

**4.** Uma obrigação a 10 anos tem cupão de 5% e a taxa de mercado é 7%. O preço (face value 1.000 €) é:<br>(a) Acima de 1.000 € · (b) Exatamente 1.000 € · (c) Abaixo de 1.000 € · (d) Depende da duration

<details>
<summary>Resposta</summary>

**(c)**. Cupão \< yield → desconto. O valor exato é ≈ 859,53 €.

</details>

**5.** Três obrigações a 10 anos, taxa de 7%: zero-coupon, cupão 7% e cupão 13%. Ordena as durations da maior para a menor.<br>(a) 13% > 7% > zero · (b) zero > 7% > 13% · (c) são todas 10 · (d) 7% > zero > 13%

<details>
<summary>Resposta</summary>

**(b)**. Zero = 10,00, cupão 7% = 7,52, cupão 13% = 6,75. Cupões maiores trazem o dinheiro mais cedo.

</details>

**6.** Uma obrigação tem duration 7 e yield de 7%. As taxas sobem 1 ponto percentual. A variação de preço aproximada pela duration é:<br>(a) +7% · (b) −7% · (c) ≈ −6,5% · (d) −1%

<details>
<summary>Resposta</summary>

**(c)**. ΔP/P ≈ −D · Δr / (1+r) = −7 × 0,01 / 1,07 ≈ −6,5%. A regra "perde \~7% por cada 1pp" é a versão simplificada para taxas baixas. Por causa da convexidade, a perda real é ainda um pouco menor.

</details>

**7.** Tens de pagar uma dívida daqui a 10 anos e queres imunizar. Qual obrigação escolhes?<br>(a) A que vence em 10 anos · (b) A que tem duration de 10 anos · (c) A de cupão mais alto · (d) A de 30 anos, porque tem mais convexidade

<details>
<summary>Resposta</summary>

**(b)**. Imunizar é casar a duration com o horizonte. No exemplo da aula é a Bond 2 (15 anos, D = 10), não a Bond 1 (10 anos, D = 7,7).

</details>

**8. (aberta)** Este código devia guardar as 3 primeiras maturidades e mudar só a cópia. O que acontece e como corriges?

```py
maturities = np.array([1, 5, 9, 4, 5, 6])
first = maturities[0:3]
first[0] = 2
```

<details>
<summary>Resposta</summary>

- Um slice NumPy é uma **view**: `first` e `maturities` partilham a memória, por isso `maturities` passa a ser `[2 5 9 4 5 6]`. Não há erro nenhum.
- Correção: `first = maturities[0:3].copy()`.

</details>

**9. (aberta)** O SVB tinha obrigações do Estado, "sem risco". Explica como perdeu cerca de 23% do valor e porque é que isso o fez falir.

<details>
<summary>Resposta</summary>

- Comprou obrigações a \~10 anos com yield de \~1,6% (duration ≈ 9,3). Quando as taxas subiram para \~4,5%, o preço de mercado caiu ≈ 23% (a duration previa ≈27%; a diferença é a convexidade).
- "Sem risco de default" só garante o pagamento **na maturidade**. Se tens de vender antes, vendes ao preço de mercado.
- O problema foi o **mismatch de duration**: ativos com D ≈ 9 financiados por depósitos com D ≈ 0. Quando os depositantes levantaram 42 mil milhões num dia, o banco teve de vender com perdas e faliu em 48 horas.
- Com obrigações a 3 anos, a perda teria sido só ≈ 8%.

</details>

**Refaz no notebook, sem olhar para as soluções:** Part 1 — "a maturidade que desapareceu", "o portefólio que se alterou sozinho" e 2.6 "proibido usar ciclos". Part 2 — Bond A vs. Bond B, a prática do SVB (3 anos e perda de 10%) e barbell vs. bullet.
