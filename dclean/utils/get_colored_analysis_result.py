from typing import List, Dict
import click


def get_colored_analysis_result(recommendations: List[Dict[str, str]]) -> str:
    if not recommendations:
        return "Analysis results: Dockerfile has no issues"
    else:
        result = click.style("Analysis Results:", fg="yellow",
                             bold=True) + "\n" + "=" * 50 + "\n\n"
        # Loop through each recommendation and format it
        for i, recommendation in enumerate(recommendations, 1):
            result += click.style(f"Issue #{i}:", fg="red", bold=True) + "\n"
            result += click.style(
                "    Instruction: ",
                fg="cyan") + f"{recommendation['instruction']}\n"
            result += f"    {recommendation['analysis']}\n\n"
        result += "=" * 50
        return result
