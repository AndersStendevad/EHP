import click
from regnskab.annotater import Annotater

@click.command()
@click.argument("name", default="world")
def regnskab(name):
    bot = Annotater(total=3) 
    tags = bot.annotate("hello")
    print(tags)
    click.echo(f'Hello {name}!')

if __name__ == '__main__':
    regnskab()
