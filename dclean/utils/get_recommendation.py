from typing import List


def get_recommendation_from(repository_name: str,
                            light_list: List[str]) -> str:
    """
    Get a recommendation for a lightweight version of a Docker image.
    """
    return (f"Try to use a lightweight version of the {repository_name} like "
            f"'{', '.join(light_list)}' and other images")


def get_recommendation_run(lines: List[int], cmds: List[str]) -> str:
    """
    Get a recommendation for a run command.
    """
    recommendation = f"Can merge RUN instructions at lines {', '.join(map(str, lines))}"
    for cmd in cmds:
        recommendation += f"  {cmd},"
    recommendation += "\nOptimization: use `&&` and `\\` to combine these commands"
    return recommendation
