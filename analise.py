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

def get_stats_geral(df, stat, bool):
    stats_gerais = df[df["played"] >= 114].copy()
    stats_gerais = stats_gerais.sort_values(by=stat, ascending=bool).head(13).reset_index(drop=False)
    return stats_gerais

def get_participacao(df):
    df_time = df[0]
    df_participacao = df[1]
    df_time_comp = {df_time:df_participacao}
    print(f"Time: {df_time} - Participações: {df_participacao}")
    return df_time_comp

# %%
df_brasileirao["percentage"] = round(df_brasileirao["points"] / (df_brasileirao["played"] * 3) * 100, 2)
df_brasileirao[["points_game", "goals_game", "goals_tak_game"]] = round(df_brasileirao[["points", "goals", "goals_taken"]].div(df_brasileirao["played"], axis=0), 2)


# %%
stats_gerais = (df_brasileirao.groupby("team").agg({"points": "sum", "played": "sum", 
                                                        "won": "sum", "draw": "sum", "loss": "sum",
                                                        "goals": "sum", "goals_taken": "sum", "goals_diff": "sum",
                                                        "points_game": "mean", "goals_game": "mean",
                                                        "goals_tak_game": "mean"})
                                     .query("played > (38 * 3)"))
stats_gerais["percentage"] = round(stats_gerais["points"] / (stats_gerais["played"] * 3) * 100, 2)
stats_gerais[["points_game", "goals_game", "goals_tak_game", "percentage"]] = round(stats_gerais[["points_game", "goals_game", "goals_tak_game", "percentage"]],2)
stats_gerais
# %%
maior_aproveitamento_temp = get_stats_temp(df_brasileirao, "percentage", False)
menor_aproveitamento_temp = get_stats_temp(df_brasileirao, "percentage", True)
maior_pontos_temp = get_stats_temp(df_brasileirao, "points_game", False)
menor_pontos_temp = get_stats_temp(df_brasileirao, "points_game", True)
maior_goals_temp = get_stats_temp(df_brasileirao, "goals_game", False)
menor_goals_temp = get_stats_temp(df_brasileirao, "goals_game", True)
menor_goals_tak_temp = get_stats_temp(df_brasileirao, "goals_tak_game", True)
maior_goals_tak_temp = get_stats_temp(df_brasileirao, "goals_tak_game", False)

maior_goals_tak_temp

#%%

times_mais_regulares = stats_gerais[stats_gerais["played"] >= (16 * 38)].copy()
times_mais_regulares
# %%
df_brasileirao_ciclo = df_brasileirao.copy()
df_brasileirao_ciclo

# %%
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
                              "goals_diff": "sum",
                              })
                              .reset_index()
                              )
# %% # %% cálculo de estatísticas adicionais
df_brasileirao_ciclo[["points_game", "goals_game", "goals_tak_game"]] = round(df_brasileirao_ciclo[["points", "goals", "goals_taken"]].div(df_brasileirao_ciclo["played"], axis=0), 2)
df_brasileirao_ciclo["percentage"] = round(df_brasileirao_ciclo["points"] / (df_brasileirao_ciclo["played"] * 3) * 100, 2)

ciclos_completos = df_brasileirao_ciclo[df_brasileirao_ciclo["ciclo"] != "2023-2026"].copy()
ciclos_completos = ciclos_completos[ciclos_completos["played"] >= 76]

"""
Escolher qual estatística para determinar os melhores e piores ciclos completos.
- "percentage": aproveitamento
- "points_game": pontos por jogo
- "goals_game": gols por jogo
- "goals_tak_game": gols sofridos por jogo
- True: Resultados negativos(invertido para o caso de gols sofridos)
- False: Resultados positivos(invertido para o caso de gols sofridos)

"""
maior_aproveit_ciclo = get_stats_ciclo(ciclos_completos, "percentage", False)
menor_aproveit_ciclo = get_stats_ciclo(ciclos_completos, "percentage", True)
maior_pontos_ciclo = get_stats_ciclo(ciclos_completos, "points_game", False)
menor_pontos_ciclo = get_stats_ciclo(ciclos_completos, "points_game", True)
maior_gols_ciclo = get_stats_ciclo(ciclos_completos, "goals_game", False)
menor_gols_ciclo = get_stats_ciclo(ciclos_completos, "goals_game", True)
menor_gols_tak_ciclo = get_stats_ciclo(ciclos_completos, "goals_tak_game", True)
maior_gols_tak_ciclo = get_stats_ciclo(ciclos_completos, "goals_tak_game", False)

# maiores_aproveitamentos
maior_aproveit_geral = get_stats_geral(stats_gerais, "percentage", False)
menor_aproveit_geral = get_stats_geral(stats_gerais, "percentage", True)
maior_pontos_geral = get_stats_geral(stats_gerais, "points", False)
menor_pontos_geral = get_stats_geral(stats_gerais, "points", True)
maior_gols_geral = get_stats_geral(stats_gerais, "goals", False)
menor_gols_geral = get_stats_geral(stats_gerais, "goals", True)
menor_gols_tak_geral = get_stats_geral(stats_gerais, "goals_tak_game", True)
maior_gols_tak_geral = get_stats_geral(stats_gerais, "goals_tak_game", False)

# partipações de cada time
df_participacoes = (df_brasileirao.groupby("team")
                    .agg({"season": "nunique"})
                    .reset_index()
                    .rename(columns={"season": "participacoes"}))
df_participacoes
for time in df_participacoes["team"]:
    if df_participacoes.loc[df_participacoes["team"] == time, "participacoes"].values[0] < 3:
        df_participacoes = df_participacoes.drop(df_participacoes[df_participacoes["team"] == time].index)
df_participacoes = df_participacoes.reset_index(drop=True)

participacoes_dict = dict(zip(df_participacoes["team"], df_participacoes["participacoes"]))

# %%
# times mais regulares
maior_aproveit_geral_regular = get_stats_geral(times_mais_regulares, "percentage", False)
maior_pontos_geral_regular = get_stats_geral(times_mais_regulares, "points", False)
maior_gols_geral_regular = get_stats_geral(times_mais_regulares, "goals", False)
menor_gols_tak_geral_regular = get_stats_geral(times_mais_regulares, "goals_tak_game", True)

# %% maior aproveitamento geral dos 13 times que mais participações
maior_aproveit_geral_regular["Posição"] = range(1, len(maior_aproveit_geral_regular) + 1)
cols = ["team"] + ["Posição"] + [col for col in maior_aproveit_geral_regular.columns if col != "team" and col != "Posição"]
maior_aproveit_geral_regular = maior_aproveit_geral_regular[cols]

# %% maior número de pontos dos 13 times que mais participações
maior_pontos_geral_regular["Posição"] = range(1, len(maior_pontos_geral_regular) + 1)
cols =["team"] + ["Posição"] + [col for col in maior_pontos_geral_regular.columns if col != "team" and col != "Posição"]
maior_pontos_geral_regular = maior_pontos_geral_regular[cols]


# %% maior numero de gols dos 13 times que mais participações
maior_gols_geral_regular["Posição"] = range(1, len(maior_gols_geral_regular) + 1)
cols =["team"] + ["Posição"] + [col for col in maior_gols_geral_regular.columns if col != "team" and col != "Posição"]
maior_gols_geral_regular = maior_gols_geral_regular[cols]


# %% menor numero de gols sofridos dos 13 times que mais participações
menor_gols_tak_geral_regular["Posição"] = range(1, len(menor_gols_tak_geral_regular) + 1)
cols = ["team"] + ["Posição"] + [col for col in menor_gols_tak_geral_regular.columns if col != "team" and col != "Posição"]
menor_gols_tak_geral_regular = menor_gols_tak_geral_regular[cols]


# %%
# media posições dos 13 times que mais participações
df_ranking = (maior_aproveit_geral_regular
              .merge(maior_pontos_geral_regular, on="team", suffixes=("_aproveitamento", "_pontos"))
              .merge(maior_gols_geral_regular, on="team", suffixes=("", "_gols"))
              .merge(menor_gols_tak_geral_regular, on="team", suffixes=("", "_gols_sofridos"))
              )
df_ranking
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
