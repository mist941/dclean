from typing import Dict, List
from dclean.utils.types import Instruction

recommendation_dict: Dict[Instruction, str] = {
    Instruction.FROM:
    "Try to use a slim version of the {repository_name} like '{slim_list}' and other images",
    Instruction.RUN: ""
}


def get_recommendation_from(repository_name: str, slim_list: List[str]) -> str:
    """
    Get a recommendation for a slim version of a Docker image.
    """
    return recommendation_dict[Instruction.FROM].format(
        repository_name=repository_name, slim_list=", ".join(slim_list))


def get_recommendation_run() -> str:
    """
    Get a recommendation for a slim version of a Docker image.
    """
    return recommendation_dict[Instruction.RUN]
