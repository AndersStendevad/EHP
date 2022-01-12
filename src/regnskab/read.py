from pathlib import Path

import pandas as pd
import os
from dataclasses import dataclass, field
from typing import List

@dataclass
class Line:
    text: str
    date: str
    amount: str
    filename: str
    tags: List[str] = field(default_factory=list)

class CsvReader:

    def __init__(self, file, out = "out/"):
        self.out = out
        self.filename = file.name
        self.total = len(file.readlines())
        self.count_skipped = 0

    def __iter__(self):
        seen = set()
        filename = os.path.basename(self.filename)
        if os.path.isfile(f'{self.out}{filename}'):
            df = pd.read_csv(f'{self.out}{filename}', sep=";")
            seen = set(df.index.tolist())
        else:
            with open(f'{self.out}{filename}', 'w+') as file:
                file.write("text;dato;beløb;tags\n")
        df = pd.read_csv("data/"+filename, sep=";")
        for row in df.itertuples(name='Line'):
            if row.Index in seen:
                self.count_skipped += 1
                continue
            yield Line(text =row.Tekst, date=row.Dato , amount=row.Beløb, filename = filename)
