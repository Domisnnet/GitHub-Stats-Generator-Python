import requests
import time

# Retorna dados básicos do perfil
def get_user(username):
    resp = requests.get(f"https://api.github.com/users/{username}")
    resp.raise_for_status()
    return resp.json()

# ✅ PEGA TODAS AS PÁGINAS — resolve "só‑20‑só‑30‑faltam‑repos"
def get_repos(username):
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
