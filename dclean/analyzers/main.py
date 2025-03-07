from pathlib import Path
from typing import Dict, List
from dockerfile_parse import DockerfileParser
from dclean.analyzers.analyze_run import analyze_run
from dclean.analyzers.analyze_from import analyze_from
from dclean.analyzers.analyze_add import analyze_add


def analyze_dockerfile(dockerfile_path: str) -> List[Dict[str, str]]:
    """
    Analyze a Dockerfile and return the analysis results.
    
    Args:
        dockerfile_path: Path to the Dockerfile to analyze
        
    Returns:
        List of analysis results for each instruction
    
    Raises:
        FileNotFoundError: If the Dockerfile doesn't exist
        KeyError: If an instruction doesn't have a corresponding analyzer
    """
    # Validate file exists
    path = Path(dockerfile_path)
    if not path.exists():
        raise FileNotFoundError(f"Dockerfile not found at {dockerfile_path}")

    # Parse the Dockerfile
    parsed_file = DockerfileParser(path=dockerfile_path)

    results = []

    for instruction in parsed_file.structure:
        if instruction['instruction'] == "FROM":
            recommendation = analyze_from(instruction)
            if recommendation:
                results.append({
                    'instruction': "FROM",
                    'analysis': recommendation
                })
        elif instruction['instruction'] == "ADD":
            recommendation = analyze_add(instruction)
            if recommendation:
                results.append({
                    'instruction': "ADD",
                    'analysis': recommendation
                })

    for recommendation in analyze_run(parsed_file.structure):
        if recommendation:
            results.append({'instruction': "RUN", 'analysis': recommendation})

    return results
