import requests


def fetch_user_profile(username: str):
    user_url = f"https://api.github.com/users/{username}"
    repos_url = f"https://api.github.com/users/{username}/repos?per_page=100"

    try:
        user_response = requests.get(user_url, timeout=10)

        if user_response.status_code == 404:
            print(f"Error: GitHub user '{username}' was not found (404).")
            return
        if user_response.status_code == 403:
            print("Error: GitHub API rate limit hit (403). Try again later.")
            return
        user_response.raise_for_status()

        user_data = user_response.json()

        repos_response = requests.get(repos_url, timeout=10)

        if repos_response.status_code == 403:
            print("Error: GitHub API rate limit hit (403) while fetching repositories.")
            return
        repos_response.raise_for_status()

        repos_data = repos_response.json()

        top_repos = sorted(
            repos_data,
            key=lambda repo: repo.get("stargazers_count", 0),
            reverse=True
        )[:5]

        print("\n=== GitHub Profile Summary ===")
        print(f"Username: {user_data.get('login', 'N/A')}")
        print(f"Bio: {user_data.get('bio') or 'No bio provided'}")
        print(f"Public Repositories: {user_data.get('public_repos', 0)}")
        print(f"Followers: {user_data.get('followers', 0)}")

        print("\nTop 5 Repositories by Stars:")
        if not top_repos:
            print("No public repositories found.")
        else:
            for repo in top_repos:
                name = repo.get("name", "N/A")
                stars = repo.get("stargazers_count", 0)
                language = repo.get("language") or "N/A"
                print(f"- {name} | Stars: {stars} | Language: {language}")

    except:
        print("Something went wrong while fetching the GitHub profile. Please check your internet connection and try again.")


if __name__ == "__main__":
    username_input = input("Enter GitHub profile name: ").strip()

    if not username_input:
        print("Error: Username cannot be empty.")
    else:
        fetch_user_profile(username_input)

