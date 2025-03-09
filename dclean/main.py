import click
import os
import sys
from typing import Optional
from dclean.analyze.main import analyze_dockerfile
from dclean.utils.get_analysis_result import get_analysis_result
from dclean.utils.get_colored_analysis_result import get_colored_analysis_result
from dclean.utils.get_colored_vulnerabilities_results import get_colored_vulnerabilities_results
from dclean.utils.get_vulnerabilities_results import get_vulnerabilities_results
from dclean import __version__


@click.group()
def cli():
    """DClean - Analyze Dockerfiles and Docker images"""
    pass


@cli.command()
def version():
    """Display the current version of dclean."""
    click.echo(f"dclean version {__version__}")


@cli.command()
@click.option('-o',
              '--output',
              type=click.Path(writable=True),
              help="File to save the analysis results.")
@click.option('-d', '--deep', is_flag=True, help="Enable deep analysis.")
@click.argument('dockerfile', type=click.Path(exists=True))
def analyze(dockerfile: str, output: Optional[str], deep: bool = False):
    """
    Analyze the given Dockerfiles and Docker images.
    """
    try:
        click.echo(f"Analyzing {dockerfile}...")
        recommendations, container_vulnerabilities = analyze_dockerfile(
            dockerfile, deep)

        if output:
            os.makedirs(os.path.dirname(output) or '.', exist_ok=True)
            with open(output, 'w') as f:
                f.write(get_analysis_result(
                    recommendations))  # Write plain text to file
                if container_vulnerabilities:
                    f.write("\n\n")
                    f.write(
                        get_vulnerabilities_results(container_vulnerabilities))
            click.echo(f"The results are saved in {output}")
        else:
            click.echo(get_colored_analysis_result(recommendations))
            if container_vulnerabilities:
                click.echo("\n")
                click.echo(
                    get_colored_vulnerabilities_results(
                        container_vulnerabilities))

    except Exception as e:
        click.echo(click.style(f"Error during analysis: {str(e)}",
                               fg="bright_red",
                               bold=True),
                   err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()
