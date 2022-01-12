import click
import os
import pandas as pd
from pathlib import Path
from regnskab.annotater import Annotater
from regnskab.read import CsvReader
from regnskab.scrape import scrape

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
    with open("tags.txt", "w+") as file:
        for tag in bot._tags:
            file.write(f"{tag}\n")
    dfs = pd.DataFrame()
    orderlist = [line.split(";")[0].strip("\ufeff") for line in bestillinger.readlines()]
    print(orderlist)
    for order in scrape(orderlist):
        dfs = pd.concat([dfs, order])
        dfs.to_csv("out/"+os.path.basename(bestillinger.name), sep=";")

if __name__ == '__main__':
    regnskab()

