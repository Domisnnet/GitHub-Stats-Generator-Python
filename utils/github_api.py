import requests
import time
<<<<<<< HEAD
import os
from datetime import datetime
# 🔑 Usa a variável de ambiente PERSONAL_GITHUB_TOKEN
PERSONAL_GITHUB_TOKEN = os.getenv("PERSONAL_GITHUB_TOKEN", "")
# Headers com autenticação
HEADERS = {
  "Accept": "application/vnd.github.v3+json",
  "User-Agent": "DomisDev-GitHub-Stats/1.0"
}
# Corrige o nome da variável aqui para bater com a definida acima
if PERSONAL_GITHUB_TOKEN:
  HEADERS["Authorization"] = f"token {PERSONAL_GITHUB_TOKEN}"
  print("✅ Autenticação com token ativada!")
else:
  print("⚠️ AVISO: Sem token! Limite de 60 req/hora. Crie PERSONAL_GITHUB_TOKEN no .env")

def _make_request(url, params=None):
  """Função auxiliar para fazer requisições com tratamento de rate limit"""
  max_retries = 3
  for attempt in range(max_retries):
    try:
      resp = requests.get(url, headers=HEADERS, params=params)
      # Verifica rate limit
      remaining = resp.headers.get('X-RateLimit-Remaining', 'unknown')
      reset_time = resp.headers.get('X-RateLimit-Reset', 'unknown')
      print(f"📡 Requisição: {url[:60]}... (Rate limit restante: {remaining})")
      if resp.status_code == 403 and remaining == '0':
        print(f"⚠️ Rate limit atingido! Reset em: {datetime.fromtimestamp(int(reset_time))}")
        time.sleep(60)  # Espera 1 minuto
        continue
      resp.raise_for_status()
      return resp
      
    except requests.exceptions.RequestException as e:
      print(f"❌ Erro na requisição (tentativa {attempt + 1}/{max_retries}): {e}")
      if attempt < max_retries - 1:
        time.sleep(2 ** attempt)  # Espera exponencial
      else:
        raise     
  return None
=======
>>>>>>> 2d2dcfe0165c2716d30aa86007dbc1658d5d45dd

# Retorna dados básicos do perfil
def get_user(username):
<<<<<<< HEAD
  """Retorna dados básicos do perfil"""
  print(f"Buscando perfil de {username}...")
  resp = _make_request(f"https://api.github.com/users/{username}")
  if resp:
    return resp.json()
  return {}
=======
    resp = requests.get(f"https://api.github.com/users/{username}")
    resp.raise_for_status()
    return resp.json()
>>>>>>> 2d2dcfe0165c2716d30aa86007dbc1658d5d45dd

# ✅ PEGA TODAS AS PÁGINAS — resolve "só‑20‑só‑30‑faltam‑repos"
def get_repos(username):
<<<<<<< HEAD
  """✅ PEGA TODAS AS PÁGINAS — resolve 'só‑20‑só‑30‑faltam‑repos'"""
  print(f"Buscando repositórios de {username}...")
  all_repos = []
  page = 1
  while True:
    url = f"https://api.github.com/users/{username}/repos"
    params = { "per_page": 100, "page": page, "sort": "updated", "direction": "desc" }
    resp = _make_request(url, params)
    if not resp:
      break
    chunk = resp.json()
    if not chunk:
      break
    all_repos.extend(chunk)
    print(f"📂 Página {page}: {len(chunk)} repositórios (Total: {len(all_repos)})")
    page += 1
    time.sleep(0.5)  # Pequena pausa para não estourar rate limit
  print(f"✅ Total de repositórios encontrados: {len(all_repos)}")
  return all_repos

def get_events(username):
  print(f"Buscando eventos de {username}...")
  all_events = []
  page = 1
  while True:
    url = f"https://api.github.com/users/{username}/events"
    params = {"per_page": 100, "page": page}
    resp = _make_request(url, params)
    if not resp:
      break
    chunk = resp.json()
    if not chunk:
      break
    all_events.extend(chunk)
    page += 1
    time.sleep(0.3)
  return all_events

def get_commits_per_repo(repo_full_name):
  print(f"💻 Buscando commits de {repo_full_name}...")
  url = f"https://api.github.com/repos/{repo_full_name}/commits"
  params = {"per_page": 100}
  resp = _make_request(url, params)
  if resp:
    return resp.json()
  return []

def get_commit_activity(repo_full_name, max_tries=5):
  """✅ Trata quando GitHub ainda está calculando (202 / vazio)"""
  url = f"https://api.github.com/repos/{repo_full_name}/stats/commit_activity"
  
  for attempt in range(max_tries):
    try:
      resp = _make_request(url)
      if not resp:
        time.sleep(2)
        continue 
      # Status 202 = GitHub ainda está calculando
      if resp.status_code == 202:
        print(f"⏳ GitHub calculando stats... (tentativa {attempt + 1}/{max_tries})")
        time.sleep(2 + attempt)  # Espera progressivamente mais
        continue  
      data = resp.json()
      # Resposta pronta: lista não‑vazia → devolve
      if isinstance(data, list) and len(data) > 0:
        return data
      print(f"📭 Sem dados de commit para {repo_full_name}")
      return []
    except Exception as e:
      print(f"❌ Erro ao buscar atividade de commits: {e}")
      time.sleep(2)
  return []  # Sem dados após todas as tentativas
=======
    all_repos = []
    page = 1
    while True:
        url = (
            f"https://api.github.com/users/{username}/repos"
            f"?per_page=100&page={page}"
        )
        resp = requests.get(url)
        resp.raise_for_status()
        chunk = resp.json()
        if not chunk:
            break
        all_repos.extend(chunk)
        page += 1
    return all_repos

def get_events(username):
    all_events = []
    page = 1
    while True:
        resp = requests.get(
            f"https://api.github.com/users/{username}/events"
            f"?per_page=100&page={page}"
        )
        chunk = resp.json()
        if not chunk:
            break
        all_events.extend(chunk)
        page += 1
    return all_events

def get_commits_per_repo(repo_full_name):
    resp = requests.get(
        f"https://api.github.com/repos/{repo_full_name}/commits"
        f"?per_page=100"
    )
    resp.raise_for_status()
    return resp.json()

# ✅ Trata quando GitHub ainda está calculando (202 / vazio)
def get_commit_activity(repo_full_name, max_tries=5):
    url = f"https://api.github.com/repos/{repo_full_name}/stats/commit_activity"
    for attempt in range(max_tries):
        resp = requests.get(url)
        data = resp.json()
        # Resposta pronta: lista não‑vazia → devolve
        if isinstance(data, list) and len(data) > 0:
            return data
        # Espera progressivamente mais longo
        time.sleep(1 + attempt)
    # Sem dados / repos vazio / sem commits no ano
    return []
>>>>>>> 2d2dcfe0165c2716d30aa86007dbc1658d5d45dd
