from pathlib import Path
from typing import Dict, Callable, List, Any
from dockerfile_parse import DockerfileParser
from dclean.analyzers.analyze_run import analyze_run
from dclean.analyzers.analyze_from import analyze_from

# Type definition for analyzer functions
AnalyzerFunc = Callable[[Dict[str, Any]], List[str]]

# Dictionary mapping Dockerfile instructions to their analyzer functions
analyzers_dict: Dict[str, AnalyzerFunc] = {
    "FROM": analyze_from,
    "RUN": analyze_run,
}


def analyze_dockerfile(dockerfile_path: str) -> List[Dict[str, List[str]]]:
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

    run_instructions = []

    # Analyze each instruction
    for instruction, next_instruction in zip(parsed_file.structure,
                                             parsed_file.structure[1:]):
        instruction_type = instruction['instruction']

        if instruction_type == 'RUN':
            run_instructions.append(instruction)
        else:
            run_instructions = []

        if instruction_type == 'RUN' and next_instruction[
                'instruction'] == 'RUN':
            continue

        # Get the appropriate analyzer for this instruction
        analyzer = analyzers_dict.get(instruction_type)

        if analyzer is not None:
            # Run the analyzer and collect results
            prepared_instruction = instruction

            if instruction_type == 'RUN':
                prepared_instruction = run_instructions

            result = analyzer(prepared_instruction)
            results.append({
                'instruction': instruction_type,
                'analysis': result
            })
        else:
            # Log unsupported instructions
            results.append({
                'instruction':
                instruction_type,
                'analysis':
                f"No analyzer available for {instruction_type}"
            })
    # print(results)
    return results


if __name__ == "__main__":
    analyze_dockerfile("dockerfiles/Dockerfile")
