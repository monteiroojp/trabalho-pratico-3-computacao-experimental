from collections import defaultdict
import pandas as pd
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt

#Leitura do arquivo
df = pd.read_csv("./consolidado_gols_2021.csv")
gols_time = defaultdict(int)

#Soma dos gols marcados de acordo com a condição(Visitante ou Mandante)
for linha in df.itertuples():
  gols_time[(linha.time, linha.condicao)] += linha.gols_marcados

#Calculo da media
for (time, condicao), gols in gols_time.items():
    gols_time[(time, condicao)] = gols/19

#Calculo do desempenho
desempenho_time = defaultdict(int)
for (time, condicao), gols in gols_time.items():
   desempenho_time[time] = gols_time[(time, "Mandante")] - gols_time[(time, "Visitante")]


#Hipóteses
#H0 : A mediana das diferenças é igual a 0(Time joga igual como mandante e como visitante)
#H1 : A mediana das diferenças é > 0(Time joga melhor como mandante)
desempenhos = list(desempenho_time.values())
stat, p_valor = stats.wilcoxon(desempenhos, alternative="greater")
print(f"Estatística W: {stat:.4f}")
print(f"Valor-p: {p_valor:.4f}")

alpha = 0.05
if p_valor < alpha:
  print("Rejeita H0: há evidência estatística de que os times marcam mais gols como mandantes.")
else:
  print("Não rejeita H0: não há evidência estatística de vantagem como mandante.")

  # --- VISUALIZAÇÃO COM SEABORN ---(Gerado com IA)
sns.set_theme(style="whitegrid")

times = list(desempenho_time.keys())
medias_mandante = [gols_time[(t, "Mandante")] for t in times]
medias_visitante = [gols_time[(t, "Visitante")] for t in times]

# DataFrame no formato longo (padrão nativo do Seaborn)
df_condicoes = pd.DataFrame({
    "Condição": ["Mandante"] * len(times) + ["Visitante"] * len(times),
    "Média de Gols": medias_mandante + medias_visitante,
})

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))

# 1. Boxplot comparativo entre Mandante e Visitante
sns.boxplot(
    data=df_condicoes,
    x="Condição",
    y="Média de Gols",
    hue="Condição",
    palette=["#4C72B0", "#DD8452"],
    legend=False,
    width=0.5,
    ax=ax1,
)
sns.stripplot(
    data=df_condicoes,
    x="Condição",
    y="Média de Gols",
    color="black",
    alpha=0.55,
    jitter=0.08,
    ax=ax1,
)
ax1.set_title("Média de Gols Marcados por Condição")
ax1.set_xlabel("")
ax1.set_ylabel("Média de Gols por Jogo")

# 2. Boxplot das diferenças pareadas (Mandante - Visitante)
sns.boxplot(y=desempenhos, color="#55A868", width=0.35, ax=ax2)
sns.stripplot(y=desempenhos, color="black", alpha=0.55, jitter=0.05, ax=ax2)
ax2.axhline(
    0, color="red", linestyle="--", linewidth=1.3, label="H0 (Diferença = 0)"
)
ax2.set_xticks([0])
ax2.set_xticklabels(["Desempenho(Mandante - Visitante)"])
ax2.set_title("Distribuição dos Desempenhos Pareados")
ax2.set_ylabel("Diferença na Média de Gols")
ax2.legend()

plt.tight_layout()
plt.show()

