from typing import List, Dict


def get_analysis_result(recommendations: List[Dict[str, str]]) -> str:
    if not recommendations:
        result = "Analysis results: Dockerfile has no issues"
    else:
        result = "Analysis Results:\n" + "=" * 50 + "\n\n"
        for i, recommendation in enumerate(recommendations, 1):
            result += f"Issue #{i}:\n"
            result += f"    Instruction: {recommendation['instruction']}\n"
            result += f"    Analysis: {recommendation['analysis']}\n\n"
        result += "=" * 50
    return result
