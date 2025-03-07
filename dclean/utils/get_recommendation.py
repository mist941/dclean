from typing import List


def get_recommendation_from(repository_name: str, light_list: List[str],
                            line: int) -> str:
    """
    Get a recommendation for a lightweight version of a Docker image.
    """
    return (
        f"Line {line}: Try to use a lightweight version of the "
        f"{repository_name} like '{', '.join(light_list)}' and other images.")


def get_recommendation_run(lines: List[int], cmds: List[str]) -> str:
    """
    Get a recommendation for a run command.
    """
    recommendation = f"Line {', '.join(map(str, lines))}: You can merge RUN instructions"
    for cmd in cmds:
        recommendation += f" {cmd},"
    recommendation += "\nUse `&&` and `\\` to combine these commands."
    return recommendation


def get_recommendation_cache_clean(clean_commands: List[str],
                                   line: int) -> str:
    """
    Get a recommendation for a cache clean command.
    """
    return (f"Line {line}: Consider adding cache cleaning commands like "
            f"'{' && '.join(clean_commands)}' to reduce image size.")


def get_recommendation_add_for_data_retrieving(line: int) -> str:
    """
    Get a recommendation for an ADD command that retrieves data from the internet.
    """
    return (
        f"Line {line}: Consider using RUN with "
        f"curl or wget instead of ADD when retrieving data from the Internet.")


def get_recommendation_add_for_archives(line: int) -> str:
    """
    Get a recommendation for an ADD command that retrieves archives.
    """
    return (f"Line {line}: Consider using COPY instead of ADD when "
            f"retrieving archives if you do not need to extract them.")


def get_recommendation_cmd_entrypoint(line: int, instruction: str) -> str:
    """
    Get a recommendation for a CMD entrypoint syntax.
    """
    return (
        f"Line {line}: Use `[]` to specify an array of commands in the "
        f"{instruction}. For example: `CMD [\"echo\", \"Hello, World!\"]`.")


def get_recommendation_apt_install_no_recommends(line: int,
                                                 apt_cmd: str) -> str:
    """
    Get a recommendation for an apt-get install command without --no-install-recommends.
    """
    return (f"Line {line}: Consider adding '--no-install-recommends' to "
            f"{apt_cmd} to reduce image size "
            f"by not installing recommended but non-essential packages.")
