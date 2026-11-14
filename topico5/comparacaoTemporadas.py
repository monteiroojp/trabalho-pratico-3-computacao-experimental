import pandas as pd
import scipy.stats as stats
import random

#Leitura e cálculo dos gols por rodada em 2021
df = pd.read_csv("./partidas_detalhadas_2021.csv")
gols_rodada_2021 = [0 for i in range (39)]

for linha in df.itertuples():
    gols_rodada_2021[linha.rodada] += linha.gols_marcados + linha.gols_sofridos

for i in range(1,39):
    gols_rodada_2021[i]  = int(gols_rodada_2021[i]/2)

#Leitura e cálculo dos gols por rodada em 2025
df = pd.read_csv("./partidas_detalhadas_2025.csv")
gols_rodada_2025 = [0 for i in range (39)]

for linha in df.itertuples():
    gols_rodada_2025[linha.rodada] += linha.gols_marcados + linha.gols_sofridos

for i in range(1,39):
    gols_rodada_2025[i]  = int(gols_rodada_2025[i]/2)

gols_rodada_2021 = gols_rodada_2021[1:39]
gols_rodada_2025 = gols_rodada_2025[1:39]

#Hipóteses
#H0 :Não há diferença significativa no número de gols por rodada entre as duas temporadas
#H1: Há diferença significativa no número de gols por rodada entre as duas temporadas
alpha = 0.05

#Teste paramétrico
t_stat, p_valor = stats.ttest_rel(gols_rodada_2025, gols_rodada_2021, alternative="two-sided")
print("Para o teste paramétrico:")
print(f"Estatística t: {t_stat:.4f}")
print(f"Valor-p: {p_valor:.4f}")
if p_valor < alpha:
    print("Rejeita H0: Há evidência significativa que o número de gols por rodada diferente entre as duas temporadas\n")
else:
    print("Não rejeita H0: Não há evidência significativa que o número de gols por rodada diferente entre as duas temporadas\n")

#Teste de sinais
# Teste de Sinais
positivos = 0
negativos = 0
empates = 0

#Calcula todas diferenças de gols em cada rodadas, para determinação do postos positivos e negativos, além dos empates
for i in range(len(gols_rodada_2025)):
  diferenca = gols_rodada_2025[i] - gols_rodada_2021[i]

  if diferenca > 0: positivos += 1
  elif diferenca < 0: negativos += 1
  else: empates += 1

total_validos = positivos + negativos
resultado = stats.binomtest(
    positivos, n=total_validos, p=0.5, alternative="two-sided"
)
p_valor = resultado.pvalue

print("Para o Teste de Sinais:")
print(f"Valor-p: {p_valor:.4f}")

if p_valor < alpha:
  print("Rejeita H0: Há evidência significativa de que o número de gols por rodada é diferente entre as duas temporadas\n")
else:
  print("Não rejeita H0: Não há evidência significativa de que o número de gols por rodada seja diferente entre as duas temporadas\n")



#Teste de Postos Sinalizados de Wilcoxon
w_stat, p_valor = stats.wilcoxon(gols_rodada_2025, gols_rodada_2021, alternative="two-sided")
print("Para o teste de Postos Sinalizaados de Wilcoxon:")
print(f"Estatística W: {w_stat:.4f}")
print(f"Valor-p: {p_valor:.4f}")
if p_valor < alpha:
    print("Rejeita H0: Há evidência significativa que o número de gols por rodada diferente entre as duas temporadas\n")
else:
    print("Não rejeita H0: Não há evidência significativa que o número de gols por rodada diferente entre as duas temporadas\n")


#Replicação do código acima, porém pegando uma subamostra aleatória de tamanho significativamente menor(15) para ver se o desempenho dos testes são afetados
#Semente para aleatorização
random.seed(42)

#Tamanho da subamostra
n_subamostra = 15

#Sorteia 15 posições
indices_sorteados = random.sample(range(len(gols_rodada_2025)), n_subamostra)

#Montagem das duas subamostras
sub_2021 = []
sub_2025 = []
for idx in indices_sorteados:
  sub_2021.append(gols_rodada_2021[idx])
  sub_2025.append(gols_rodada_2025[idx])

print("*TESTE COM AS SUBAMOSTRAS*\n")
#Teste paramétrico
t_stat, p_valor = stats.ttest_rel(sub_2025, sub_2021, alternative="two-sided")
print("Para o teste paramétrico:")
print(f"Estatística t: {t_stat:.4f}")
print(f"Valor-p: {p_valor:.4f}")
if p_valor < alpha:
    print("Rejeita H0: Há evidência significativa que o número de gols por rodada diferente entre as duas temporadas\n")
else:
    print("Não rejeita H0: Não há evidência significativa que o número de gols por rodada diferente entre as duas temporadas\n")

#Teste de sinais
# Teste de Sinais
positivos = 0
negativos = 0
empates = 0

#Calcula todas diferenças de gols em cada rodadas, para determinação do postos positivos e negativos, além dos empates
for i in range(len(sub_2025)):
  diferenca = sub_2025[i] - sub_2021[i]

  if diferenca > 0: positivos += 1
  elif diferenca < 0: negativos += 1
  else: empates += 1

total_validos = positivos + negativos
resultado = stats.binomtest(
    positivos, n=total_validos, p=0.5, alternative="two-sided"
)
p_valor = resultado.pvalue

print("Para o Teste de Sinais:")
print(f"Valor-p: {p_valor:.4f}")

if p_valor < alpha:
  print("Rejeita H0: Há evidência significativa de que o número de gols por rodada é diferente entre as duas temporadas\n")
else:
  print("Não rejeita H0: Não há evidência significativa de que o número de gols por rodada seja diferente entre as duas temporadas\n")



#Teste de Postos Sinalizados de Wilcoxon
w_stat, p_valor = stats.wilcoxon(sub_2025, sub_2021, alternative="two-sided")
print("Para o teste de Postos Sinalizaados de Wilcoxon:")
print(f"Estatística W: {w_stat:.4f}")
print(f"Valor-p: {p_valor:.4f}")
if p_valor < alpha:
    print("Rejeita H0: Há evidência significativa que o número de gols por rodada diferente entre as duas temporadas\n")
else:
    print("Não rejeita H0: Não há evidência significativa que o número de gols por rodada diferente entre as duas temporadas\n")