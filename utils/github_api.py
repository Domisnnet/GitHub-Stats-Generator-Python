from dotenv import load_dotenv
load_dotenv()

import requests
import time
import os
from datetime import datetime

PERSONAL_GITHUB_TOKEN = os.getenv("PERSONAL_GITHUB_TOKEN", "")

HEADERS = {
  "Accept": "application/vnd.github.v3+json",
  "User-Agent": "DomisDev-GitHub-Stats/1.0"
}

if PERSONAL_GITHUB_TOKEN:
  HEADERS["Authorization"] = f"token {PERSONAL_GITHUB_TOKEN}"
  print("✅ Autenticação com token ativada!")
else:
  print("⚠️ AVISO: Sem token! Limite de 60 req/hora.")

def _make_request(url, params=None):
  max_retries = 3
  for attempt in range(max_retries):
    try:
      resp = requests.get(url, headers=HEADERS, params=params)
      remaining = resp.headers.get('X-RateLimit-Remaining', 'unknown')
      reset_time = resp.headers.get('X-RateLimit-Reset', 'unknown')
      print(f"📡 Requisição: {url[:60]}... (Restante: {remaining})")
      
      if resp.status_code == 403 and remaining == '0':
        print(f"⚠️ Rate limit atingido! Reset em: {datetime.fromtimestamp(int(reset_time))}")
        time.sleep(60)
        continue
        
      resp.raise_for_status()
      return resp
    except requests.exceptions.RequestException as e:
      print(f"❌ Erro na requisição (tentativa {attempt + 1}/{max_retries}): {e}")
      if attempt < max_retries - 1:
        time.sleep(2 ** attempt)
      else:
        raise
  return None

def get_user(username):
  print(f"Buscando perfil de {username}...")
  resp = _make_request(f"https://api.github.com/users/{username}")
  return resp.json() if resp else {}

def get_repos(username):
  print(f"Buscando repositórios de {username}...")
  all_repos = []
  page = 1
  while True:
    url = f"https://api.github.com/users/{username}/repos"
    params = {"per_page": 100, "page": page, "sort": "updated", "direction": "desc"}
    resp = _make_request(url, params)
    if not resp: break
    chunk = resp.json()
    if not chunk: break
    all_repos.extend(chunk)
    print(f"📂 Página {page}: {len(chunk)} repositórios (Total: {len(all_repos)})")
    page += 1
    time.sleep(0.5)
  print(f"✅ Total de repositórios encontrados: {len(all_repos)}")
  return all_repos

def get_commit_activity(repo_full_name, max_tries=5):
  url = f"https://api.github.com/repos/{repo_full_name}/stats/commit_activity"
  for attempt in range(max_tries):
    try:
      resp = _make_request(url)
      if not resp:
        time.sleep(2)
        continue
      if resp.status_code == 202:
        print(f"⏳ GitHub calculando stats... (tentativa {attempt + 1}/{max_tries})")
        time.sleep(2 + attempt)
        continue
      data = resp.json()
      if isinstance(data, list) and len(data) > 0:
        return data
      print(f"📭 Sem dados de commit para {repo_full_name}")
      return []
    except Exception as e:
      print(f"❌ Erro ao buscar atividade de commits: {e}")
      time.sleep(2)
  return []