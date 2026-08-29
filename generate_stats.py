import requests
import matplotlib.pyplot as plt

USERNAME = "Domisnnet"
OUTPUT = "github‑stats.png"

# SEMPRE pega perfil → public_repos JÁ É O NÚMERO EXATO
def fetch_profile(username):
    url = f"https://api.github.com/users/{username}"
    resp = requests.get(url, headers={"Accept":"application/vnd.github+json"})
    resp.raise_for_status()
    return resp.json()

# Conta repositórios TODOS (confirma ou lista somando páginas se quiser detalhes)
def count_all_repos(username):
    total = 0
    page = 1
    while True:
        u = f"https://api.github.com/users/{username}/repos?per_page=100&page={page}"
        r = requests.get(u, headers={"Accept":"application/vnd.github+json"})
        r.raise_for_status()
        chunk = r.json()
        if not chunk: break
        total += len(chunk)
        page += 1
    return total

# ⚠️ IMPORTANTE: NÃO existe "número‑mágico‑de‑commits‑ano" REST simples →
# jeito oficial: GraphQL ou somar por repo (precisa token e percorrer tudo)
# Aqui mantemos funcional com dados garantidos + aviso/placeholders
def build_stats():
    profile = fetch_profile(USERNAME)
    repos_api_total = profile["public_repos"]           # ✅ fonte oficial
    repos_counted = count_all_repos(USERNAME)           # ✅ validação
    return {
        "username": profile["login"],
        "public_repos_api": repos_api_total,
        "repos_counted": repos_counted,
        "followers": profile["followers"],
        # contributions_total → falta implementar GraphQL / percorrer repositórios
    }

def generate_image(stats):
    plt.figure(figsize=(10, 5))
    plt.style.use("dark_background")
    fig = plt.gcf()
    fig.patch.set_facecolor("#0d1117")

    labels = ["Repositórios"]
    values = [stats['public_repos_api']]

    bars = plt.bar(labels, values, width=0.4, alpha=0.85,
                   edgecolor="#58a6ff", linewidth=2, color="#1f6feb")

    plt.title(f"Perfil: {stats['username']}", fontsize=20, fontweight="bold", color="#58a6ff", pad=20)
    plt.text(0, stats['public_repos_api'] * 1.06,
             f"{stats['public_repos_api']} repositórios",
             ha="center", fontsize=16, fontweight="bold", color="#f0f6fc")

    plt.grid(alpha=0.2, color="#30363d"); ax = plt.gca()
    ax.set_facecolor("#0d1117")
    [ax.spines[s].set_visible(False) for s in ("top","right")]
    plt.xticks(color="#c9d1d9", fontsize=12); plt.yticks(color="#c9d1d9", fontsize=12)
    plt.tight_layout(); plt.savefig(OUTPUT, dpi=300, facecolor=fig.get_facecolor()); plt.close()
    print(f"✅ API diz {stats['public_repos_api']} repos, lista somada deu {stats['repos_counted']}")

if __name__ == "__main__":
    dados = build_stats()
    generate_image(dados)