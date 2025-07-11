# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import kagglehub as kg
# %%
path = kg.dataset_download("lucasyukioimafuko/brasileirao-serie-a-2006-2022")
# %% dataframe do brasileirão de 2003 a 2024
df_brasileirao = pd.read_csv(path + "/brasileirao.csv")
df_brasileirao
# %% # dataframe dos times
df_times = pd.read_csv(path + "/teams.csv")
df_times

# %%
maiores_pontuadores = (df_brasileirao.groupby("team").agg({"points": "sum", "played": "sum"})
                                     .sort_values(by="points", ascending=False)
                                     .query("played > (38 * 3)"))

# %%
maiores_aproveitamentos = (df_brasileirao.groupby("team")
                                        .agg({"points": "sum", "played": "sum"})
                                        .assign(percentage=lambda x: x["points"] / (x["played"] * 3) * 100)
                                        .sort_values(by="percentage", ascending=False)
                                        .query("played > (38 * 3)"))
maiores_aproveitamentos["percentage"] = maiores_aproveitamentos["percentage"].round(2)
maiores_aproveitamentos
# %% visualização dos maiores pontuadores
plt.figure(figsize=(20, 12))
sns.barplot(x=maiores_pontuadores.index, y=maiores_pontuadores["points"], width=0.6)
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

# Criar coluna 'ciclo' agrupando as temporadas de 4 em 4 anos
def get_ciclo(season):
    start = 2003 + 4 * ((season - 2003) // 4)
    end = start + 3
    return f"{start}-{end}"

df_brasileirao_ciclo["ciclo"] = df_brasileirao_ciclo["season"].apply(get_ciclo)

# Exemplo de visualização dos ciclos
print(df_brasileirao_ciclo[["season", "ciclo"]].drop_duplicates().sort_values("season"))
# %%
df_brasileirao_ciclo = df_brasileirao_ciclo.drop(columns = ["season", "place"])
# %%
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

# %%
df_brasileirao_ciclo["percentage"] = df_brasileirao_ciclo["percentage"].round(2)
df_brasileirao_ciclo
# %%
melhores_ciclos = df_brasileirao_ciclo.sort_values(by="percentage", ascending=False).head(10).reset_index(drop=True)
melhores_ciclos
# %%
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
maiores_pontuadores
# %%
