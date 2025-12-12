import requests

def get_user(username):
    return requests.get(f"https://api.github.com/users/{username}").json()

def get_repos(username):
    return requests.get(f"https://api.github.com/users/{username}/repos?per_page=100").json()

def get_events(username):
    return requests.get(f"https://api.github.com/users/{username}/events?per_page=100").json()

def get_commits_per_repo(repo_full_name):
    url = f"https://api.github.com/repos/{repo_full_name}/commits?per_page=100"
    return requests.get(url).json()

def get_commit_activity(repo_full_name):
    url = f"https://api.github.com/repos/{repo_full_name}/stats/commit_activity"
    return requests.get(url).json()