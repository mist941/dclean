from typing import Dict, Any


def analyze_add(instruction: Dict[str, Any] = None) -> str:
    """
    Analyze ADD instruction to check if it can be replaced with COPY.
    
    Args:
        instruction: Dictionary containing the ADD instruction details

    Returns:
        Recommendations for improving ADD commands
    """
    if not instruction or "value" not in instruction:
        return ""
