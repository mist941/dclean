from typing import List


def get_recommendation_from(repository_name: str,
                            light_list: List[str]) -> str:
    """
    Get a recommendation for a lightweight version of a Docker image.
    """
    return (f"Try to use a lightweight version of the {repository_name} like "
            f"'{', '.join(light_list)}' and other images")


def get_recommendation_run() -> str:
    """
    Get a recommendation for a run command.
    """
    return "Combine RUN commands to reduce the number of layers"
