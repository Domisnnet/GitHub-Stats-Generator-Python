import os
import json
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
from utils.plot_theme import apply_dark_tech_theme
from utils.github_api import get_user, get_repos, get_commit_activity

USERNAME = "Domisnnet"
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_premium_graph():
  apply_dark_tech_theme()
  profile = get_user(USERNAME)
  repos = get_repos(USERNAME)
  total_stars = sum(repo.get("stargazers_count", 0) for repo in repos)
  repo_count = len(repos)
  repo_count_api = profile.get("public_repos", repo_count)
  weekly_commits = [0] * 52
  print(f"🔍 Coletando estatísticas de {repo_count} repositórios…")
  for idx_repo, repo in enumerate(repos, start=1):
    repo_name = repo["full_name"]
    print(f"   [{idx_repo}/{repo_count}] {repo_name}…")
    commit_data = get_commit_activity(repo_name)
    if isinstance(commit_data, list) and commit_data:
      for idx_week, week in enumerate(commit_data):
        if idx_week < 52:
          weekly_commits[idx_week] += week.get("total", 0)
  total_commits_year = int(sum(weekly_commits))
  fig, ax = plt.subplots(figsize=(12, 5))  # === GRÁFICO ===
  x = np.arange(52)
  y = np.array(weekly_commits)
  ax.plot(x, y, linewidth=2.5, color="#00A8FF", alpha=0.9, zorder=3)
  for glow_size in [6, 12, 18]:
    ax.plot(x, y, linewidth=glow_size, color="#00A8FF", alpha=0.06, zorder=2)
  ax.fill_between(x, y, color="#00A8FF", alpha=0.18, zorder=1)
  ax.set_title(f"Commits no Último Ano — {USERNAME}", fontsize=18, pad=20, weight="bold", color="#FFFFFF")
  ax.spines["top"].set_visible(False)
  ax.spines["right"].set_visible(False)
  ax.grid(color="#666666", alpha=0.2)
  fig.text(0.02, 0.96, f"Commits no Ano: {total_commits_year}", fontsize=12, color="#00A8FF", weight="bold")
  fig.text(0.22, 0.96, f"Repositórios: {repo_count} (perfil: {repo_count_api})", fontsize=12, color="#00FFBF", weight="bold")
  fig.text(0.44, 0.96, f"Stars: {total_stars}", fontsize=12, color="#FFD86B", weight="bold")
  plt.tight_layout()
  caminho = f"{OUTPUT_DIR}/github-stats.png"
  plt.savefig(caminho, dpi=300)
  plt.close()
  print(f"\n✅ Pronto → Salvo: {caminho}")
  print(f"📊 Resumo → {repo_count} repos / {total_commits_year} commits / {total_stars} estrelas")
  save_stats_to_json(profile, repos, total_commits_year, total_stars)  # Gera o JSON para o Dashboard

def save_stats_to_json(profile, repos, total_commits, total_stars):
  languages = {}
  for repo in repos:
    if repo.get("language"):
      lang = repo["language"]
      languages[lang] = languages.get(lang, 0) + 1  
  sorted_languages = dict(sorted(languages.items(), key=lambda item: item[1], reverse=True))
  stats_data = {
    "username": USERNAME,
    "total_repos": len(repos),
    "total_commits_year": total_commits,
    "total_stars": total_stars,
    "public_repos_api": profile.get("public_repos", 0),
    "top_languages": sorted_languages,
    "last_updated": datetime.now().isoformat()
  }

  json_path = f"{OUTPUT_DIR}/stats.json"
  with open(json_path, "w", encoding="utf-8") as f:
    json.dump(stats_data, f, indent=2, ensure_ascii=False)    
  print(f"💾 Dados salvos em: {json_path}")

if __name__ == "__main__":
  print("🚀 Iniciando Gerador de Stats do DomisDev...\n")
  generate_premium_graph()
  print("\n✨ Processo concluído com sucesso!")