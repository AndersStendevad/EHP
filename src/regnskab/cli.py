import click
from pathlib import Path
from regnskab.annotater import Annotater
from regnskab.csv import CsvReader

@click.command()
@click.argument("kontobevaegelser", type=click.File('r'))
@click.argument("bestillinger", type=click.File('r'))
def regnskab(
    kontobevaegelser: Path,
    bestillinger: Path,
    ):
    csv = CsvReader(kontobevaegelser)
    bot = Annotater(total=csv.total)
    for line in csv:
        bot.count += 1 + csv.count_skipped
        csv.count_skipped = 0
        tags = bot.annotate(f"{line.text} {line.date} {line.amount}")
        with open(csv.out+line.filename, "a") as out:
            out.write(f"{line.text};{line.date};{line.amount};{tags}\n")
    bot.save_tags()
    csv = CsvReader(bestillinger)
    bot = Annotater(total=csv.total)
    for line in csv:
        bot.count += 1 + csv.count_skipped
        csv.count_skipped = 0
        tags = bot.annotate(f"{line.text} {line.date} {line.amount}")
        with open(csv.out+line.filename, "a") as out:
            out.write(f"{line.text};{line.date};{line.amount};{tags}\n")
    bot.save_tags()

if __name__ == '__main__':
    regnskab()

