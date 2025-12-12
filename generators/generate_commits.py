# generators/generate_commits.py

import os
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe

from utils.plot_theme import apply_dark_tech_theme, apply_vertical_gradient
from utils.github_api import get_repos, get_commit_activity

OUTPUT_PATH = "output/github-stats.png"
USERNAME = "Domisnnet"

def generate_commits_graph():
    apply_dark_tech_theme()

    repos = get_repos(USERNAME)

    total_commits = 0

    for repo in repos:
        activity = get_commit_activity(repo["full_name"])
        if isinstance(activity, list):
            for week in activity:
                total_commits += week["total"]

    # Cria figura
    fig, ax = plt.subplots(figsize=(9, 3.8))

    # Aplica gradiente moderno
    apply_vertical_gradient(ax)

    # Barra neon
    bar = ax.bar(
        ["Commits no Ano"],
        [total_commits],
        width=0.45,
        color="#39C0FF",
        edgecolor="#39C0FF",
        linewidth=1.8,
        zorder=3
    )

    # Glow sutil
    for rect in bar:
        rect.set_path_effects([
            pe.withStroke(linewidth=8, foreground="#39C0FF50"),
            pe.Normal()
        ])

    # Valor acima da barra
    ax.text(
        0, total_commits + (total_commits * 0.05),
        f"{total_commits}",
        ha="center",
        fontsize=18,
        color="#6ED8FF",
        fontweight="bold",
        zorder=5,
        path_effects=[
            pe.withStroke(linewidth=4, foreground="#00000080"),
            pe.Normal()
        ]
    )

    ax.set_title("Commits no Último Ano", pad=14, fontsize=20)
    ax.grid(axis="y", color="#2A2A2A", linestyle="--", linewidth=0.5)

    plt.tight_layout()

    # Garante que a pasta output existe
    os.makedirs("output", exist_ok=True)

    plt.savefig(OUTPUT_PATH, dpi=300, bbox_inches="tight")
    plt.close()

if __name__ == "__main__":
    generate_commits_graph()