import json
import sys
import requests
from typing import List, Dict

def fetch_sorted_repos(username: str) -> List[Dict]:
    """Fetch repositories using the same method as portfolio_generator.py"""
    repos = []
    page = 1
    per_page = 100

    while True:
        url = f"https://api.github.com/users/{username}/repos?page={page}&per_page={per_page}&sort=stars&direction=desc"
        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'X-GitHub-Api-Version': '2022-11-28'
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            page_repos = response.json()

            if not page_repos:
                break

            repos.extend(page_repos)

            if 'next' not in response.links:
                break

            page += 1

        except requests.exceptions.RequestException as e:
            print(f"Error fetching repositories: {e}")
            sys.exit(1)

    return sorted(repos, key=lambda x: (x.get('stargazers_count', 0) or 0), reverse=True)

def verify_sorting(username: str = "octocat") -> None:
    """Verify that repositories are properly sorted by stars."""
    repos = fetch_sorted_repos(username)

    if not repos:
        print("Error: No repositories found")
        sys.exit(1)

    print("Top repositories by stars:")
    print("-" * 50)

    for i, repo in enumerate(repos[:5], 1):
        name = repo.get('name', 'N/A')
        stars = repo.get('stargazers_count', 0)
        print(f"{i}. {name}: {stars} stars")

    # Verify the sort order is correct
    star_counts = [repo.get('stargazers_count', 0) or 0 for repo in repos]
    is_sorted = all(star_counts[i] >= star_counts[i+1] for i in range(len(star_counts)-1))

    print("\nSort verification:")
    print(f"Star counts: {star_counts[:5]}")
    print(f"\nCorrectly sorted by stars: {'✓' if is_sorted else '✗'}")

    if not is_sorted:
        print("\nError: Repositories are not properly sorted!")
        sys.exit(1)
    else:
        print("\nSuccess: Repositories are correctly sorted by stars!")

def main():
    username = sys.argv[1] if len(sys.argv) > 1 else "octocat"
    verify_sorting(username)

if __name__ == "__main__":
    main()
