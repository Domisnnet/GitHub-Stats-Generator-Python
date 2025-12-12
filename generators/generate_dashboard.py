import matplotlib.pyplot as plt
import matplotlib.patches as FancyBox
import numpy as np
from github import Github
import os

# -------------------------------
# CONFIGURAÇÕES GERAIS PREMIUM
# -------------------------------
plt.rcParams['figure.figsize'] = (16, 10)
plt.rcParams['figure.dpi'] = 120
plt.rcParams["axes.facecolor"] = "#050A1A"
plt.rcParams["figure.facecolor"] = "#050A1A"
plt.rcParams["savefig.facecolor"] = "#050A1A"

PRIMARY = "#2BD1FF"     # Azul neon elegante
SECONDARY = "#00A3FF"   # Azul mais profundo
TEXT = "#EEEEEE"        # Texto claro premium


# -------------------------------
# OBTÉM DADOS DO GITHUB
# -------------------------------
token = os.getenv("GITHUB_TOKEN")
username = os.getenv("GITHUB_USERNAME")

g = Github(token)
user = g.get_user()

repos = list(user.get_repos())
total_repos = len(repos)
active_repos = sum(1 for r in repos if not r.archived)

total_commits = 0
for repo in repos:
    try:
        commits = repo.get_commits(author=user)
        total_commits += commits.totalCount
    except:
        pass

# fake para teste visual (remova depois se não quiser)
# total_commits = 255

languages = {}
for repo in repos:
    langs = repo.get_languages()
    for lang, count in langs.items():
        languages[lang] = languages.get(lang, 0) + count

sorted_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)
labels = [l[0] for l in sorted_langs]
sizes = [l[1] for l in sorted_langs]


# -------------------------------
# FUNÇÃO PARA CRIAR CARD PREMIUM
# -------------------------------
def add_card(ax, title):
    rect = FancyBox.FancyBboxPatch(
        (0, 0),
        1,
        1,
        boxstyle="round,pad=0.03,rounding_size=0.14",
        linewidth=2,
        edgecolor=PRIMARY,
        facecolor="#0B152E",
        transform=ax.transAxes,
        zorder=-1
    )
    ax.add_patch(rect)

    ax.text(
        0.5, 0.92, title,
        color=TEXT,
        fontsize=18,
        ha="center",
        va="center",
        weight="bold",
        family="DejaVu Sans"
    )

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)


# --------------------------------------
# CONSTRUÇÃO DO DASHBOARD 2x2 PREMIUM
# --------------------------------------
fig, axs = plt.subplots(2, 2)

# CARD 1 - OVERVIEW
ax1 = axs[0][0]
add_card(ax1, "Visão Geral do GitHub")

ax1.text(
    0.5, 0.55,
    f"Repositórios Totais: {total_repos}\n"
    f"Repositórios Ativos: {active_repos}\n"
    f"Commits no Último Ano: {total_commits}",
    color=TEXT,
    ha="center",
    va="center",
    fontsize=14
)

# CARD 2 - DONUT COMMITS
ax2 = axs[0][1]
add_card(ax2, "Commits (Donut)")

# Donut
values = [total_commits]
ax2.pie(
    values,
    radius=0.8,
    wedgeprops=dict(width=0.35, edgecolor='none'),
    colors=[PRIMARY]
)

ax2.text(
    0.5, 0.5,
    f"{total_commits}",
    color=TEXT,
    fontsize=24,
    ha="center",
    va="center",
    weight="bold"
)

# CARD 3 & 4 — LINGUAGENS (ocupando ambas as colunas da linha de baixo)
# Unifica as duas células inferiores para criar um card wide premium
ax3 = fig.add_subplot(2, 1, 2)
add_card(ax3, "Linguagens Mais Usadas")

# Pie grande
ax3.pie(
    sizes,
    labels=labels,
    autopct='%1.1f%%',
    pctdistance=0.75,
    labeldistance=1.05,
    textprops={'color': TEXT, 'fontsize': 10},
    wedgeprops=dict(edgecolor='none'),
)

# Centraliza totalmente
ax3.set_position([0.05, 0.03, 0.9, 0.42])

# -------------------------------
# SALVAR SAÍDA
# -------------------------------
output_path = "output/github-stats.png"
plt.savefig(output_path, dpi=140, bbox_inches="tight")
plt.close()

print("Dashboard premium gerado com sucesso:", output_path)