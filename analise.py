# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import kagglehub as kg

path = kg.dataset_download("lucasyukioimafuko/brasileirao-serie-a-2006-2022")
# dataframe do brasileirão de 2003 a 2024
df_brasileirao = pd.read_csv(path + "/brasileirao.csv")
# dataframe dos times
df_times = pd.read_csv(path + "/teams.csv")
# %%
def get_stats_ciclo(df, stat, bool):
    stats_ciclos_completos = df[df["played"] >= 76].copy()
    stats_ciclos_completos = stats_ciclos_completos.sort_values(by=stat, ascending=bool).head(10).reset_index(drop=True)
    return stats_ciclos_completos

def get_stats_temp(df, stat, bool):
    stats_temporadas = df[df["played"] >= 38].copy()
    stats_temporadas = stats_temporadas.sort_values(by=stat, ascending=bool).head(10).reset_index(drop=True)
    return stats_temporadas

# %%
df_brasileirao["percentage"] = round(df_brasileirao["points"] / (df_brasileirao["played"] * 3) * 100, 2)
df_brasileirao[["points_game", "goals_game", "goals_tak_game"]] = round(df_brasileirao[["points", "goals", "goals_taken"]].div(df_brasileirao["played"], axis=0), 2)


# %%
stats_gerais = (df_brasileirao.groupby("team").agg({"points": "sum", "played": "sum", 
                                                        "won": "sum", "draw": "sum", "loss": "sum",
                                                        "goals": "sum", "goals_taken": "sum",
                                                        "points_game": "mean", "goals_game": "mean",
                                                        "goals_tak_game": "mean"})
                                     .query("played > (38 * 3)"))
# %%
maior_aproveitamento_temp = get_stats_temp(df_brasileirao, "goals_tak_game", False)
menor_aproveitamento_temp = get_stats_temp(df_brasileirao, "goals_tak_game", True)

temp_2014 = df_brasileirao[df_brasileirao["season"] == 2014]
temp_2014
# maiores_aproveitamentos = get_stats_temp(stats_gerais, "percentage", False) TO FIX - PAREI AQUIII
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
sns.barplot(x=maiores_aproveitamentos.index, y=maiores_aproveitamentos["percentage"], width=0.6)
plt.suptitle("Maiores Aproveitamentos do Brasileirão (2003-2024)", fontsize=20)
plt.title("Times que jogaram ao menos 3 temporadas", fontsize=18)
plt.xlabel("Times", fontsize=16)
plt.ylabel("Aproveitamento (%)", fontsize=16)
plt.bar_label(plt.gca().containers[0], fontsize=14, rotation=45)
plt.xticks(rotation=90, fontsize=14)
plt.yticks(fontsize=14)

plt.show()
# %%
df_brasileirao_ciclo = df_brasileirao.copy()

# Cria coluna 'ciclo' agrupando as temporadas de 4 em 4 anos
def get_ciclo(season):
    start = 2003 + 4 * ((season - 2003) // 4)
    end = start + 3
    return f"{start}-{end}"

df_brasileirao_ciclo["ciclo"] = df_brasileirao_ciclo["season"].apply(get_ciclo)

# Exemplo de visualização dos ciclos
# print(df_brasileirao_ciclo[["season", "ciclo"]].drop_duplicates().sort_values("season"))
df_brasileirao_ciclo = df_brasileirao_ciclo.drop(columns = ["season", "place"])
df_brasileirao_ciclo = (df_brasileirao_ciclo.groupby(["ciclo", "team"])
                        .agg({
                              "points": "sum",
                              "played": "sum",
                              "won": "sum",
                              "draw": "sum",
                              "loss": "sum",
                              "goals": "sum",
                              "goals_taken": "sum",
                              "goals_diff": "sum"})
                              .reset_index()
                              .assign(percentage=lambda x: x["points"] / (x["played"] * 3) * 100))

# %% cálculo de estatísticas adicionais
df_brasileirao_ciclo["points_game"] = round(df_brasileirao_ciclo["points"] / df_brasileirao_ciclo["played"], 2)
df_brasileirao_ciclo["goals_game"] = round(df_brasileirao_ciclo["goals"] / df_brasileirao_ciclo["played"], 2)
df_brasileirao_ciclo["goals_tak_game"] = round(df_brasileirao_ciclo["goals_taken"] / df_brasileirao_ciclo["played"],2)
df_brasileirao_ciclo["percentage"] = df_brasileirao_ciclo["percentage"].round(2)
df_brasileirao_ciclo


# %% melhores ciclos completos por aproveitamento
ciclos_completos = df_brasileirao_ciclo[df_brasileirao_ciclo["ciclo"] != "2023-2026"].copy()
melhores_ciclos_completos = ciclos_completos.sort_values(by="percentage", ascending=False).head(10).reset_index(drop=True)

# %% Ciclos
"""
Escolher qual estatística para determinar os melhores e piores ciclos completos.
- "percentage": aproveitamento
- "points_game": pontos por jogo
- "goals_game": gols por jogo
- "goals_tak_game": gols sofridos por jogo
- True: Resultados negativos(invertido para o caso de gols sofridos)
- False: Resultados positivos(invertido para o caso de gols sofridos)

"""
get_stats_ciclo(ciclos_completos, "percentage", True)
# %% visualização dos melhores ciclos (4 anos) por aproveitamento
plt.figure(figsize=(20, 12))
ax = sns.barplot(x=melhores_ciclos["ciclo"], y=melhores_ciclos["percentage"], hue=melhores_ciclos["team"], dodge=True)
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
df_brasileirao_ciclo_geral = (df_brasileirao_ciclo.sort_values(by="percentage", ascending=False)
                                                  .reset_index(drop=True)
                                                  .query("percentage >= 55")
                                                  .copy())
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
stats_gerais
# %%
