import click
from pathlib import Path
from regnskab.annotater import Annotater

@click.command()
@click.argument("kontobevaegelser", type=click.File('r'))
@click.argument("bestillinger", type=click.File('r'))
def regnskab(
    kontobevaegelser: Path,
    bestillinger: Path,
    ):
    
    print(kontobevaegelser, kontobevaegelser)

if __name__ == '__main__':
    regnskab()

