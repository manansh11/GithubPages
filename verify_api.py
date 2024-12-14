import json
import sys
from typing import List, Dict

def verify_repo_fields(repos: List[Dict]) -> None:
    """Verify that all required fields are present in the repository data."""
    required_fields = ['name', 'html_url', 'description', 'stargazers_count', 'language']
    
    if not repos:
        print("Error: No repositories found in the response")
        sys.exit(1)
    
    sample_repo = repos[0]
    print('Required fields check:')
    all_present = True
    for field in required_fields:
        present = field in sample_repo
        print(f'{field}: {"✓" if present else "✗"}')
        all_present = all_present and present
    
    print('\nSample repository data:')
    for field in required_fields:
        print(f'{field}: {sample_repo.get(field)}')
    
    if not all_present:
        print("\nError: Some required fields are missing!")
        sys.exit(1)
    else:
        print("\nSuccess: All required fields are present!")

def main():
    # Read JSON data from stdin
    try:
        repos = json.load(sys.stdin)
        verify_repo_fields(repos)
    except json.JSONDecodeError:
        print("Error: Invalid JSON input")
        sys.exit(1)

if __name__ == "__main__":
    main()
