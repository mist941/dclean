import requests
from typing import List


def get_repository_tags(repository: str, version: str = None) -> List[str]:
    """
    Fetch available tags for a Docker Hub repository,
    optionally filtering by version.
    
    Args:
        repository: Repository name (e.g. 'ubuntu', 'nginx', 'username/repo')
        version: Optional version to filter by (e.g. '1.21', '3.9')
        
    Returns:
        List of available tags for the repository,
        filtered by version if specified
    """
    # Handle official repositories (no slash)
    if "/" not in repository:
        api_url = f"https://hub.docker.com/v2/repositories/library/{repository}/tags"
    else:
        api_url = f"https://hub.docker.com/v2/repositories/{repository}/tags"

    tags = []

    try:
        response = requests.get(f"{api_url}?page=1&page_size=100")

        data = response.json()
        results = data.get('results', [])

        # Add tags to our list
        tags.extend([item['name'] for item in results])

        # If version is specified, filter tags to match that version
        if version and version != "latest":
            # Extract major version (e.g., from "3.9.2" get "3.9")
            if "." in version:
                major_version = ".".join(version.split(".")[:2])
            else:
                major_version = version

            # Filter tags that contain the version
            filtered_tags = []
            for tag in tags:
                # Direct match
                if tag.startswith(
                        version
                ) or f"-{version}" in tag or f"_{version}" in tag:
                    filtered_tags.append(tag)
                # Major version match
                elif major_version != version and (
                        tag.startswith(major_version) or f"-{major_version}"
                        in tag or f"_{major_version}" in tag):
                    filtered_tags.append(tag)

            return filtered_tags

        return tags
    except Exception as e:
        print(f"Error fetching tags for {repository}: {str(e)}")
        return []
