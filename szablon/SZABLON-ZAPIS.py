#!/usr/bin/env python3
"""
SZABLON-ZAPIS.py — minimalny skrypt ciągłości: push plików projektu
do GitHub Contents API (bez klonowania, bez zależności).

Konfiguracja (zmiennych środowiskowych lub domyślnych poniżej):
  GITHUB_TOKEN  — PAT z uprawnieniem Contents (Read/Write) do repo
  GITHUB_REPO   — "user/repo"
  GITHUB_BRANCH — domyślnie "main"
  ZRODLO        — katalog lokalny do wysłania (np. ./docs)
  CEL           — prefiks ścieżki w repo (np. "docs")

Użycie:
  GITHUB_TOKEN=ghp_xxx GITHUB_REPO=user/repo python3 SZABLON-ZAPIS.py

Sekrety: token WYŁĄCZNIE ze zmiennej środowiskowej — nigdy w pliku,
nigdy w commicie. Ten plik jest bezpieczny do wrzucenia do repo.
"""
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO = os.environ.get("GITHUB_REPO", "USER/REPO")
BRANCH = os.environ.get("GITHUB_BRANCH", "main")
ZRODLO = Path(os.environ.get("ZRODLO", "."))
CEL = os.environ.get("CEL", "").strip("/")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
API = "https://api.github.com"


def gh(method: str, path: str, data: dict | None = None) -> dict:
    req = urllib.request.Request(
        API + path, method=method,
        data=json.dumps(data).encode() if data else None,
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "continuity-kit",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read() or b"{}")


def push_file(local: Path, repo_path: str) -> str:
    b64 = base64.b64encode(local.read_bytes()).decode()
    sha = None
    try:
        sha = gh("GET", f"/repos/{REPO}/contents/{repo_path}?ref={BRANCH}")["sha"]
    except urllib.error.HTTPError as e:
        if e.code != 404:
            raise
    payload = {"message": f"zapis: {repo_path}", "content": b64, "branch": BRANCH}
    if sha:
        payload["sha"] = sha
    res = gh("PUT", f"/repos/{REPO}/contents/{repo_path}", payload)
    return f"OK {repo_path} (commit {res['commit']['sha'][:7]})"


def main() -> None:
    if not TOKEN:
        sys.exit("Brak GITHUB_TOKEN — ustaw zmienną środowiskową.")
    files = [p for p in sorted(ZRODLO.rglob("*"))
             if p.is_file() and ".git" not in p.parts]
    if not files:
        sys.exit(f"Brak plików w {ZRODLO}")
    for p in files:
        rel = "/".join(filter(None, [CEL, p.relative_to(ZRODLO).as_posix()]))
        print(push_file(p, rel))
    print(f"Zapisano {len(files)} plików do {REPO}.")


if __name__ == "__main__":
    main()
