import re
from typing import Dict, Any, Optional
from dclean.utils.get_recommendation import (
    get_recommendation_add_for_archives,
    get_recommendation_add_for_data_retrieving)

URL_REGEX = r"^https?:\/\/(www\.)?[\da-z\.-]+\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$"
ARCHIVE_EXTENSIONS = ['.tar', '.gz', '.zip', '.xz', '.bz2', '.tgz']


def analyze_add(instruction: Optional[Dict[str, Any]] = None) -> str:
    """
    Analyze ADD instruction to check if it can be replaced with COPY or RUN.
    
    Args:
        instruction: Dictionary containing the ADD instruction details

    Returns:
        Recommendations for improving ADD commands
    """
    if not instruction or "value" not in instruction:
        return ""

    # More comprehensive URL regex that handles various URL formats

    # Handle multiple values (ADD can accept multiple sources)
    instruction_values = instruction.get("value", "").strip().split()
    instruction_line = instruction.get("startline", -1) + 1

    # Check if any of the values is a URL
    for value in instruction_values:
        if re.match(URL_REGEX, value):
            return get_recommendation_add_for_data_retrieving(instruction_line)

    # Check for archive files that should use COPY instead
    for value in instruction_values:
        if any(value.endswith(ext) for ext in ARCHIVE_EXTENSIONS):
            return get_recommendation_add_for_archives(instruction_line)

    return ""
