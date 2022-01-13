import click
import os
import pandas as pd
from pathlib import Path
from regnskab.annotater import Annotater
from regnskab.read import CsvReader
from regnskab.scrape import scrape
from regnskab.pdf import PDF
from regnskab.calculate import Sums, income, expences, konto

@click.command()
@click.argument("kontobevaegelser", type=click.File('r'))
@click.argument("bestillinger", type=click.File('r'))
@click.option('-s', '--scrape-enable')
def regnskab(
    kontobevaegelser: Path,
    bestillinger: Path,
    scrape_enable: bool,
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
    if scrape_enable:
        for order in scrape(orderlist):
            dfs = pd.concat([dfs, order])
            dfs.to_csv("out/"+os.path.basename(bestillinger.name), sep=";")
    else:
        print("scraping is disabled")
    pdf = PDF()
    pdf.add_page()
    pdf.add_title("Ølhullet Regnskab 2021")
    pdf.add_line()
   
    t = Sums()
    t(income(pdf, kontobevaegelser.name))
    t(expences(pdf, kontobevaegelser.name))
    pdf.add_text("Resultat")
    pdf.add_section("Resultat total", t.total, "B")
    
    konto(pdf, kontobevaegelser.name, bestillinger.name)


    
    
    pdf.output('../Ølhullet_regnskab.pdf', 'F')

if __name__ == '__main__':
    regnskab()

