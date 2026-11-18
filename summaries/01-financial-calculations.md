# Lecture 1 — Princípios e Basic Financial Calculations

> Resumo exportado das notas em Notion (18/11/2026). As respostas das perguntas *Testa-te* estão escondidas: clica em **Resposta** para as ver.

## Week 1: Princípios de Financial Modelling + Python Basics

### O que é um modelo?

- **Definição genérica:** uma representação de uma coisa, sistema ou teoria que permite examinar ou alterar as características do original.
- **Definição de negócio:** um programa de computador com lógica estruturada que mostra as relações entre variáveis dinâmicas, cujo output responde às perguntas da gestão.

### Porquê usar um modelo?

- **Precisão:** se uma ideia pode ser descrita, pode ser modelada. Nada é demasiado complexo ou detalhado para isso.
- **Eficiência:**
  - Poupa tempo em cálculos repetitivos.
  - Simplifica um problema de negócio ao parti-lo nas suas componentes.
  - Documenta num só sítio as fontes de dados, os pressupostos e as metodologias.
- **Interatividade:** permite análises "what if" para testar a sensibilidade dos resultados a mudanças no negócio, e pode ser atualizado em tempo real.
- Os modelos podem ter cálculos complexos, mas devem ter sempre **interfaces simples** para o utilizador.

### Como construir um modelo?

**1. Estrutura e design**

- Determinar o objetivo do modelo.
- Definir o output.
- Identificar os dados necessários.
- Definir o fluxo e o conteúdo das secções principais.
- **Desenhar o layout físico.** Este passo tem um ROI altíssimo: mais de 10× o tempo investido.
- O design do modelo pode ser, ele próprio, um entregável.

**2. Construção**

- Estabelecer pressupostos, introduzir os dados, formatar segundo a estrutura definida e testar erros.
- Com uma boa estrutura e design, a construção deve ser direta.

**3. Utilização**

- Testar a lógica e os limites, atualizar e modificar o modelo conforme necessário, e criar documentação.

### O que é um bom modelo?

- **Rápido de perceber:** fluxo lógico claro, divisível em componentes geríveis, inputs bem especificados e funcionalidades complexas só onde são mesmo necessárias.
- **Orientado para objetivos:** responde às necessidades de decisão do cliente, com inputs e outputs adequados e o nível de detalhe certo.
- **Sem erros:** sem consequências não intencionais nem pressupostos implícitos, capta corretamente a relação entre variáveis e é fácil de calibrar (comparar com dados históricos).
- Em resumo, um bom modelo é **coerente, bem formatado, robusto, simples, transparente, reutilizável e atualizável**.

**Processo de um bom modelo**

- **Dados obtíveis e precisos.** Obtíveis porque são publicados regularmente (relatórios regulatórios, relatórios de investimento) e por isso atualizáveis. Precisos porque a fonte não é contestada.
- **Objetivo vs. subjetivo:** pressupostos e cenários razoáveis, baseados em factos sempre que possível, e uma razão clara para incluir cada dado.
- **Documentação completa:** objetivo do modelo, explicação dos fluxos de dados e dos cálculos complexos, fontes e como atualizar, limitações e melhorias possíveis.

### Porquê Python?

- Linguagem de uso geral criada em 1989 por Guido van Rossum.
- É **gratuita e open source**, coordenada pela Python Software Foundation. Isto poupa dinheiro, põe a linguagem nas mãos da comunidade de utilizadores e não de uma empresa, e incentiva a **reprodutibilidade** e a ciência aberta.

### Python Basics: condições e ciclos

#### if / elif / else

- Permitem ramificação lógica: fazer coisas diferentes consoante uma condição.
- A sintaxe usa **dois pontos `:` e indentação**. A indentação determina o que está dentro de cada bloco, por isso afeta o fluxo do programa.
- `if` define a condição, `elif` acrescenta condições adicionais e `else` diz o que fazer quando nenhuma se cumpre.
- Convém manter os `if` curtos, porque ramos longos levam a código repetido.

```py
if asset_vol > 0:                                      # condição 1
    sharpe_ratio = (asset_ret - rf_rate) / asset_vol
    print(f'Asset Sharpe Ratio is {sharpe_ratio}')
elif asset_ret == rf_rate:                             # condição 2
    print('Asset is just the risk-free bond.')
else:                                                  # nenhuma das anteriores
    print('Asset payoffs are risk-free. This is an arbitrage opportunity!')
```

Leitura financeira: se o ativo tem volatilidade, calcula-se o Sharpe ratio. Se não tem volatilidade e rende o mesmo que a taxa sem risco, é simplesmente uma obrigação sem risco. Se não tem volatilidade mas rende mais do que a taxa sem risco, é uma **arbitragem** (lucro sem risco).

**Operadores lógicos:** `<`, `>`, `<=`, `>=`, `==` (igual), `!=` (diferente). `and` exige que todas as condições sejam verdadeiras, `or` basta uma.

#### Ciclos for

- Repetem um bloco de código um **número fixo de vezes**. É o que torna os computadores tão poderosos.
- O Colab indenta automaticamente depois dos `:`. Se te esqueceres dos dois pontos, dá erro.
- A variável do ciclo (o **loop counter**) é por convenção `i`, `j`, `k` ou `n`.

#### range(start, stop, step)

Gera uma sequência de inteiros. O `stop` **não é incluído** e, se omitires `start`, começa em 0. Se omitires `step`, o passo é 1.

```py
range(10)          # 0, 1, ..., 9   (atenção à indexação a partir de 0)
range(1, 11)       # 1, 2, ..., 10
range(0, 30, 5)    # 0, 5, 10, 15, 20, 25   (o 30 não aparece)
range(0, -10, -1)  # 0, -1, ..., -9   (passo negativo conta para trás)
x = list(range(1, 21, 1))   # um range não se imprime diretamente: converte em lista
```

#### Ciclos encaixados (nested loops)

Um ciclo dentro de outro: para cada valor do ciclo exterior, o interior corre do início ao fim.

```py
N = 4; M = 4
for n in range(1, N, 1):        # ciclo exterior: n = 1, 2, 3
    for m in range(1, M, 1):    # ciclo interior: m = 1, 2, 3
        print(m*n)              # imprime 9 valores: 1 2 3, 2 4 6, 3 6 9
```

### Complementos da sebenta às Lectures 1 e 2

- **Fórmula da anuidade em Python:** `PV0 = CF/r*(1-(1/((1+r)**T)))` dá 445,18 € para 100 €/ano durante 5 anos a 4%, igual à soma termo a termo.
- Em Python, potências escrevem-se com `**`, **não** com `^`. Usa `;` para pôr várias instruções na mesma linha.
- **Reforma, a lógica dos índices:** as contribuições são no início de cada ano, por isso descontam com os expoentes 0, 1, 2, 3, 4. Os levantamentos usam os expoentes 5 a 12. O numerador da fórmula é quanto precisas hoje para financiar os 8 levantamentos e o denominador é quanto vale hoje 1 € depositado em cada um dos 5 anos.
- **`txt.replace('l', 'L', 2)`:** o terceiro argumento limita o número de substituições (aqui só as 2 primeiras ocorrências).
- **`type()`** dá o tipo de qualquer objeto. **dict** guarda pares chave-valor e **set** é uma coleção não ordenada de elementos únicos.
- **`list(myTuple)`** converte um tuple numa lista, que já pode ser alterada.
- **Funções estatísticas do NumPy:**
  - `np.mean(a)` e `np.std(a)`: média e desvio padrão.
  - `np.amax(a)` / `np.max(a)` e `np.amin(a)` / `np.min(a)`: o **maior / menor elemento** de um array (devolve um só número).
  - `np.maximum(x1, x2)` e `np.minimum(x1, x2)`: comparam **dois arrays elemento a elemento** e devolvem um array. Por exemplo, `np.maximum(payoff, 0)` é o payoff de uma opção.
  - `np.linalg.norm(x)`: comprimento (norma) de um vetor.
- **Indexação mista 2D:** `M[a:c, b]` dá algumas linhas de uma coluna e `M[a, b:d]` algumas colunas de uma linha. Ambas devolvem um array 1D.
- **Broadcasting com matriz de uma linha:** `C = np.array([v])` é uma matriz 1×4. `A + C` dá o mesmo que `A + v`, porque a linha é repetida para as 3 linhas de A.
- **Duration:** os pesos C\_t / \[P(1+r)\^t\] somam 1. A duration é, literalmente, uma média ponderada dos tempos. Com uma taxa de desconto perto de 0, a duration cresce sempre com a maturidade. Com uma taxa alta, a relação deixa de ser monótona.
- **Imunização, formalmente:** uma empresa tem uma obrigação futura Q com valor presente V\_0 = Q/(1+r)\^N e cobre-a com uma obrigação cujo valor V\_B = V\_0. Com a estrutura de taxas plana e movimentos paralelos, a condição necessária e suficiente (em 1ª ordem) para os valores continuarem iguais é **duration do ativo = duration da obrigação**. Há duas limitações: a aproximação de 1ª ordem pode afastar-se muito da igualdade real, e a hipótese de estrutura plana pode não se verificar.


## Lecture 1: Basic Financial Calculations

### 1.0 Ideia central: um euro hoje não vale um euro amanhã

- Bonds, carteiras e simulações assentam todos na mesma ideia: **cash flows em momentos diferentes não são comparáveis**. Para os comparar ou somar, é preciso levá-los ao mesmo ponto no tempo.
- Trazer um cash flow futuro para hoje chama-se **descontar**. O resultado é o **valor presente (PV)**:

$$
PV = \frac{CF_t}{(1+r)^t}
$$

- **r = taxa de desconto = custo de oportunidade**: o que ganharias numa alternativa comparável. Quanto mais arriscado o cash flow, maior o r exigido e menor o valor hoje.
- Sinónimos: discount rate, cost of capital, interest rate, required return.
- A pergunta que se repete em toda a aula: *quanto vale hoje esta sequência de pagamentos futuros?*

### 1.1 O Louisiana Purchase (1803) foi um bom negócio?

Os EUA pagaram 15 milhões de dólares por 2,1 milhões de km². Se em vez disso tivessem investido o dinheiro durante 223 anos:

```py
amount = 15e6
T = 2026 - 1803
r = 0.05
FV = amount * (1 + r)**T
print(f"Return {r:.0%}: $15M in 1803 grows to ${FV/1e9:,.0f} billion today")
```

- A 3%: cerca de **11 mil milhões**.
- A 5%: cerca de **797 mil milhões**.
- A 7%: cerca de **53,5 biliões** (quase 2× o PIB dos EUA).
- A taxa que leva os 15M aos 30 biliões do PIB atual é **≈ 6,7%**.

**Lição:** com horizontes longos, pequenas diferenças na taxa mudam o resultado em milhares de vezes. Perguntar se "foi um bom negócio" não tem resposta sem dizer o que o dinheiro *podia* ter rendido. Esse custo de oportunidade é a taxa de desconto, o primeiro input de qualquer modelo.

**Python:** `f"{x:.0%}"` formata como percentagem e `f"{x:,.0f}"` põe separador de milhares sem casas decimais.

### 1.2 Valor presente passo a passo

**Investimento 1:** 100 € no fim de cada um dos próximos 5 anos, com r = 4%.

```py
CF1 = 100; CF2 = 100; CF3 = 100; CF4 = 100; CF5 = 100
r = 0.04
PV0 = CF1/(1+r)**1 + CF2/(1+r)**2 + CF3/(1+r)**3 + CF4/(1+r)**4 + CF5/(1+r)**5
print(f"The present value of Investment 1 is {PV0:.2f} Euro")   # 445.18
```

Vale menos que os 500 € "no papel", porque cada pagamento é descontado.

**Investimento 2:** 100, 200, 300, 400, 500 → 1.500 € no papel, mas o **PV é 1.300,65 €**. É *menos* de 3× o Investimento 1, porque o dinheiro chega mais tarde e é descontado mais vezes.

#### Net Present Value (NPV)

Inclui o custo inicial (cash flow negativo no tempo 0):

$$
NPV = CF_0 + \sum_{t=1}^{N} \frac{CF_t}{(1+r)^t}
$$

**Regra de decisão: investir se NPV > 0.**

- Comprar o Investimento 2 por 1.500 € dá NPV ≈ −199 €, ou seja, destrói valor.
- Prática: um ativo custa 600 € e paga 100 €/ano durante 10 anos, com r = 8%. NPV = **+71,01 €**, logo **comprar**.

Atalho com a fórmula da **anuidade** (pagamentos iguais):

$$
PV = C \cdot \frac{1-(1+r)^{-n}}{r}
$$

```py
payment = 100; r = 0.08; n = 10; price = 600
NPV = payment*(1 - 1/(1+r)**n)/r - price
if NPV > 0:
    print("buy the asset")
else:
    print("don't buy the asset")
```

### 1.3 IRR: a taxa escondida num negócio

Inverte-se a pergunta: dado o preço, que taxa estou de facto a receber? A **Internal Rate of Return** é a taxa que torna o NPV = 0:

$$
CF_0 + \sum_{t=1}^{N} \frac{CF_t}{(1+IRR)^t} = 0
$$

- É o número a calcular sempre que alguém oferece "dinheiro depois em troca de dinheiro agora" (banco, stand de carros, fundo de pensões).
- Não tem solução analítica (é a raiz de um polinómio), por isso resolve-se numericamente com `fsolve`:

```py
from scipy.optimize import fsolve
CF0 = -800
IRR = fsolve(lambda IRR: CF0 + 100/(1+IRR)**1 + 200/(1+IRR)**2
             + 300/(1+IRR)**3 + 400/(1+IRR)**4 + 500/(1+IRR)**5, 0.05)
print(f"IRR = {100*IRR[0]:.2f}%")
```

- `lambda` cria uma função numa linha. O `0.05` é o palpite inicial. `fsolve` devolve um array, daí o `IRR[0]`.
- Ao preço justo (1.300,65 €) a IRR é exatamente 4%. A 800 € é bem mais alta, ≈ 19–20% (onde a curva cruza zero).
- Prática: o ativo de 600 € com 100 €/ano durante 10 anos tem **IRR = 10,56%**, acima dos 8%, o que é coerente com NPV > 0.

#### NPV em função da taxa de desconto

```py
import numpy as np
import matplotlib.pyplot as plt
i = np.linspace(0, 0.25, 100)       # 100 taxas entre 0% e 25%
npv = -800 + 100/(1+i) + 200/(1+i)**2 + 300/(1+i)**3 + 400/(1+i)**4 + 500/(1+i)**5
plt.plot(i*100, npv, 'g--', i*100, i*0, 'k-', linewidth=2)
plt.xlabel("Discount rate, %"); plt.ylabel("NPV"); plt.grid(True)
```

- A curva é **decrescente**: quanto maior a taxa, menor o NPV. **Cruza o zero na IRR.**
- `np.linspace(a, b, n)` dá n pontos igualmente espaçados. Calcular 100 NPVs numa linha, sem ciclo, é a **vetorização** do NumPy da Parte 1.

#### IRR em private equity (LBO)

- **LBO (leveraged buyout):** um fundo compra uma empresa sobretudo com dívida e vende-a uns anos depois. A performance é reportada com dois números: **MOIC** e **IRR**.
- **TascaCo:** o fundo investe −360M hoje, recebe +100M de dividendo no ano 3 (*dividend recap*) e +817M na venda no ano 5.
  - **MOIC** (multiple of invested capital) = (100 + 817) / 360 = **2,55×**. Não tem dimensão temporal.
  - **IRR ≈ 21,8%/ano**. Se tudo chegasse no ano 5 seria (917/360)\^(1/5) − 1 ≈ 20,6%. O dividendo antecipado faz subir a IRR.
  - Com o dividendo no **ano 1**, o MOIC é o mesmo (2,55×) mas a **IRR passa a 23,9%**.
- **Lição:** a IRR premeia cash antecipado e é o número que se anuncia. Por isso os fundos gostam de dividend recaps. Há quem critique que alguns fundos "gerem o relógio" mais do que a empresa.

#### Explore: anuidade de uma seguradora

Oferta: pagar 100.000 € hoje para receber 6.000 €/ano durante 25 anos. A brochura vende "150.000 € garantidos, ganho de 50%!".

- **IRR ≈ 3,4%/ano.** Os "50%" ignoram o valor temporal do dinheiro, por isso a apresentação é enganadora.
- Para a IRR chegar a 4%, o pagamento anual teria de ser ≈ **6.401 €**.

### 1.4 O problema da reforma: a intuição falha com juros compostos

Tens 55 anos e reformas-te aos 60. Fazes 5 depósitos anuais (no início de cada ano) a 7%. Dos 60 em diante queres levantar 30.000 € no início de cada ano durante 8 anos. Quanto depositas por ano?

- A conta "intuitiva" é 8 × 30.000 / 5 = 48.000 €/ano. **Está errada**: ignora os juros nos dois sentidos (os depósitos rendem enquanto esperam e o saldo continua a render durante a reforma).
- Condição correta, com PV das contribuições = PV dos levantamentos:

$$
Contribution = \sum_{t=n_c}^{n_c+n_p-1} \frac{Payout}{(1+r)^t} \Bigg/ \sum_{t=0}^{n_c-1} \frac{1}{(1+r)^t}
$$

```py
r = 0.07; payout_value = 30_000
payout_years = 8; contribution_years = 5

PV_payout = 0
for t in range(contribution_years, contribution_years + payout_years):
    PV_payout = PV_payout + payout_value/(1+r)**t

sum_discount_rates = 0
for t in range(0, contribution_years):
    sum_discount_rates = sum_discount_rates + 1/(1+r)**t

contribution = PV_payout / sum_discount_rates
print(f"The required annual contribution is {contribution:,.2f} Euro")   # 31,150.60
```

- Resultado: **≈ 31.150 €/ano**, não 48.000 €. Os juros fazem mais de 1/3 da poupança num horizonte de apenas 13 anos.
- **Python novo:** o ciclo `for t in range(a, b)` percorre t = a, …, b−1 e vai acumulando a soma. `30_000` é o mesmo que 30000 (o `_` só serve para legibilidade).

#### Prática: a década mais valiosa da tua vida (7%, levantar 30.000 €/ano dos 65 aos 84)

- Começar aos **25** (40 contribuições): ≈ **1.592 €/ano**.
- Começar aos **35** (30 contribuições): ≈ **3.365 €/ano**, mais do dobro e não apenas +1/3.
- **Lição:** 10 anos de atraso fazem mais do que duplicar o esforço, por causa da capitalização composta.

### 1.5 Prática: as letras pequenas de um crédito automóvel

Empréstimo de 15.000 € a 48 meses, taxa anual de 15%, que o banco converte em 15%/12 = 1,25%/mês. Pagamentos no fim de cada mês. É o problema da reforma ao contrário: os 15.000 € = PV das 48 prestações.

$$
PV = \sum_{t=1}^{n \times m} \frac{payment}{(1+r/m)^t} \;\Rightarrow\; payment = PV \cdot \frac{r/m}{1-(1+r/m)^{-nm}}
$$

- Prestação com 1,25%/mês: **≈ 417,46 €**.
- **Explore:** 1,25%/mês capitaliza para (1,0125)\^12 − 1 = **16,08% de taxa anual efetiva**, não 15%.
- Com a taxa mensal equivalente exata, (1,15)\^(1/12) − 1, a prestação seria **≈ 410,33 €** (cerca de 7 €/mês menos).
- Os bancos anunciam a taxa nominal (15%), que parece mais baixa do que o custo efetivo.

### Ideias-chave da Lecture 1

1. **Valor temporal do dinheiro:** só se comparam cash flows depois de os descontar para o mesmo momento.
2. **A taxa de desconto é o custo de oportunidade**, e o resultado é extremamente sensível a ela em horizontes longos.
3. **NPV > 0 → investir.** A **IRR** é a taxa que anula o NPV e serve para avaliar qualquer oferta "pagar agora, receber depois".
4. **MOIC vs. IRR:** o múltiplo ignora o tempo e a IRR premeia cash antecipado.
5. **Juros compostos** enganam a intuição: na reforma, começar cedo vale muito mais do que parece.
6. **Taxa nominal ≠ taxa efetiva:** lê sempre as letras pequenas.
7. **Ferramentas Python:** f-strings, `lambda`, `scipy.optimize.fsolve`, `np.linspace`, ciclos `for` com `range`, gráficos com `plt.plot`.

### Armadilhas da Lecture 1

- **Somar cash flows sem descontar:** 5 × 100 € = 500 € "no papel", mas o PV a 4% é 445,18 €.
- **3× os cash flows ≠ 3× o PV:** o Investimento 2 tem 3× o dinheiro do Investimento 1, mas o PV é menos de 3×, porque o dinheiro chega mais tarde.
- **NPV e IRR dizem o mesmo** (para um investimento normal: paga-se primeiro, recebe-se depois): NPV > 0 ⇔ IRR > taxa de desconto.
- **A curva do NPV é decrescente na taxa** e cruza o zero na IRR.
- **MOIC ignora o tempo:** o mesmo MOIC (2,55×) pode ter IRRs diferentes (21,8% vs. 23,9%). Cash mais cedo → IRR mais alta.
- **"Ganho de 50%"** numa brochura não é um retorno anual: a IRR real da anuidade da seguradora é ≈ 3,4%/ano.
- **Nominal ≠ efetiva:** 15% com capitalização mensal = (1 + 0,15/12)\^12 − 1 = 16,08% efetiva.
- **Reforma "intuitiva" (48.000 €) está errada:** ignora os juros. O valor certo é ≈ 31.150 €.
- **Início vs. fim do ano:** pagamentos no início descontam com expoente 0, 1, 2…; no fim, com 1, 2, 3… Errar isto muda o resultado.
- **Horizontes longos amplificam a taxa:** Louisiana a 3% → 11 mil milhões; a 7% → 53,5 biliões.
- **Python:** `**` é potência (`^` não é); `=` atribui e `==` compara; `range(a, b)` exclui o `b`; `fsolve` precisa de um palpite inicial e devolve um array (`IRR[0]`).
- **Bom modelo (Week 1):** cálculos podem ser complexos, mas a interface deve ser simples. Desenhar o layout primeiro tem ROI de mais de 10×.

### Números de referência da Lecture 1

| Exemplo | Resultado |
| --- | --- |
| Investimento 1 (5 × 100 €, 4%) | PV = 445,18 € |
| Investimento 2 (100…500 €, 4%) | PV = 1.300,65 €; comprar por 1.500 € → NPV ≈ −199 € |
| Ativo de 600 €, 100 €/ano × 10 anos, 8% | NPV = +71,01 € · IRR = 10,56% |
| Investimento 2 comprado por 800 € | IRR ≈ 19–20% |
| TascaCo (LBO) | MOIC 2,55× · IRR 21,8% (dividendo no ano 3) / 23,9% (ano 1) |
| Anuidade da seguradora (100k → 6k × 25) | IRR ≈ 3,4%; para 4% seriam 6.401 €/ano |
| Reforma (5 depósitos, 8 levantamentos de 30k, 7%) | 31.150,60 €/ano (não 48.000 €) |
| Começar a poupar aos 25 vs. 35 | 1.592 vs. 3.365 €/ano |
| Crédito automóvel (15k, 48 meses, 15%) | 417,46 €/mês · efetiva 16,08% · com taxa exata 410,33 € |
| Louisiana: taxa implícita até ao PIB atual | ≈ 6,7% |

### Testa-te: Lecture 1 (e Week 1)

**1.** Um banco anuncia 15% ao ano, com prestações mensais a 15%/12. Qual é a taxa anual efetiva?<br>(a) 15% · (b) 16,08% · (c) 18% · (d) 1,25%

<details>
<summary>Resposta</summary>

**(b)**. (1 + 0,15/12)\^12 − 1 = (1,0125)\^12 − 1 = 16,08%. A capitalização mensal faz o custo real ser maior do que a taxa anunciada.

</details>

**2.** Dois fundos de private equity investem 360M e recebem no total 917M (MOIC 2,55×). O fundo A recebe um dividendo de 100M no ano 1, o fundo B no ano 3; ambos vendem por 817M no ano 5. Qual tem a IRR mais alta?<br>(a) A · (b) B · (c) Igual, porque o MOIC é igual · (d) Não dá para saber

<details>
<summary>Resposta</summary>

**(a)**. A IRR premeia cash antecipado: 23,9% (A) vs. 21,8% (B). O MOIC é o mesmo porque ignora o tempo.

</details>

**3.** Um ativo tem IRR de 10,56% e o teu custo de oportunidade é 8%. O que podes dizer sobre o NPV a 8%?<br>(a) É positivo, compra · (b) É negativo, não compra · (c) É zero · (d) Não dá para saber sem os cash flows

<details>
<summary>Resposta</summary>

**(a)**. Se a IRR > taxa de desconto, o NPV a essa taxa é positivo (a curva do NPV é decrescente e só cruza o zero na IRR). Aqui NPV = +71,01 €.

</details>

**4.** O que dá `list(range(0, 30, 5))`?<br>(a) \[0, 5, 10, 15, 20, 25, 30\] · (b) \[5, 10, 15, 20, 25, 30\] · (c) \[0, 5, 10, 15, 20, 25\] · (d) \[0, 30, 5\]

<details>
<summary>Resposta</summary>

**(c)**. O `stop` (30) não é incluído.

</details>

**5.** Qual destas **não** é uma característica de um bom modelo, segundo a Week 1?<br>(a) Fluxo lógico claro e componentes geríveis · (b) Pressupostos implícitos para simplificar a interface · (c) Fácil de calibrar com dados históricos · (d) Reutilizável e atualizável

<details>
<summary>Resposta</summary>

**(b)**. Um bom modelo não tem pressupostos implícitos nem consequências não intencionais. A interface deve ser simples, mas os pressupostos têm de estar explícitos e documentados.

</details>

**6. (cálculo)** Quanto vale hoje 100 € recebidos daqui a 5 anos, com r = 4%? Escreve a linha de Python.

<details>
<summary>Resposta</summary>

PV = 100 / 1,04\^5 ≈ **82,19 €**.

```py
PV = 100 / (1 + 0.04)**5
```

</details>

**7. (aberta)** Tens 55 anos e queres levantar 30.000 € por ano durante 8 anos a partir dos 60, depositando durante 5 anos a 7%. Um colega diz que tens de depositar 48.000 €/ano. Explica o erro e qual é a condição certa.

<details>
<summary>Resposta</summary>

- 8 × 30.000 / 5 = 48.000 € ignora os juros: os depósitos rendem até à reforma e o saldo continua a render enquanto levantas.
- A condição certa é **PV das contribuições = PV dos levantamentos**, ambos descontados para hoje. As contribuições (início do ano) usam expoentes 0–4 e os levantamentos 5–12.
- Resultado: ≈ **31.150 €/ano**, mais de 1/3 a menos.

</details>

**Refaz no notebook, sem olhar para as soluções:** 1.1 Practice (Louisiana a 3% e 7%), 1.2 Practice (NPV do ativo de 600 €), 1.3 Practice (IRR do mesmo ativo e da TascaCo), 1.4 "a década mais valiosa" e 1.5 crédito automóvel.
