import click
import os
import sys
from typing import Optional
from analyzers.main import analyze_dockerfile


@click.group()
def cli():
    """Docker Dependency Cleaner - Analyze and optimize Docker dependencies"""
    pass


@cli.command()
@click.option('-o',
              '--output',
              type=click.Path(writable=True),
              help="File to save the analysis results.")
@click.option('-v',
              '--verbose',
              is_flag=True,
              help="Turn on the detailed output.")
@click.argument('dockerfile', type=click.Path(exists=True))
def analyze(dockerfile: str, output: Optional[str], verbose: bool):
    """
    Analyze the given Dockerfile for issues and optimization opportunities.
    """
    try:
        click.echo(f"Analyzing {dockerfile}...")
        analyze_dockerfile(dockerfile)
        if verbose:
            click.echo("Analysis in detailed mode has been launched...")

        # TODO: Implement actual Dockerfile analysis logic here
        result = "Analysis results: Dockerfile is fine"

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
