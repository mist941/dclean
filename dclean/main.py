import click
import os
import sys
from typing import Optional
from dclean.analyze.main import analyze_dockerfile
from dclean.utils.get_analysis_result import get_analysis_result
from dclean.utils.get_colored_analysis_result import get_colored_analysis_result


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

        if output:
            os.makedirs(os.path.dirname(output) or '.', exist_ok=True)
            with open(output, 'w') as f:
                f.write(get_analysis_result(
                    recommendations))  # Write plain text to file
            click.echo(f"The results are saved in {output}")
        else:
            click.echo(get_colored_analysis_result(
                recommendations))  # Display colored output in terminal

    except Exception as e:
        click.echo(click.style(f"Error during analysis: {str(e)}",
                               fg="bright_red",
                               bold=True),
                   err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()
