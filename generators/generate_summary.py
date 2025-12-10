import matplotlib.pyplot as plt
from utils.plot_theme import apply_dark_tech_theme
from utils.github_api import get_user, get_repos

USERNAME = "Domisnnet"

def generate_summary_graph():
    apply_dark_tech_theme()

    user = get_user(USERNAME)
    repos = get_repos(USERNAME)

    stars = sum(repo["stargazers_count"] for repo in repos)
    forks = sum(repo["forks_count"] for repo in repos)
    public_repos = user["public_repos"]
    
    fig, ax = plt.subplots(figsize=(8, 3))

    metrics = ["Stars", "Forks", "Repositórios"]
    values = [stars, forks, public_repos]

    ax.bar(metrics, values)
    ax.set_title("Resumo Geral do Perfil")

    plt.tight_layout()
    plt.savefig("output/summary.png", dpi=300)
    plt.close()

if __name__ == "__main__":
    generate_summary_graph()