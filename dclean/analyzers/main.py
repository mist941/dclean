from pathlib import Path
from typing import Dict, Callable, List, Any
from dockerfile_parse import DockerfileParser
from .analyze_from import analyze_from

# Type definition for analyzer functions
AnalyzerFunc = Callable[[Dict[str, Any]], None]

# Dictionary mapping Dockerfile instructions to their analyzer functions
analyzers_dict: Dict[str, AnalyzerFunc] = {
    "FROM": analyze_from,
}


def analyze_dockerfile(dockerfile_path: str) -> List[Dict[str, Any]]:
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

    # Analyze each instruction
    for instruction in parsed_file.structure:
        instruction_type = instruction['instruction']

        # Get the appropriate analyzer for this instruction
        analyzer = analyzers_dict.get(instruction_type)

        if analyzer is not None:
            # Run the analyzer and collect results
            result = analyzer(instruction)
            results.append({'instruction': instruction, 'analysis': result})
        else:
            # Log unsupported instructions
            results.append({
                'instruction':
                instruction_type,
                'analysis':
                f"No analyzer available for {instruction_type}"
            })
    print(results)
    return results
