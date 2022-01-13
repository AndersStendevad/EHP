import pandas as pd
import os

from regnskab.pdf import PDF

class Sums:
    def __init__(self):
        self.total = 0
    def __call__(self, i: int):
        self.total += i
        return i

def income(pdf: PDF, filename: str):
    df = pd.read_csv("out/"+os.path.basename(filename), sep = ";")
    df['beløb'] = df['beløb'].map(lambda x: x.replace(".", "").replace(",", ""))
    df['beløb'] = df['beløb'].map(lambda x: int(x)) 
    df['tags'] = df['tags'].map(lambda x: x.replace("['", "").replace("']", ""))
    df = df[df["beløb"] > 0]
    df = df[["beløb","tags"]]
    pdf.add_text("Indtægter")
    c = Sums()
    for key, value in df.groupby(['tags']).sum().iterrows():
        pdf.add_section(key, c(value[0]))
    pdf.add_section("Indtægter i alt", c.total, "B")
    return c.total

def expences(pdf: PDF, filename: str):
    df = pd.read_csv("out/"+os.path.basename(filename), sep = ";")
    df['beløb'] = df['beløb'].map(lambda x: x.replace(".", "").replace(",", ""))
    df['beløb'] = df['beløb'].map(lambda x: int(x)) 
    df['tags'] = df['tags'].map(lambda x: x.replace("['", "").replace("']", ""))
    df = df[df["beløb"] < 0]
    df = df[["beløb","tags"]]
    pdf.add_text("Udgifter")
    c = Sums()
    for key, value in df.groupby(['tags']).sum().iterrows():
        pdf.add_section(key, c(value[0]))
    pdf.add_section("Udgifter i alt", c.total, "B")
    return c.total

def konto(pdf: PDF, movements: str, orders: str):
    pdf.add_text("Kontoer")
    c = Sums()
    #pdf.add_section("Jyske Bank",c(5500000), "B")
    #pdf.add_section("Ny5",c(800000), "B")
    #pdf.add_section("Ny3",c(-2700000), "B")

    pdf.add_text("Balance")
    pdf.add_section("Balance total", c.total, "B")




