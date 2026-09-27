"""Overwrite EVERY existing project with random data through the API.

This replaces the data you already have, so it asks for confirmation first.
Usage (backend running, run from the repository root):
    python scripts/update_all_projects.py
    python scripts/update_all_projects.py --yes --email you@example.com --password YourPass1
"""
import httpx

from common import all_project_ids, base_parser, login, random_project


def main() -> None:
    parser = base_parser(__doc__)
    parser.add_argument("--yes", action="store_true", help="skip the confirmation prompt")
    args = parser.parse_args()

    with httpx.Client(base_url=args.api, timeout=15) as client:
        login(client, args.email, args.password)
        ids = all_project_ids(client)
        if not ids:
            print("No projects to update. Create some with: python scripts/generate_projects.py")
            return
        if not args.yes:
            try:
                answer = input(f"Overwrite all {len(ids)} projects with random data? Type 'yes' to continue: ")
            except EOFError:  # no interactive input available
                answer = ""
            if answer.strip().lower() != "yes":
                print("Cancelled.")
                return
        updated = 0
        for project_id in ids:
            res = client.put(f"/projects/{project_id}", json=random_project())
            if res.status_code == 200:
                updated += 1
            else:
                print(f"Update {project_id} failed: {res.status_code} {res.text[:200]}")
    print(f"Updated {updated}/{len(ids)} projects.")


if __name__ == "__main__":
    main()
