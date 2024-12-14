import requests
import json
from typing import List, Dict
import sys

def fetch_user_repos(username: str) -> List[Dict]:
    """Fetch all public repositories for a given username."""
    repos = []
    page = 1
    per_page = 100  # Maximum allowed by GitHub API

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

            if not page_repos:  # No more repos to fetch
                break

            repos.extend(page_repos)

            # Check if we have more pages
            if 'next' not in response.links:
                break

            page += 1

        except requests.exceptions.RequestException as e:
            print(f"Error fetching repositories: {e}")
            sys.exit(1)

    # Final sort to ensure correct order
    return sorted(repos, key=lambda x: (x.get('stargazers_count', 0) or 0), reverse=True)

def generate_html(username: str, repos: List[Dict]) -> str:
    """Generate HTML page with repository information."""
    css_styles = """
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
            background-color: #f6f8fa;
            color: #24292e;
        }
        .header {
            text-align: center;
            padding: 2rem;
            margin-bottom: 3rem;
            background-color: #24292e;
            color: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .repo-grid {
            display: grid;
            gap: 1.5rem;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        }
        .repo-card {
            background-color: white;
            padding: 1.5rem;
            border-radius: 8px;
            border: 1px solid #e1e4e8;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            transition: transform 0.2s;
        }
        .repo-card:hover {
            transform: translateY(-2px);
        }
        .repo-name {
            color: #0366d6;
            text-decoration: none;
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            display: block;
        }
        .repo-name:hover {
            text-decoration: underline;
        }
        .repo-description {
            color: #586069;
            margin: 0.8rem 0;
            font-size: 0.9rem;
            line-height: 1.5;
        }
        .repo-meta {
            display: flex;
            gap: 1rem;
            color: #586069;
            font-size: 0.9rem;
            align-items: center;
        }
        .repo-language::before {
            content: '●';
            margin-right: 4px;
        }
        .repo-stars::before {
            content: '★';
            margin-right: 4px;
        }
    """

    repo_items = []
    for repo in repos:
        name = repo.get('name', '')
        description = repo.get('description', '') or 'No description available'
        url = repo.get('html_url', '')
        language = repo.get('language', '')
        stars = repo.get('stargazers_count', 0)

        repo_html = f"""
            <div class="repo-card">
                <a href="{url}" class="repo-name" target="_blank">{name}</a>
                <p class="repo-description">{description}</p>
                <div class="repo-meta">
                    {f'<span class="repo-language">{language}</span>' if language else ''}
                    <span class="repo-stars">{stars:,}</span>
                </div>
            </div>
        """
        repo_items.append(repo_html)

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{username}'s GitHub Portfolio</title>
        <style>
            {css_styles}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>{username}'s GitHub Portfolio</h1>
        </div>
        <div class="repo-grid">
            {''.join(repo_items)}
        </div>
    </body>
    </html>
    """

def main():
    if len(sys.argv) != 2:
        print("Usage: python portfolio_generator.py <github_username>")
        sys.exit(1)

    username = sys.argv[1]
    repos = fetch_user_repos(username)
    html_content = generate_html(username, repos)

    with open('portfolio.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Portfolio generated successfully for {username}!")

if __name__ == "__main__":
    main()
