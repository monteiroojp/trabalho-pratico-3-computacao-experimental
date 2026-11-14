import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

#Leitura e cálculo dos gols por rodada
df = pd.read_csv("./partidas_detalhadas_2024.csv")
gols_rodada = [0 for i in range (39)]

#Total de gols em cada rodada
for linha in df.itertuples():
    gols_rodada[linha.rodada] += linha.gols_marcados + linha.gols_sofridos

for i in range(1,39):
    gols_rodada[i]  = int(gols_rodada[i]/2)

#Separação em turnos
gols_primeiro_turno = gols_rodada[1:20]
gols_segundo_turno = gols_rodada[20:39]

#Medianas(Apenas para exibição)
mediana_t1 = pd.Series(gols_primeiro_turno).median()
mediana_t2 = pd.Series(gols_segundo_turno).median()
print(f"Mediana 1º Turno: {mediana_t1} gols/rodada")
print(f"Mediana 2º Turno: {mediana_t2} gols/rodada\n")

#Teste estatístico
stat_u, p_valor = stats.mannwhitneyu(gols_primeiro_turno, gols_segundo_turno, alternative="greater")
print(f"Estatística W: {stat_u:.4f}")
print(f"Valor-p: {p_valor:.4f}")

alpha = 0.05
if p_valor < alpha:
    print("Rejeita H0: ")
else:
    print("Confima H0: ")

alpha = 0.05
if p_valor < alpha:
  print("Rejeita H0: há evidência estatística de que o 2º turno tem menos gols por rodada que o 1º.")
else:
  print("Não rejeita H0: não há evidência estatística de que o 2º turno tenha menos gols que o 1º.")

# 5. Visualização: Boxplots lado a lado (Gerado com IA)
sns.set_theme(style="whitegrid")

df_turnos = pd.DataFrame({
    "Turno": (
        ["1º Turno (Rodadas 1–19)"] * len(gols_primeiro_turno)
        + ["2º Turno (Rodadas 20–38)"] * len(gols_segundo_turno)
    ),
    "Total de Gols": gols_primeiro_turno + gols_segundo_turno,
})

plt.figure(figsize=(8, 5))
ax = sns.boxplot(
    data=df_turnos,
    x="Turno",
    y="Total de Gols",
    hue="Turno",
    palette=["#4C72B0", "#DD8452"],
    legend=False,
    width=0.45,
)
sns.stripplot(
    data=df_turnos,
    x="Turno",
    y="Total de Gols",
    color="black",
    alpha=0.6,
    jitter=0.07,
    ax=ax,
)

plt.title(
    "Distribuição do Total de Gols por Rodada: 1º Turno vs. 2º Turno",
    fontsize=12,
)
plt.xlabel("")
plt.ylabel("Total de Gols na Rodada")
plt.tight_layout()
plt.show()