import os
import sys
import traceback
from datetime import datetime

import matplotlib.pyplot as plt

# LOGS DE DIAGNÓSTICO
print("=== DEBUG: Iniciando generate_commits.py ===")
print("Working directory:", os.getcwd())
print("Python path:", sys.path)

# Garante diretório correto
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Output directory absolute path:", os.path.abspath(OUTPUT_DIR))
print("Conteúdo inicial da pasta output:", os.listdir(OUTPUT_DIR))

# IMPORTS DO PROJETO
try:
    from utils.plot_theme import apply_dark_tech_theme
    from utils.github_api import get_repos, get_commit_activity
    print("Imports internos OK.")
except Exception as e:
    print("ERRO IMPORTANDO utils/:")
    traceback.print_exc()
    # Cria arquivo placeholder indicando erro
    with open(os.path.join(OUTPUT_DIR, "error_imports.txt"), "w") as f:
        f.write(str(e))
    sys.exit(1)

USERNAME = "Domisnnet"


def generate_commits_graph():
    print("\n=== DEBUG: Iniciando coleta de repositórios ===")

    try:
        repos = get_repos(USERNAME)
        if not repos:
            raise ValueError("Nenhum repositório foi retornado pela API.")
        print(f"Repositórios encontrados: {len(repos)}")
    except Exception as e:
        print("ERRO ao obter repositórios:")
        traceback.print_exc()
        with open(os.path.join(OUTPUT_DIR, "error_repos.txt"), "w") as f:
            f.write(str(e))
        sys.exit(1)

    total_commits = 0

    print("\n=== DEBUG: Iniciando coleta de commits por repositório ===")
    for repo in repos:
        try:
            activity = get_commit_activity(repo["full_name"])

            if isinstance(activity, list):
                soma = sum(week.get("total", 0) for week in activity)
                print(f"{repo['full_name']}: {soma} commits")
                total_commits += soma
            else:
                print(f"{repo['full_name']}: API retornou formato inesperado: {activity}")

        except Exception as e:
            print(f"ERRO lendo commits do repo {repo['full_name']}:")
            traceback.print_exc()

    print("\nTotal de commits no ano:", total_commits)

    # APLICA TEMA
    try:
        apply_dark_tech_theme()
    except Exception:
        print("ERRO aplicando tema do gráfico.")
        traceback.print_exc()

    print("\n=== DEBUG: Gerando gráfico ===")
    try:
        fig, ax = plt.subplots(figsize=(8, 3))
        ax.bar(["Commits no ano"], [total_commits], width=0.4)
        ax.set_title("Commits no Último Ano", pad=12)

        plt.tight_layout()

        output_path = os.path.join(OUTPUT_DIR, "github-stats.png")
        plt.savefig(output_path, dpi=300)
        plt.close()

        print("Gráfico salvo com sucesso em:", os.path.abspath(output_path))
        print("Conteúdo final da pasta output:", os.listdir(OUTPUT_DIR))

    except Exception as e:
        print("ERRO ao gerar ou salvar o gráfico:")
        traceback.print_exc()

        with open(os.path.join(OUTPUT_DIR, "error_graph.txt"), "w") as f:
            f.write(str(e))

        sys.exit(1)


if __name__ == "__main__":
    generate_commits_graph()
    print("\n=== generate_commits.py finalizado com sucesso ===")