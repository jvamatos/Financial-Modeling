# Python básico (DataCamp)

> Resumo exportado das notas em Notion (18/11/2026).

## Introduction to Python for Finance (DataCamp)

### Capítulo 1 – Welcome to Python

#### Ambiente de trabalho

- **Shell (IPython):** executa uma linha de cada vez e mostra logo o resultado. Serve para testar.
- **Script (.py):** ficheiro com várias linhas executadas em sequência. É onde se guarda uma análise reprodutível.
- `print()` mostra resultados no output. Num script, sem `print` não aparece nada.
- Comentários começam com `#`, o Python ignora-os.

#### Python como calculadora

```py
+  -  *  /     # soma, subtração, multiplicação, divisão
**             # potência: 2 ** 3 = 8
%              # resto da divisão: 7 % 3 = 1
```

Exemplo financeiro, juro composto: `100 * 1.05 ** 10` dá o valor de 100 € ao fim de 10 anos a 5%.

#### Variáveis

- Guardam valores com um nome: `price = 120`.
- Os nomes são sensíveis a maiúsculas (`Price` ≠ `price`), não podem começar por número e não podem usar palavras reservadas.

```py
price = 120
earnings = 6
pe_ratio = price / earnings   # 20.0
```

#### P/E ratio (Price-to-Earnings)

- P/E = preço por ação ÷ lucro por ação (EPS, *earnings per share*).
- Diz quantos euros/dólares pagas por cada 1 de lucro da empresa.
- Um P/E alto quer dizer que o mercado espera mais crescimento, ou então que a ação está cara.

#### Tipos de dados

- `int` → `10` → números inteiros (nº de ações)
- `float` → `10.5` → números decimais (preços)
- `str` → `'Apple'` → texto (nomes, setores)
- `bool` → `True` / `False` → resultados de comparações
- `type(x)` diz o tipo de uma variável.
- **Conversões:** `int()`, `float()`, `str()`, `bool()`. Ex.: `"P/E: " + str(pe_ratio)`.
- Operações dependem do tipo: `"a" + "b"` dá `"ab"`, mas `"a" + 1` dá erro.

---

### Capítulo 2 – Lists

#### Criar listas

```py
prices = [159.54, 37.13, 71.17]
names = ['Apple', 'Coca-Cola', 'Walmart']
```

- Guardam vários valores numa só variável e podem misturar tipos.

#### Indexação (começa em 0)

```py
names[0]    # 'Apple'  (primeiro)
names[-1]   # 'Walmart' (último)
```

#### Slicing \[início:fim\] — o fim não é incluído

```py
names[0:2]  # ['Apple', 'Coca-Cola']
names[:2]   # do início até ao índice 1
names[1:]   # do índice 1 até ao fim
```

#### Listas aninhadas (como uma tabela)

```py
stocks = [names, prices]
stocks[1][0]   # 159.54 → lista 1 (preços), elemento 0
```

#### Funções vs. métodos

- **Função:** recebe o objeto como argumento, `funcao(lista)`.
  - `len()` dá o nº de elementos, `max()` e `min()` o maior e o menor, `sorted()` devolve uma cópia ordenada.
- **Método:** pertence ao objeto, `lista.metodo()`.
  - `.append(x)` acrescenta um elemento.
  - `.extend([x, y])` acrescenta vários.
  - `.index(x)` dá a posição de `x`.
  - `.sort()` ordena a própria lista (altera-a).

Exemplo: encontrar a empresa com o preço máximo

```py
max_price = max(prices)
idx = prices.index(max_price)
names[idx]
```

#### Packages

- Código já escrito que se importa: `import numpy as np`.
- Também se pode importar só uma parte: `from numpy import array`.

**Limitação das listas:** não fazem cálculos elemento a elemento (`prices / earnings` dá erro). Isto motiva o capítulo seguinte.

---

### Capítulo 3 – Arrays in Python (NumPy)

#### Arrays NumPy

```py
import numpy as np
prices_array = np.array(prices)
```

- Todos os elementos têm o **mesmo tipo**. Se misturares, o NumPy converte tudo (ex.: para texto).
- Fazem **operações elemento a elemento**:

```py
pe = prices_array / earnings_array   # P/E de todas as empresas de uma vez
prices_array * 1.1                   # aumento de 10% em todos os preços
```

- Atenção: `+` entre listas concatena, entre arrays soma.

#### Arrays 2D

```py
stock_array = np.array([[1, 2, 3], [4, 5, 6]])
stock_array.shape   # (2, 3) → linhas, colunas
stock_array.size    # 6 elementos
stock_array[0, 2]   # linha 0, coluna 2 → 3
stock_array[:, 1]   # coluna 1 inteira
```

- `np.transpose()` troca linhas com colunas.

#### Funções estatísticas

```py
np.mean(arr)    # média
np.std(arr)     # desvio padrão (volatilidade/dispersão)
```

#### Sequências

```py
np.arange(start, stop, step)
np.arange(1, 8)      # [1 2 3 4 5 6 7] (stop excluído)
np.arange(1, 8, 2)   # [1 3 5 7]
```

#### Indexação com arrays

```py
months[[1, 3, 5]]    # elementos nas posições 1, 3 e 5
months[[-1, -2]]     # último e penúltimo
```

#### Indexação booleana (o conceito mais importante do curso)

```py
boolean_array = prices > np.mean(prices)   # [True False True ...]
above_avg = prices[boolean_array]          # só os preços acima da média

mask = sectors == 'Health Care'
health_care = names[mask]                  # só empresas de saúde
```

Primeiro cria-se uma "máscara" de True/False com uma condição e depois aplica-se a outro array para filtrar.

---

### Capítulo 4 – Visualization in Python (Matplotlib)

```py
import matplotlib.pyplot as plt
```

#### Gráficos de linha (evolução ao longo do tempo)

```py
plt.plot(days, prices, color='red', linestyle='--')
plt.show()
```

- Cores: `'red'`, `'green'`, `'blue'`...
- Estilos de linha: `'-'` (sólido), `'--'` (tracejado), `':'` (pontilhado), `'-.'`.
- Para várias séries, chama-se `plt.plot()` mais vezes antes do `plt.show()`.

#### Etiquetas

```py
plt.xlabel('Days')
plt.ylabel('Prices, $')
plt.title('Company Stock Prices Over Time')
```

#### Scatter plots

```py
plt.scatter(days, prices, color='green', s=0.1)   # s = tamanho dos pontos
```

#### Histogramas (distribuição dos dados)

```py
plt.hist(prices, bins=100)
```

- Em finanças servem para ver se retornos/preços seguem uma **distribuição normal** ou são **enviesados (skewed)**, medir a **variabilidade** e identificar **outliers**.
- `bins` = nº de intervalos. Mais bins → mais detalhe e menos observações por barra.
- `density=True` normaliza (frequências relativas em vez de contagens).
- `alpha=0.4` dá transparência, útil para sobrepor dois histogramas.

#### Legendas

```py
plt.hist(stock_A, bins=100, alpha=0.4, label='Stock A')
plt.hist(stock_B, bins=100, alpha=0.4, label='Stock B')
plt.legend()
plt.show()
```

A ação com o histograma mais "largo" é a mais volátil.

---

### Capítulo 5 – Case study: S&P 100

O S&P 100 é um índice com 100 das maiores empresas dos EUA, de vários setores. Dados: 4 listas — `names`, `prices`, `earnings` (EPS) e `sectors`.

#### Passo 1 – Explorar as listas

```py
names[0:4]                                        # primeiras 4 empresas
names[-1], prices[-1], earnings[-1], sectors[-1]  # Exxon Mobil, 80.31, 3.56, Energy
```

#### Passo 2 – Converter em arrays e calcular o P/E

```py
prices_array = np.array(prices)
earnings_array = np.array(earnings)
pe = prices_array / earnings_array
```

#### Passo 3 – Filtrar por setor

```py
it_pe = pe[sectors == 'Information Technology']
cs_pe = pe[sectors == 'Consumer Staples']
```

#### Passo 4 – Estatísticas por setor

- **Information Technology:** P/E médio ≈ 26,3 · desvio padrão ≈ 10,9
- **Consumer Staples:** P/E médio ≈ 21,6 · desvio padrão ≈ 4,4

Leitura: a tecnologia tem expectativas de crescimento mais altas e muito mais heterogéneas. Os bens de consumo essenciais (Coca-Cola, P&G, Walmart...) são mais estáveis e previsíveis.

#### Passo 5 – Visualizar

- Scatter com os P/E dos dois setores (vermelho = IT, verde = CS): uma empresa de IT destaca-se muito acima das outras.
- Histograma de `it_pe` com 8 bins confirma um valor isolado acima de 50.

#### Passo 6 – Identificar o outlier

```py
outlier_price = it_pe[it_pe > 50]
outlier_name = it_names[it_pe > 50]
# "In 2017, Paypal Holdings had an abnormally high P/E ratio of 54.68."
```

---

### Ideias-chave

1. **Python básico:** variáveis, tipos e conversões são a base de qualquer cálculo financeiro.
2. **Listas** servem para guardar e organizar dados. **Arrays** servem para calcular com eles.
3. **Vetorização:** com NumPy calculas indicadores (P/E, retornos, variações) para centenas de ativos numa linha, sem ciclos.
4. **Filtros booleanos:** a forma de responder a perguntas do tipo "quais as empresas que...?".
5. **Média e desvio padrão** resumem nível e dispersão (risco) de um grupo.
6. **Visualizar antes de concluir:** linhas para tendências, scatters para comparar, histogramas para distribuições e outliers.

**Próximos passos no DataCamp:** *Intermediate Python* (dicionários, pandas, ciclos), *Introduction to Portfolio Analysis in Python* e *Importing and Managing Financial Data in Python*.
