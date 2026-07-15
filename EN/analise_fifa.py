# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os

sns.set_theme(style="darkgrid")
plt.rcParams["figure.dpi"] = 120
FIG_DIR = "figs"
os.makedirs(FIG_DIR, exist_ok=True)

# ETAPA 1: ENTENDIMENTO DOS DADOS
df = pd.read_csv("FIFA_World_Cup_1558_23.csv")
print("Dimensoes:", df.shape)
print(df.dtypes)
print(df.head())

# ETAPA 2: AUDITORIA DOS DADOS
print("\n--- Valores ausentes ---")
print(df.isnull().sum())

print("\n--- Duplicados (linha inteira) ---")
print(df.duplicated().sum())

print("\n--- Duplicados por MatchID ---")
dup_match = df[df.duplicated(subset=["MatchID"], keep=False)].sort_values("MatchID")
print(dup_match[["MatchID", "Year", "Home.Team.Name", "Away.Team.Name", "Datetime"]])

print("\n--- Inconsistencia: Half-time goals > Full-time goals ---")
inc_home = df[df["Half.time.Home.Goals"] > df["Home.Team.Goals"]]
inc_away = df[df["Half.time.Away.Goals"] > df["Away.Team.Goals"]]
print("Home:", len(inc_home), "Away:", len(inc_away))

print("\n--- Attendance == 0 ou irrealista ---")
print(df[df["Attendance"] < 2000][["Year", "City", "Attendance"]])

print("\n--- Placar irrealista (>8 gols em um time) ---")
print(df[(df["Home.Team.Goals"] > 8) | (df["Away.Team.Goals"] > 8)]
      [["Year", "Home.Team.Name", "Home.Team.Goals", "Away.Team.Goals", "Away.Team.Name"]])

q1, q3 = df["Attendance"].quantile([0.25, 0.75])
iqr = q3 - q1
lim_sup = q3 + 1.5 * iqr
lim_inf = q1 - 1.5 * iqr
outliers_att = df[(df["Attendance"] > lim_sup) | (df["Attendance"] < lim_inf)]
print(f"\nOutliers de publico (IQR): {len(outliers_att)} jogos | limite superior={lim_sup:.0f}")


# ETAPA 3: ANALISE UNIVARIADA
num_vars = ["Home.Team.Goals", "Away.Team.Goals", "Attendance",
            "Half.time.Home.Goals", "Half.time.Away.Goals"]

resumo = pd.DataFrame({
    "media": df[num_vars].mean(),
    "mediana": df[num_vars].median(),
    "moda": df[num_vars].mode().iloc[0],
    "variancia": df[num_vars].var(),
    "desvio_padrao": df[num_vars].std(),
    "cv_%": (df[num_vars].std() / df[num_vars].mean()) * 100,
    "assimetria": df[num_vars].skew(),
    "q1": df[num_vars].quantile(0.25),
    "q3": df[num_vars].quantile(0.75),
})
print(resumo)

fig, axes = plt.subplots(2, 3, figsize=(16, 9))
for ax, col in zip(axes.flat, num_vars):
    sns.histplot(df[col], kde=True, ax=ax, color="#1f6f43")
    ax.set_title(col)
axes.flat[-1].axis("off")
plt.tight_layout()
plt.savefig(f"{FIG_DIR}/histogramas.png")
plt.close()

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
sns.boxplot(y=df["Home.Team.Goals"], ax=axes[0], color="#2a9d8f")
sns.boxplot(y=df["Away.Team.Goals"], ax=axes[1], color="#e76f51")
sns.boxplot(y=df["Attendance"], ax=axes[2], color="#264653")
axes[0].set_title("Gols Mandante")
axes[1].set_title("Gols Visitante")
axes[2].set_title("Publico")
plt.tight_layout()
plt.savefig(f"{FIG_DIR}/boxplots.png")
plt.close()


# ETAPA 4: ANALISE BIVARIADA
corr = df[num_vars].corr()
print(corr)

plt.figure(figsize=(7, 6))
sns.heatmap(corr, annot=True, cmap="RdBu_r", center=0, fmt=".2f")
plt.title("Matriz de Correlacao")
plt.tight_layout()
plt.savefig(f"{FIG_DIR}/heatmap.png")
plt.close()

plt.figure(figsize=(7, 6))
sns.scatterplot(data=df, x="Home.Team.Goals", y="Away.Team.Goals", alpha=0.4)
plt.title("Gols Mandante vs Gols Visitante")
plt.tight_layout()
plt.savefig(f"{FIG_DIR}/scatter_gols.png")
plt.close()

plt.figure(figsize=(7, 6))
sns.scatterplot(data=df, x="Year", y="Attendance", alpha=0.5)
plt.title("Publico ao longo dos anos")
plt.tight_layout()
plt.savefig(f"{FIG_DIR}/scatter_publico_ano.png")
plt.close()


# ETAPA 5: MULTICOLINEARIDADE
print("\nPares com |r| > 0.5 (excluindo diagonal):")
c = corr.abs()
pairs = c.where(np.triu(np.ones(c.shape), k=1).astype(bool)).stack()
print(pairs[pairs > 0.5].sort_values(ascending=False))


# ETAPA 6: VISUALIZACAO MULTIVARIADA
df["Total.Goals"] = df["Home.Team.Goals"] + df["Away.Team.Goals"]
df["Is.Final"] = df["Stage"].isin(["Final", "Match for third place", "Third place",
                                    "Play-off for third place"])

plt.figure(figsize=(9, 6))
sns.scatterplot(data=df, x="Year", y="Total.Goals", hue="Is.Final",
                 size="Attendance", sizes=(20, 200), alpha=0.6, palette="Set1")
plt.title("Gols totais por jogo x Ano, tamanho=Publico, cor=Fase Final")
plt.tight_layout()
plt.savefig(f"{FIG_DIR}/multivar1.png")
plt.close()

top_stages = df["Stage"].value_counts().nlargest(6).index
plt.figure(figsize=(9, 6))
sns.boxplot(data=df[df["Stage"].isin(top_stages)], x="Stage", y="Attendance")
plt.xticks(rotation=30)
plt.title("Publico por Fase (top 6 fases mais frequentes)")
plt.tight_layout()
plt.savefig(f"{FIG_DIR}/multivar2.png")
plt.close()

pp = sns.pairplot(df[num_vars[:2] + ["Attendance"]].assign(
    Epoca=pd.cut(df["Year"], bins=[1929, 1966, 1994, 2014],
                 labels=["1930-1966", "1970-1994", "1998-2014"])),
    hue="Epoca", diag_kind="kde", palette="viridis")
pp.savefig(f"{FIG_DIR}/pairplot.png")
plt.close()

print("\nScript concluido. Figuras salvas em", FIG_DIR)
