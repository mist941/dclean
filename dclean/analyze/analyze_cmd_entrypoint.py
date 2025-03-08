from typing import Any, Dict
from dclean.utils.get_recommendation import get_recommendation_cmd_entrypoint


def analyze_cmd_entrypoint(instruction: Dict[str, Any] = None) -> str:
    """
    Analyze the CMD entrypoint syntax.
    
    Args:
        instruction: Dictionary containing the CMD instruction details.
            Expected keys: 'value', 'instruction', 'startline'
            
    Returns:
        List of recommendation strings. Empty list if no issues found.
    """
    if not instruction:
        return ""

    if not instruction or "value" not in instruction:
        return ""

    instr_type = instruction.get("instruction", "").strip()
    value = instruction.get("value", "").strip()
    line_number = instruction.get("startline", -1)

    if not value:
        return ""

    if not value.startswith("[") and not value.endswith("]"):
        return get_recommendation_cmd_entrypoint(line_number, instr_type)

    return ""
