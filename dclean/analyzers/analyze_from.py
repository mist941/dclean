import requests
from typing import Dict, Any, List


def getRepositoryTags(repository: str, version: str = None) -> List[str]:
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
    page = 1

    try:
        while True:
            response = requests.get(f"{api_url}?page={page}&page_size=100")

            # Break if we get an error response
            if response.status_code != 200:
                break

            data = response.json()
            results = data.get('results', [])

            # Break if no more results
            if not results:
                break

            # Add tags to our list
            tags.extend([item['name'] for item in results])

            # Check if there are more pages
            if not data.get('next'):
                break

            page += 1

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


def getRepositoryName(instruction_value: str) -> str:
    # First process digests if present
    if "@" in instruction_value:
        instruction_value = instruction_value.split("@")[0]

    # Split repository path and tag
    repo_part = instruction_value
    if ":" in instruction_value:
        # Check if colon is part of URL (has port) or tag separator
        parts = instruction_value.split("/")
        # If colon is in the first part (registry with port)
        if len(parts) > 1 and ":" in parts[0]:
            # Keep path with port unchanged, but remove tag if present
            last_part = parts[-1]
            if ":" in last_part:  # If last element contains a tag
                parts[-1] = last_part.split(":")[0]
                repo_part = "/".join(parts)
            else:
                repo_part = instruction_value
        else:
            # Regular tag processing
            repo_part = instruction_value.split(":")[0]

    # Handle registry domain if present (contains dots)
    parts = repo_part.split("/")
    if len(parts) > 1 and ("." in parts[0] or ":" in parts[0]):
        # Remove registry domain, keep the rest
        return "/".join(parts[1:])

    # Return the full repository name (including namespace if present)
    return repo_part


def getRepositoryVersion(instruction_value: str) -> str:
    """
    Extract the version/tag from a Docker image reference.
    
    Args:
        instruction_value: Docker image reference (e.g. 'nginx:1.21', 'ubuntu@sha256:123...')
        
    Returns:
        The version/tag string or 'latest' if no tag is specified
    """
    # First check if there's a digest
    if "@" in instruction_value:
        # For digest references, there might still be a tag before the digest
        pre_digest = instruction_value.split("@")[0]
        if ":" in pre_digest:
            # Handle cases like "nginx:1.21@sha256:123..."
            parts = pre_digest.split("/")
            last_part = parts[-1]
            if ":" in last_part:
                return last_part.split(":")[-1]
        # If no tag before digest, return 'latest'
        return "latest"

    # For regular image references with tags
    if ":" in instruction_value:
        parts = instruction_value.split("/")
        # Check if colon is in registry part (e.g., localhost:5000/image)
        if len(parts) > 1 and ":" in parts[0]:
            # Check if there's a tag in the last part
            last_part = parts[-1]
            if ":" in last_part:
                return last_part.split(":")[-1]
            else:
                return "latest"
        else:
            # Regular tag format (image:tag)
            return instruction_value.split(":")[-1]

    # No tag specified, default to 'latest'
    return "latest"


def analyze_from(instruction: Dict[str, Any]) -> List[str]:
    if not instruction or "value" not in instruction:
        return []

    instruction_value = instruction["value"]
    repository_name = getRepositoryName(instruction_value)
    current_version = getRepositoryVersion(instruction_value)

    # Get tags that match the current version
    tags = getRepositoryTags(repository_name, current_version)

    # Filter for slim versions
    slim_tags = [tag for tag in tags if "slim" in tag.lower()]

    # If no slim versions found for specific version, try all tags
    if not slim_tags:
        print(
            f"No slim versions found for {repository_name}:{current_version}, checking all tags"
        )
        all_tags = getRepositoryTags(repository_name)
        slim_tags = [tag for tag in all_tags if "slim" in tag.lower()]

    # If still no slim versions found, return empty list
    if not slim_tags:
        print(f"No slim versions found for {repository_name}")
        return []

    # Sort slim tags to prioritize newer versions
    slim_tags.sort(reverse=True)

    print(f"Found slim versions for {repository_name}: {slim_tags}")
    return slim_tags
