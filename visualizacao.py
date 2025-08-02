#%%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from analise import maior_aproveit_geral, maior_aproveit_ciclo, stats_gerais, df_brasileirao_ciclo_geral, decada_2000, decada_2010, decada_2020, df_ranking_stats, df_brasileirao_top_5


# %% visualização dos maiores pontuadores

plt.figure(figsize=(20, 12))
sns.barplot(x=stats_gerais.index, y=stats_gerais["points"], width=0.6)
plt.suptitle("Maiores Pontuadores do Brasileirão (2003-2024)", fontsize=20)
plt.title("Times que jogaram ao menos 3 temporadas", fontsize=18)
plt.xlabel("Times", fontsize=16)
plt.ylabel("Pontos", fontsize=16)
plt.bar_label(plt.gca().containers[0], fontsize=14, rotation=45)
plt.xticks(rotation=90, fontsize = 14)
plt.yticks(fontsize = 14)
plt.show()
# %%
plt.figure(figsize=(20, 12))
sns.barplot(x=maior_aproveit_geral["team"], y=maior_aproveit_geral["percentage"], width=0.6)
plt.suptitle("Maiores Aproveitamentos do Brasileirão (2003-2024)", fontsize=20)
plt.title("Times que jogaram ao menos 3 temporadas", fontsize=18)
plt.xlabel("Times", fontsize=16)
plt.ylabel("Aproveitamento (%)", fontsize=16)
plt.bar_label(plt.gca().containers[0], fontsize=14)
plt.xticks(rotation=30, fontsize=14)
plt.yticks(fontsize=14)

plt.show()

# %% visualização dos melhores ciclos (4 anos) por aproveitamento
plt.figure(figsize=(20, 12))
ax = sns.barplot(x=maior_aproveit_ciclo["ciclo"], y=maior_aproveit_ciclo["percentage"], hue=maior_aproveit_ciclo["team"], dodge=True)
plt.suptitle("Melhores Ciclos(4 anos) do Brasileirão (2003-2024)", fontsize=20)
plt.title("Top 10 Times, Ciclos com Melhor Aproveitamento", fontsize=18)
plt.xlabel("Ciclos", fontsize=16)
plt.ylabel("Aproveitamento (%)", fontsize=16)

# Adiciona o valor da porcentagem em cima de cada barra
for container in ax.containers:
    plt.bar_label(container, labels=[f"{v:.2f}%" for v in container.datavalues], fontsize=14, rotation=60)

plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend(title="Times", fontsize=14, title_fontsize=16, loc="lower center")
plt.show()

# %%
plt.figure(figsize=(20, 15), dpi = 400)
ax = sns.barplot(y=df_brasileirao_ciclo_geral["ciclo"], x=df_brasileirao_ciclo_geral["percentage"], hue=df_brasileirao_ciclo_geral["team"], dodge=True)
plt.suptitle("Melhores Ciclos(4 anos) do Brasileirão (2003-2024)", fontsize=20)
plt.title("Top 10 Times, Ciclos com Melhor Aproveitamento", fontsize=18)
plt.ylabel("Ciclos", fontsize=16)
plt.xlabel("Aproveitamento (%)", fontsize=16)

# Adiciona o valor da porcentagem em cima de cada barra
for container in ax.containers:
    plt.bar_label(container, labels=[f"{v:.2f}%" for v in container.datavalues], fontsize=14)

plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend(title="Times", fontsize=14, title_fontsize=16, loc="lower left")
plt.show()

# %%
# Supondo que df_ranking_stats já tem a coluna "Média de Posições"
plt.figure(figsize=(12, 6))
sns.boxplot(x=df_ranking_stats["Média de Posições Geral"], color="lightblue")
sns.stripplot(x=df_ranking_stats["Média de Posições Geral"], color="gray", size=8, jitter=True)

# Destaca o Vasco
vasco_media = df_ranking_stats.loc[df_ranking_stats["Time"] == "Vasco", "Média de Posições Geral"].values[0]
plt.scatter(vasco_media, 0, color="red", s=150, label="Vasco")

plt.title("Distribuição da Média de Posições Gerais dos Times", fontsize=16)
plt.xlabel("Média de Posições", fontsize=14)
plt.legend()
plt.show()

# %% decada 2000 - times top 5 (São Paulo, Palmeiras, Flamengo, Corinthians, Internacional)
plt.figure(figsize=(20, 12))
sns.lineplot(data=decada_2000, x="season", y="place", hue="team", marker="o")
plt.title("Média de Posições dos Times Top 5 (2003-2009)", fontsize=24)
plt.xlabel("Temporada", fontsize=20)
plt.ylabel("Média de Posições", fontsize=20)
plt.xticks(fontsize=18)
y_values = sorted(decada_2000["place"].unique())
plt.yticks(y_values, fontsize=18)
plt.legend(title="Times", fontsize=18, title_fontsize=22)
plt.grid(True)
plt.ylim(20, 0)
plt.show()

# %% decada 2010 - times top 5 (São Paulo, Palmeiras, Flamengo, Corinthians, Internacional)
plt.figure(figsize=(20, 12))
sns.lineplot(data=decada_2010, x="season", y="place", hue="team", marker="o")
plt.title("Média de Posições dos Times Top 5 (2010-2019)", fontsize=24)
plt.xlabel("Temporada", fontsize=20)
plt.ylabel("Média de Posições", fontsize=20)
plt.xticks(fontsize=18)
y_values = sorted(decada_2010["place"].unique())
plt.yticks(y_values, fontsize=18)
plt.legend(title="Times", fontsize=18, title_fontsize=22)
plt.grid(True)
plt.ylim(20, 0)
plt.show()

# %% decada 2020 - times top 5 (São Paulo, Palmeiras, Flamengo, Corinthians, Internacional)
plt.figure(figsize=(20, 12))
sns.lineplot(data=decada_2020, x="season", y="place", hue="team", marker="o")
plt.title("Média de Posições dos Times Top 5 (2020-2024)", fontsize=24)
plt.xlabel("Temporada", fontsize=20)
plt.ylabel("Média de Posições", fontsize=20)
plt.xticks(fontsize=18)
y_values = sorted(decada_2020["place"].unique())
plt.yticks(y_values, fontsize=18)
plt.legend(title="Times", fontsize=18, title_fontsize=22)
plt.grid(True)
plt.ylim(20, 0)
plt.show()

# %% Gráfico geral dos times top 5 (São Paulo, Palmeiras, Flamengo, Corinthians, Internacional) de 2002 a 2024
plt.figure(figsize=(20, 12))
sns.lineplot(data=df_brasileirao_top_5, x="season", y="place", hue="team", marker="o")
plt.title("Média de Posições dos Times Top 5 (2002-2024)", fontsize=24)
plt.xlabel("Temporada", fontsize=20)
plt.ylabel("Média de Posições", fontsize=20)
plt.xticks(fontsize=18)
y_values = sorted(df_brasileirao_top_5["place"].unique())
plt.yticks(y_values, fontsize=18)
plt.legend(title="Times", fontsize=18, title_fontsize=22)
plt.grid(True)
plt.ylim(20, 0)
plt.show()
# %%
from analise import df_brasileirao_top_3

plt.figure(figsize=(20, 12))
sns.lineplot(data=df_brasileirao_top_3, x="season", y="place", hue="team", marker="o")
plt.title("Posições dos 3 Times com estatísticas mais consistentes (2002-2024)", fontsize=24)
plt.xlabel("Temporada", fontsize=20)
plt.ylabel("Posição", fontsize=20)
x_values = df_brasileirao_top_3["season"].unique()
plt.xticks(x_values, fontsize=18, rotation=90)
y_values = sorted(df_brasileirao_top_3["place"].unique())
plt.yticks(y_values, fontsize=18)
plt.legend(title="Times", fontsize=18, title_fontsize=22)
plt.grid(True)
plt.ylim(20, 0)
plt.show()

# %%
