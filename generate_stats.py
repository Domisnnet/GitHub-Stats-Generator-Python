import requests
import matplotlib.pyplot as plt
from datetime import datetime
import os

USERNAME = "Domisnnet"
OUTPUT = "github-stats.png"


def fetch_contributions(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception("Erro ao buscar dados do GitHub")

    data = response.json()

    # Alguns endpoints mostram "contributions" apenas em APIs específicas,
    # mas você mencionou que este aparece para você (bom sinal).
    contributions = data.get("contributions", 0)

    return contributions


def generate_image(total_commits):
    plt.figure(figsize=(10, 5))
    plt.style.use("dark_background")

    # Fundo
    fig = plt.gcf()
    fig.patch.set_facecolor("#0d1117")  # GitHub dark theme

    # Barra única
    plt.bar(
        ["Commits no Último Ano"],
        [total_commits],
        width=0.4,
        alpha=0.85,
        edgecolor="#58a6ff",
        linewidth=2,
        color="#1f6feb",
    )

    # Título estilizado
    plt.title(
        f"Atividade de {USERNAME} no GitHub",
        fontsize=20,
        fontweight="bold",
        color="#58a6ff",
        pad=20,
    )

    # Valor do commit
    plt.text(
        0,
        total_commits + (total_commits * 0.05),
        f"{total_commits} commits",
        ha="center",
        fontsize=16,
        fontweight="bold",
        color="#f0f6fc",
    )

    # Grid
    plt.grid(alpha=0.2, color="#30363d")

    # Eixos
    ax = plt.gca()
    ax.set_facecolor("#0d1117")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Cores dos ticks
    plt.xticks(color="#c9d1d9", fontsize=12)
    plt.yticks(color="#c9d1d9", fontsize=12)

    plt.tight_layout()
    plt.savefig(OUTPUT, dpi=300, facecolor=fig.get_facecolor())
    plt.close()


def main():
    print("Gerando GitHub Stats…")
    commits = fetch_contributions(USERNAME)
    generate_image(commits)
    print("Imagem gerada:", OUTPUT)


if __name__ == "__main__":
    main()
