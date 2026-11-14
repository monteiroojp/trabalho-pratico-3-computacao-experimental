from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math

# Leitura do arquivo
df1 = pd.read_csv("./partidas_detalhadas_2021.csv")
gols_time = defaultdict(int)
pontos_time = defaultdict(int)

for linha in df1.itertuples():
    pontos = 0
    if linha.gols_marcados == linha.gols_sofridos:
        pontos = 1
    elif linha.gols_marcados > linha.gols_sofridos:
        pontos = 3
    pontos_time[linha.time] += pontos
    gols_time[linha.time] += linha.gols_marcados


# Organizando os dados agregados por time em um DataFrame
times = list(gols_time.keys())
df_resumo = pd.DataFrame({
    "time": times,
    "gols_marcados": [gols_time[t] for t in times],
    "pontos": [pontos_time[t] for t in times]
})

covariancia = df_resumo["gols_marcados"].cov(df_resumo["pontos"])
print(f"Covariância amostral entre X e Y: {covariancia}")

var_x = df_resumo["gols_marcados"].std()
var_y = df_resumo["pontos"].std()
coef_pearson = covariancia / (var_x * var_y)

print(f"Coeficiente de Correlação de Pearson: {coef_pearson}")

t = coef_pearson * math.sqrt((20 - 2) / (1 - (coef_pearson * coef_pearson)))

print(f"Valor t calculado: {t:.4f}")

print(f"Conferindo a tabela t-sudent, podemos observar que o p-valor de {t:.4f} com 18 graus de liberadade se aproxima muito de 0, isto é, sendo menor do que o alpha = 0.05. Logo, há fortes indícios de que quantos mais gols um time faz, mais pontos o time também faz")

# Gráfico gerado por IA
# Construção do gráfico de dispersão
plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=df_resumo,
    x="gols_marcados",
    y="pontos",
    s=80,
    color="royalblue"
)

# Adiciona o nome de cada time próximo ao respectivo ponto (opcional, ajuda na análise)
for linha in df_resumo.itertuples():
    plt.text(
        linha.gols_marcados + 0.5,
        linha.pontos + 0.5,
        linha.time,
        fontsize=8,
        alpha=0.85
    )


plt.title("Relação entre Gols Marcados e Pontos Conquistados (2021)")
plt.xlabel("Gols Marcados")
plt.ylabel("Pontos")
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("dispersao_gols_pontos.png", dpi=300)
plt.show()