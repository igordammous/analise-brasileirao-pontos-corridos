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

def get_ciclo(season):
    start = 2003 + 4 * ((season - 2003) // 4)
    end = start + 3
    return f"{start}-{end}"

# Cria dataframe com estatísticas do brasileirão por temporada 
# E cria a porcentagem de aproveitamento em cada temporada
df_brasileirao["percentage"] = round(df_brasileirao["points"] / (df_brasileirao["played"] * 3) * 100, 2)
df_brasileirao[["points_game", "goals_game", "goals_tak_game"]] = round(df_brasileirao[["points", "goals", "goals_taken"]].div(df_brasileirao["played"], axis=0), 2)

# Cria dataframe com estatísticas gerais dos times
stats_gerais = (df_brasileirao.groupby("team").agg({"points": "sum", "played": "sum", 
                                                        "won": "sum", "draw": "sum", "loss": "sum",
                                                        "goals": "sum", "goals_taken": "sum", "goals_diff": "sum",
                                                        "points_game": "mean", "goals_game": "mean",
                                                        "goals_tak_game": "mean"})
                                     .query("played > (38 * 3)"))
stats_gerais["percentage"] = round(stats_gerais["points"] / (stats_gerais["played"] * 3) * 100, 2)
stats_gerais[["points_game", "goals_game", "goals_tak_game", "percentage"]] = round(stats_gerais[["points_game", "goals_game", "goals_tak_game", "percentage"]],2)
stats_gerais

# Filtra dataframes de acordo com a estatística desejada
# Escolher qual estatística para determinar os melhores e piores times
"""
Escolher qual estatística para determinar os melhores e piores ciclos completos.
- "percentage": aproveitamento
- "points_game": pontos por jogo
- "goals_game": gols por jogo
- "goals_tak_game": gols sofridos por jogo
- True: Resultados negativos(invertido para o caso de gols sofridos)
- False: Resultados positivos(invertido para o caso de gols sofridos)

"""
maior_aproveitamento_temp = get_stats_temp(df_brasileirao, "percentage", False)
menor_aproveitamento_temp = get_stats_temp(df_brasileirao, "percentage", True)
maior_pontos_temp = get_stats_temp(df_brasileirao, "points_game", False)
menor_pontos_temp = get_stats_temp(df_brasileirao, "points_game", True)
maior_goals_temp = get_stats_temp(df_brasileirao, "goals_game", False)
menor_goals_temp = get_stats_temp(df_brasileirao, "goals_game", True)
menor_goals_tak_temp = get_stats_temp(df_brasileirao, "goals_tak_game", True)
maior_goals_tak_temp = get_stats_temp(df_brasileirao, "goals_tak_game", False)

# Filtra times mais regulares, que jogaram pelo menos 16 temporadas
# (38 jogos por temporada, totalizando mais de 608 jogos)
times_mais_regulares = stats_gerais[stats_gerais["played"] >= (16 * 38)].copy()

times_13 = times_mais_regulares.index
df_brasileirao_regulares = df_brasileirao[df_brasileirao["team"].isin(times_13)].copy()

# Cria uma dataframe com a média de posições dos times mais regulares 
df_brasileirao_regulares = (df_brasileirao_regulares.groupby("team").agg({"place": "mean"})
                            .reset_index()
                            )

df_brasileirao_regulares["place"] = round(df_brasileirao_regulares[["place"]], 2)
df_brasileirao_regulares.rename(columns={"place": "Média de Posições Geral"}, inplace=True)

#%% 
df_brasileirao_ciclo = df_brasileirao.copy()

# Cria coluna 'ciclo' agrupando as temporadas de 4 em 4 anos
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
# %% cálculo de estatísticas adicionais
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
# Times mais regulares
maior_aproveit_geral_regular = get_stats_geral(times_mais_regulares, "percentage", False)
maior_pontos_geral_regular = get_stats_geral(times_mais_regulares, "points", False)
maior_gols_geral_regular = get_stats_geral(times_mais_regulares, "goals", False)
menor_gols_tak_geral_regular = get_stats_geral(times_mais_regulares, "goals_tak_game", True)

# Maior aproveitamento geral dos 13 times que mais participações
maior_aproveit_geral_regular["Posição"] = range(1, len(maior_aproveit_geral_regular) + 1)
cols = ["team"] + ["Posição"] + [col for col in maior_aproveit_geral_regular.columns if col != "team" and col != "Posição"]
maior_aproveit_geral_regular = maior_aproveit_geral_regular[cols]

# Maior número de pontos dos 13 times que mais participações
maior_pontos_geral_regular["Posição"] = range(1, len(maior_pontos_geral_regular) + 1)
cols =["team"] + ["Posição"] + [col for col in maior_pontos_geral_regular.columns if col != "team" and col != "Posição"]
maior_pontos_geral_regular = maior_pontos_geral_regular[cols]


# Maior numero de gols dos 13 times que mais participações
maior_gols_geral_regular["Posição"] = range(1, len(maior_gols_geral_regular) + 1)
cols =["team"] + ["Posição"] + [col for col in maior_gols_geral_regular.columns if col != "team" and col != "Posição"]
maior_gols_geral_regular = maior_gols_geral_regular[cols]


# Menor numero de gols sofridos dos 13 times que mais participações
menor_gols_tak_geral_regular["Posição"] = range(1, len(menor_gols_tak_geral_regular) + 1)
cols = ["team"] + ["Posição"] + [col for col in menor_gols_tak_geral_regular.columns if col != "team" and col != "Posição"]
menor_gols_tak_geral_regular = menor_gols_tak_geral_regular[cols]


# %%
# media posições dos 13 times que mais participações
df_ranking_stats = (maior_aproveit_geral_regular
              .merge(maior_pontos_geral_regular, on="team", suffixes=("_aproveitamento", "_pontos"))
              .merge(maior_gols_geral_regular, on="team", suffixes=("", "_gols"))
              .merge(menor_gols_tak_geral_regular, on="team", suffixes=("", "_gols_sofridos"))
              .merge(df_brasileirao_regulares, on="team", how="left")
              )

# dropando colunas duplicadas
drop_columns_pontos = ['points_pontos', 'played_pontos', 'won_pontos',
       'draw_pontos', 'loss_pontos', 'goals_pontos', 'goals_taken_pontos',
       'goals_diff_pontos', 'points_game_pontos', 'goals_game_pontos',
       'goals_tak_game_pontos', 'percentage_pontos']
drop_columns_gols = ['points','played', 'won', 'draw', 'loss', 'goals', 'goals_taken', 'goals_diff',
       'points_game', 'goals_game', 'goals_tak_game', 'percentage']
drop_columns_gols_sofridos = ['points_gols_sofridos', 'played_gols_sofridos',
       'won_gols_sofridos', 'draw_gols_sofridos', 'loss_gols_sofridos',
       'goals_gols_sofridos', 'goals_taken_gols_sofridos',
       'goals_diff_gols_sofridos', 'points_game_gols_sofridos',
       'goals_game_gols_sofridos', 'goals_tak_game_gols_sofridos',
       'percentage_gols_sofridos']
drop_columns = (drop_columns_pontos + drop_columns_gols + drop_columns_gols_sofridos)
df_ranking_stats = df_ranking_stats.drop(drop_columns, axis=1)

# renomeando colunas para português
df_ranking_stats.rename(columns={
    "team": "Time",
    "Posição_aproveitamento": "Posição em Aproveitamento",
    "points_aproveitamento": "Total de Pontos",
    "played_aproveitamento": "Total de Jogos",
    "won_aproveitamento": "Total de Vitórias",
    "draw_aproveitamento": "Total de Empates",
    "loss_aproveitamento": "Total de Derrotas",
    "goals_aproveitamento": "Total de Gols Feitos",
    "goals_taken_aproveitamento": "Total de Gols Sofridos",
    "goals_diff_aproveitamento": "Saldo de Gols",
    "Posição_pontos": "Posição em Pontos",
    "percentage_aproveitamento": "Aproveitamento (%)",
    "points_game_aproveitamento": "Média de Pontos por Jogo",
    "goals_game_aproveitamento": "Média de Gols por Jogo",
    "goals_tak_game_aproveitamento": "Média de Gols Sofridos por Jogo",
    "Posição": "Posição em Gols Feitos",
    "Posição_gols_sofridos": "Posição em Gols Sofridos",
}, inplace=True)

# reordenando colunas
columns = ["Total de Pontos",
           "Total de Jogos",
           "Total de Vitórias",
           "Total de Empates",
           "Total de Derrotas",
           "Total de Gols Feitos",
           "Total de Gols Sofridos",
           "Saldo de Gols",           
           "Aproveitamento (%)",
           "Média de Pontos por Jogo",
           "Média de Gols por Jogo",
           "Média de Gols Sofridos por Jogo",
           "Posição em Aproveitamento",
           "Posição em Pontos",
           "Posição em Gols Feitos",
           "Posição em Gols Sofridos",
           "Média de Posições Geral"]
df_ranking_stats = df_ranking_stats[["Time"] + columns]
df_ranking_stats

# %% media de posições dos 13 times que mais participações
media_posicoes = (df_ranking_stats[["Time"] + ["Posição em Aproveitamento", "Posição em Pontos",
                              "Posição em Gols Feitos", "Posição em Gols Sofridos"]]
                  .copy()
                  .set_index("Time")
                  .mean(axis=1)
                  .reset_index()
                  .rename(columns={0: "Média de Posições"}))
# merge com df_ranking_stats
df_ranking_stats = df_ranking_stats.merge(media_posicoes, on="Time", how="left")
df_ranking_stats = df_ranking_stats.sort_values(by="Média de Posições", ascending=True).reset_index(drop=True)
df_ranking = df_ranking_stats.copy()

# dropando colunas que não serão utilizadas
drop_columns = ["Total de Empates", "Total de Derrotas", "Saldo de Gols",
                "Média de Pontos por Jogo", "Média de Gols por Jogo",
                "Média de Gols Sofridos por Jogo"]
df_ranking = df_ranking.drop(drop_columns, axis=1)
df_ranking
# %%
md_df_ranking = df_ranking.to_markdown()
print(md_df_ranking)

df_brasileirao_ciclo_geral = (df_brasileirao_ciclo.sort_values(by="percentage", ascending=False)
                                                  .reset_index(drop=True)
                                                  .query("percentage >= 55")
                                                  .copy())

# %%
times_top_5 = df_ranking["Time"].head(5)

# %%
df_brasileirao_top_5 = df_brasileirao[df_brasileirao["team"].isin(times_top_5)].copy()
# %%
decada_2000 = df_brasileirao_top_5[df_brasileirao_top_5["season"].between(2003, 2009)]
decada_2010 = df_brasileirao_top_5[df_brasileirao_top_5["season"].between(2010, 2019)]
decada_2020 = df_brasileirao_top_5[df_brasileirao_top_5["season"].between(2020, 2024)]


# %%
decada_2000
# %%
decada_2010
# %%
