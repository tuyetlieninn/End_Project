"""Create random sample projects through the API.

Usage (backend running, run from the repository root):
    python scripts/generate_projects.py                     # 30 projects, demo account
    python scripts/generate_projects.py --count 100
    python scripts/generate_projects.py --email you@example.com --password YourPass1
"""
import httpx

from common import base_parser, login, random_project


def main() -> None:
    parser = base_parser(__doc__)
    parser.add_argument("--count", type=int, default=30, help="number of projects to create")
    args = parser.parse_args()

    with httpx.Client(base_url=args.api, timeout=15) as client:
        login(client, args.email, args.password)
        created = 0
        for _ in range(args.count):
            res = client.post("/projects", json=random_project())
            if res.status_code == 201:
                created += 1
            else:
                print(f"Create failed: {res.status_code} {res.text[:200]}")
        total = client.get("/projects").json()["total"]
    print(f"Created {created}/{args.count} projects. Total projects now: {total}")


if __name__ == "__main__":
    main()
