"""Shared helpers for the data scripts in this folder.

Credentials are never stored in the scripts: pass --email / --password, or set
SEED_EMAIL / SEED_PASSWORD. Without them the demo account below is used (it is
registered automatically on a fresh database).
"""
import argparse
import os
import random
import sys
from datetime import date, timedelta

import httpx
from faker import Faker

DEFAULT_EMAIL = "demo@example.com"
DEFAULT_PASSWORD = "Demo12345"

TECHS = ["react", "fastapi", "python", "aws", "docker", "typescript", "postgresql"]
PROJECT_TYPES = ["offshore", "ses", "lab", "new_dev", "maintenance"]
PHASES = ["requirements", "design", "implementation", "testing", "release", "maintenance_ops"]
INDUSTRIES = ["ITサービス", "製造業", "小売", "金融"]

fake = Faker("ja_JP")


def base_parser(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--api", default="http://127.0.0.1:8000", help="backend URL")
    parser.add_argument("--email", default=os.environ.get("SEED_EMAIL", DEFAULT_EMAIL))
    parser.add_argument("--password", default=os.environ.get("SEED_PASSWORD", DEFAULT_PASSWORD))
    return parser


def login(client: httpx.Client, email: str, password: str) -> None:
    """Log in (registering the account first if it does not exist) and set the auth header."""
    try:
        res = client.post("/auth/login", json={"email": email, "password": password})
    except httpx.HTTPError:
        sys.exit(f"Cannot reach the backend at {client.base_url}. Start it with: uvicorn app.main:app --reload")
    if res.status_code == 401:
        client.post("/auth/register", json={"email": email, "password": password})
        res = client.post("/auth/login", json={"email": email, "password": password})
    if res.status_code != 200:
        sys.exit(f"Login failed for {email}: {res.status_code} {res.text}")
    client.headers["Authorization"] = f"Bearer {res.json()['idToken']}"


def random_project() -> dict:
    """A valid random project (dates 2022-2026, some ongoing)."""
    start = date(random.randint(2022, 2026), random.randint(1, 12), random.randint(1, 28))
    ongoing = random.random() < 0.3
    end = None if ongoing else (start + timedelta(days=random.randint(30, 720))).isoformat()
    return {
        "customer_name": fake.company(),
        "project_name": fake.catch_phrase(),
        "description": fake.text(),
        "start_date": start.isoformat(),
        "end_date": end,
        "is_ongoing": ongoing,
        "team_size": random.randint(3, 15),
        "total_man_month": round(random.uniform(5, 50), 1),
        "source_note": fake.text(),
        "industry": random.choice(INDUSTRIES),
        "outcome_note": fake.text(),
        "team_composition_note": fake.text(),
        "technologies": random.sample(TECHS, random.randint(2, 5)),
        "project_types": random.sample(PROJECT_TYPES, random.randint(1, 2)),
        "dev_process_phases": random.sample(PHASES, random.randint(2, 5)),
    }


def all_project_ids(client: httpx.Client) -> list[int]:
    ids: list[int] = []
    page = 1
    while True:
        items = client.get("/projects", params={"page": page, "page_size": 100}).json()["items"]
        if not items:
            return ids
        ids.extend(item["id"] for item in items)
        page += 1
