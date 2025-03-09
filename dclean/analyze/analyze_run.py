from typing import Dict, Any, List, Tuple
from dclean.utils.get_recommendation import (
    get_recommendation_apt_install_no_recommends,
    get_recommendation_cache_clean, get_recommendation_run)

# Commands that are generally safe to merge in Dockerfile RUN instructions
SAFE_TO_MERGE = [
    "apt-get update", "apt-get install", "apk add", "yum install",
    "dnf install", "zypper install", "rm -rf", "wget", "curl", "tar -xzf",
    "unzip", "mv", "cp", "chmod +x", "ln -s"
]

# Commands that might be risky to merge due to side effects or dependencies
DANGEROUS_TO_MERGE = [
    "pip install", "npm install", "pnpm install", "yarn install",
    "composer install", "go get", "cargo build", "conda install",
    "gem install", "bundle install", "apk upgrade", "yum update", "dnf update",
    "zypper update", "pip cache purge", "npm cache clean --force", "groupadd",
    "useradd", "usermod", "mkdir", "chown", "chmod", "service", "systemctl",
    "update-alternatives", "ldconfig", "locale-gen", "echo \"export",
    "source /etc/profile"
]

# Dockerfile instructions that create a new layer or change context
CRITICAL_SEPARATORS = [
    "ENV", "ARG", "WORKDIR", "USER", "COPY", "ADD", "ONBUILD", "EXPOSE",
    "VOLUME", "LABEL", "ENTRYPOINT", "CMD"
]

# Commands that can be used to clean the cache
CACHE_CLEAN_COMMANDS = ["apt-get clean", "rm -rf /var/lib/apt/lists/*"]

# APT commands that should use --no-install-recommends flag
APT_INSTALL_COMMANDS = ["apt-get install", "apt install"]


def analyze_run(instructions: List[Dict[str, Any]]) -> List[str]:
    """
    Analyzes a list of RUN instructions and returns those that can be improved (merged).

    Args:
        instructions: List of parsed Dockerfile RUN instructions

    Returns:
        List of recommendations for improving RUN commands
    """

    if not instructions:
        return []

    run_commands: List[Tuple[str, int]] = []
    separators: List[Tuple[str, int]] = []
    recommendations: List[str] = []

    # Extract RUN commands and critical separators
    for instr in instructions:
        instr_type = instr.get("instruction", "").strip()
        value = instr.get("value", "").strip()
        line_number = instr.get("startline", -1)

        if instr_type in CRITICAL_SEPARATORS:
            separators.append((value, line_number))

        if instr_type == "RUN":
            run_commands.append((value, line_number))

            # Check for apt-get install without cache cleaning
            if any(apt_cmd in value for apt_cmd in APT_INSTALL_COMMANDS):
                has_cache_clean = any(clean_cmd in value
                                      for clean_cmd in CACHE_CLEAN_COMMANDS)
                if not has_cache_clean:
                    recommendations.append(
                        get_recommendation_cache_clean(CACHE_CLEAN_COMMANDS,
                                                       line_number + 1))

            # Check for apt install commands without --no-install-recommends
            for apt_cmd in APT_INSTALL_COMMANDS:
                if apt_cmd in value and "--no-install-recommends" not in value:
                    recommendations.append(
                        get_recommendation_apt_install_no_recommends(
                            line_number + 1, apt_cmd))

    # Find groups of consecutive RUN commands that can be merged
    if len(run_commands) >= 2:
        mergeable_groups = []
        current_group = [run_commands[0]]

        for i in range(1, len(run_commands)):
            prev_cmd, prev_line = run_commands[i - 1]
            curr_cmd, curr_line = run_commands[i]

            # Check if there's a separator between these commands
            separator_between = any(prev_line < sep_line < curr_line
                                    for _, sep_line in separators)

            if separator_between:
                # Start a new group if there was a separator
                if len(current_group) > 1:
                    mergeable_groups.append(current_group)
                current_group = [run_commands[i]]
                continue

            # Check if both commands contain safe-to-merge operations
            prev_safe_merge = any(keyword in prev_cmd
                                  for keyword in SAFE_TO_MERGE)
            curr_safe_merge = any(keyword in curr_cmd
                                  for keyword in SAFE_TO_MERGE)

            if prev_safe_merge and curr_safe_merge:
                current_group.append(run_commands[i])
            else:
                # Start a new group if commands aren't safe to merge
                if len(current_group) > 1:
                    mergeable_groups.append(current_group)
                current_group = [run_commands[i]]

        # Don't forget to add the last group if it's mergeable
        if len(current_group) > 1:
            mergeable_groups.append(current_group)

        # Generate recommendations for each mergeable group
        for group in mergeable_groups:
            if len(group) >= 2:
                cmds = [cmd for cmd, _ in group]
                lines = [line + 1 for _, line in group]
                recommendations.append(get_recommendation_run(lines, cmds))

    return recommendations
