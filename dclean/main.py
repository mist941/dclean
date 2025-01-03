import click


@click.group()
def cli():
    """Docker Dependency Cleaner"""
    pass


@cli.command()
@click.argument('dockerfile', type=click.Path(exists=True))
def analyze(dockerfile):
    """Analyze the given Dockerfile."""
    click.echo(f"Analyzing {dockerfile}...")


if __name__ == "__main__":
    cli()
