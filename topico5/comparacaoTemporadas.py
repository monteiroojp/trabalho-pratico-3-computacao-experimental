import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats

#Leitura e cálculo dos gols por rodada
df = pd.read_csv("./partidas_detalhadas_2021.csv")
gols_rodada_2021 = [0 for i in range (39)]

for linha in df.itertuples():
    gols_rodada_2021[linha.rodada] += linha.gols_marcados + linha.gols_sofridos

for i in range(1,39):
    gols_rodada_2021[i]  = int(gols_rodada_2021[i]/2)


df = pd.read_csv("./partidas_detalhadas_2025.csv")
gols_rodada_2025 = [0 for i in range (39)]

for linha in df.itertuples():
    gols_rodada_2025[linha.rodada] += linha.gols_marcados + linha.gols_sofridos

for i in range(1,39):
    gols_rodada_2025[i]  = int(gols_rodada_2025[i]/2)