from typing import List


def get_recommendation_from(repository_name: str, light_list: List[str],
                            line: int) -> str:
    """
    Get a recommendation for a lightweight version of a Docker image.
    """
    return (
        f"Line {line}: Try to use a lightweight version of the "
        f"{repository_name} like '{', '.join(light_list)}' and other images")


def get_recommendation_run(lines: List[int], cmds: List[str]) -> str:
    """
    Get a recommendation for a run command.
    """
    recommendation = f"Line {', '.join(map(str, lines))}: Can merge RUN instructions"
    for cmd in cmds:
        recommendation += f"  {cmd},"
    recommendation += "\nUse `&&` and `\\` to combine these commands"
    return recommendation


def get_recommendation_cache_clean(clean_commands: List[str],
                                   line: int) -> str:
    """
    Get a recommendation for a cache clean command.
    """
    return (f"Line {line}: Consider adding cache cleaning commands like "
            f"'{' && '.join(clean_commands)}' to reduce image size.")
