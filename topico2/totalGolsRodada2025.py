import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats

#Leitura e cálculo dos gols por rodada
df = pd.read_csv("./partidas_detalhadas_2025.csv")
gols_rodada = [0 for i in range (39)]

for linha in df.itertuples():
    gols_rodada[linha.rodada] += linha.gols_marcados + linha.gols_sofridos

for i in range(1,39):
    gols_rodada[i]  = int(gols_rodada[i]/2)

#Gráfico Q-Q Plot
dados = gols_rodada[1:39]
stats.probplot(dados, dist="norm", plot=plt)
plt.title("Q-Q Plot - Total de Gols por Rodada")
plt.xlabel("Quantis Teóricos (Normal)")
plt.ylabel("Quantis Observados")
plt.grid(True)
plt.show()

#Teste de hipótese
#H0 : Os dados de total de gols por rodada seguem uma distribuição normal
#H1 : Os dados não seguem a distribuição normal
stat, p_valor = stats.shapiro(dados)
print(f"Estatística W: {stat:.4f}")
print(f"Valor-p: {p_valor:.4f}")

alpha = 0.05
if p_valor > alpha:
  print("Não rejeita H0: Os dados seguem uma distribuição normal.")
else:
  print("Rejeita H0: Os dados não seguem uma distribuição normal.")

