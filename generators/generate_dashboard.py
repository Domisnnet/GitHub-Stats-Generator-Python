import os
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from utils.plot_theme import apply_dark_tech_theme
from utils.github_api import get_repos, get_commit_activity

USERNAME = "Domisnnet"
OUTPUT_PATH = "output/dashboard.png"

os.makedirs("output", exist_ok=True)


def rounded_panel(ax, x, y, width, height, radius=0.15, color="#10121a", alpha=0.9):
    """Cria um painel com bordas arredondadas, estilo card moderno."""
    box = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle=f"round,pad=0.02,rounding_size={radius}",
        linewidth=1.2,
        edgecolor="#303542",
        facecolor=color,
        alpha=alpha,
    )
    ax.add_patch(box)


def generate_dashboard():
    apply_dark_tech_theme()

    repos = get_repos(USERNAME)

    total_commits = 0
    total_repos = len(repos)

    for repo in repos:
        activity = get_commit_activity(repo["full_name"])
        if isinstance(activity, list):
            for week in activity:
                total_commits += week["total"]

    # Layout da figura
    fig = plt.figure(figsize=(12, 6), dpi=300)
    ax = fig.add_subplot(111)

    # Remove eixos
    ax.axis("off")

    # Painel de fundo com bordas arredondadas
    rounded_panel(ax, 0.02, 0.02, 0.96, 0.96, radius=0.08, color="#0c0e14", alpha=1)

    # Título central
    ax.text(
        0.5,
        0.92,
        f"GitHub Dashboard — {USERNAME}",
        ha="center",
        va="center",
        fontsize=26,
        fontweight="bold",
        color="#F0F3FF",
    )

    # Subtítulo
    ax.text(
        0.5,
        0.87,
        "Resumo geral de contribuições e repositórios",
        ha="center",
        va="center",
        fontsize=14,
        color="#aeb6d8",
    )

    # Painel 1 — Total de commits
    rounded_panel(ax, 0.08, 0.52, 0.40, 0.30, radius=0.07, color="#141722")
    ax.text(
        0.28,
        0.67,
        "Commits no Último Ano",
        ha="center",
        va="center",
        fontsize=16,
        fontweight="bold",
        color="#E6E9F5",
    )
    ax.text(
        0.28,
        0.58,
        f"{total_commits:,}".replace(",", "."),
        ha="center",
        va="center",
        fontsize=34,
        fontweight="bold",
        color="#4f9bff",
    )

    # Painel 2 — Total de repositórios
    rounded_panel(ax, 0.52, 0.52, 0.40, 0.30, radius=0.07, color="#141722")
    ax.text(
        0.72,
        0.67,
        "Repositórios Públicos",
        ha="center",
        va="center",
        fontsize=16,
        fontweight="bold",
        color="#E6E9F5",
    )
    ax.text(
        0.72,
        0.58,
        f"{total_repos}",
        ha="center",
        va="center",
        fontsize=34,
        fontweight="bold",
        color="#4fffba",
    )

    # Painel inferior com destaque
    rounded_panel(ax, 0.08, 0.10, 0.84, 0.32, radius=0.07, color="#1a1d29")

    ax.text(
        0.50,
        0.32,
        "Resumo Executivo",
        ha="center",
        va="center",
        fontsize=20,
        fontweight="bold",
        color="#F0F3FF",
    )

    ax.text(
        0.50,
        0.19,
        f"- Total de commits no último ano: {total_commits:,}".replace(",", ".")
        + f"\n- Total de repositórios públicos: {total_repos}"
        + "\n- Dados atualizados automaticamente via GitHub Actions",
        ha="center",
        va="center",
        fontsize=12,
        color="#c1c7dd",
        linespacing=1.6,
    )

    # Salvar
    plt.savefig(OUTPUT_PATH, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Dashboard gerado com sucesso em: {OUTPUT_PATH}")


if __name__ == "__main__":
    generate_dashboard()