from collections import defaultdict
import pandas as pd
import scipy.stats as stats

# Leitura do arquivo
nomes_arquivos = [
    "./partidas_detalhadas_2025.csv",
    "./partidas_detalhadas_2024.csv",
    "./partidas_detalhadas_2023.csv",
    "./partidas_detalhadas_2022.csv",
    "./partidas_detalhadas_2021.csv",
]

gols_z4_total = []
gols_g4_total = []

for nomeArquivo in nomes_arquivos:
  # Reinicia pontos e gols a cada nova temporada
  gols_time = defaultdict(int)
  pontos_time = defaultdict(int)

  df = pd.read_csv(nomeArquivo)

  for linha in df.itertuples():
    pontos = 0
    if linha.gols_marcados == linha.gols_sofridos:
      pontos = 1
    elif linha.gols_marcados > linha.gols_sofridos:
      pontos = 3
    pontos_time[linha.time] += pontos
    gols_time[linha.time] += linha.gols_marcados

  # Ordena por pontos e desempata por gols marcados
  tabela_ordenada = sorted(
      pontos_time.items(), key=lambda item: (item[1], gols_time[item[0]])
  )

  # Pega os 4 primeiros (Z4) e os 4 últimos (G4) da temporada
  z4 = tabela_ordenada[:4]
  g4 = tabela_ordenada[-4:]

  # Guarda o total de gols marcados por cada time do Z4 e do G4
  for time, pontos in z4:
    gols_z4_total.append(gols_time[time])

  for time, pontos in g4:
    gols_g4_total.append(gols_time[time])

print("Gols Z4 (2021-2025):", gols_z4_total)
print("Gols G4 (2021-2025):", gols_g4_total)

# Hipóteses:
# H0: Mediana_G4 = Mediana_Z4 (não há diferença nos gols marcados entre G4 e Z4)
# H1: Mediana_G4 > Mediana_Z4 (os times do G4 marcam mais gols que os do Z4)
stat_u, p_valor = stats.mannwhitneyu(
    gols_g4_total, gols_z4_total, alternative="greater"
)
print(f"\nEstatística U: {stat_u:.4f}")
print(f"Valor-p: {p_valor:.4f}")

alpha = 0.05
if p_valor < alpha:
  print("Rejeita H0: há evidência estatística de que os times do G4 marcam mais gols que os do Z4.")
else:
  print("Não rejeita H0: não há evidência estatística de que os times do G4 marquem mais gols que os do Z4.")