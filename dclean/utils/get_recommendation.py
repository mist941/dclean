from typing import Dict, List

recommendation_dict: Dict[str, str] = {
    "FROM":
    "Try to use a slim version of the {repository_name} like '{slim_list}' and other images",
    "RUN": ""
}


def get_recommendation_from(repository_name: str, slim_list: List[str]) -> str:
    """
    Get a recommendation for a slim version of a Docker image.
    """
    return recommendation_dict["FROM"].format(repository_name=repository_name,
                                              slim_list=", ".join(slim_list))
