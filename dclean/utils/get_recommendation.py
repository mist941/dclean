from typing import List


def get_recommendation_from(repository_name: str, light_list: List[str],
                            instruction_line: int) -> str:
    """
    Get a recommendation for a lightweight version of a Docker image.
    """
    return (
        f"Try to use a lightweight version of the {repository_name} at line "
        f"{instruction_line} like '{', '.join(light_list)}' and other images")


def get_recommendation_run(lines: List[int], cmds: List[str]) -> str:
    """
    Get a recommendation for a run command.
    """
    recommendation = f"Can merge RUN instructions at lines {', '.join(map(str, lines))}:"
    for cmd in cmds:
        recommendation += f"  {cmd},"
    recommendation += "\nUse `&&` and `\\` to combine these commands"
    return recommendation
