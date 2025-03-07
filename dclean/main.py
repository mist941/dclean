import click
import os
import sys
from typing import Optional
from dclean.analyzers.main import analyze_dockerfile


@click.group()
def cli():
    """Docker Dependency Cleaner - Analyze and optimize Docker dependencies"""
    pass


@cli.command()
@click.option('-o',
              '--output',
              type=click.Path(writable=True),
              help="File to save the analysis results.")
@click.argument('dockerfile', type=click.Path(exists=True))
def analyze(dockerfile: str, output: Optional[str]):
    """
    Analyze the given Dockerfile for issues and optimization opportunities.
    """
    try:
        click.echo(f"Analyzing {dockerfile}...")
        recommendations = analyze_dockerfile(dockerfile)

        if not recommendations:
            result = "Analysis results: Dockerfile has no issues"
        else:
            # Format the recommendations in a more readable way
            result = "Analysis Results:\n" + "=" * 50 + "\n\n"
            for i, recommendation in enumerate(recommendations, 1):
                result += f"Issue #{i}:\n"
                result += f"    Instruction: {recommendation['instruction']}\n"
                result += f"    {recommendation['analysis']}\n\n"
            result += "=" * 50

        if output:
            os.makedirs(os.path.dirname(output) or '.', exist_ok=True)
            with open(output, 'w') as f:
                f.write(result)
            click.echo(f"The results are saved in {output}")
        else:
            click.echo(result)

    except Exception as e:
        click.echo(f"Error during analysis: {str(e)}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()
