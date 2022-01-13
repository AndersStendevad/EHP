from fpdf import FPDF

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.WIDTH = 210
        self.HEIGHT = 297
        
    def header(self):
        # Custom logo and positioning
        # Create an `assets` folder and put any wide and short image inside
        # Name the image `logo.png`
        self.image('assets/logo.jpeg', 10, 8, 33)
        self.set_font('Arial', 'B', 11)
        self.cell(self.WIDTH - 80)
        self.cell(60, 1, 'Regnskab Ølhullet', 0, 0, 'R')
        self.ln(60)
        
    def footer(self):
        # Page numbers in the footer
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def add_title(self, string: str):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, string, 0, 1)

    def add_line(self):
        self.set_font('Courier', 'B', 12)
        line = "_"
        self.cell(0, 10, line*74, 0, 1)

    @staticmethod
    def ddk(i):
        minus = ""
        if i < 0:
            minus = "- "
        if 10 <= i < 100 or -10 >= i > -100:
            return minus+f"0,{str(abs(i))} kr."
        elif 0 <= i < 10 or 0 >= i > -10:
            return minus+f"0,0{str(abs(i))} kr."
        num = str(abs(i))
        dot = "." if num[:-5] else "" 
        dot2 = "." if num[:-8] else "" 
        num = f"{minus}{num[:-8]}{dot2}{num[-8:-5]}{dot}{num[-5:-2]},{num[-2:]} kr."
        return num

    def add_text(self, string: str):
        self.set_font('Courier', 'B', 12)
        self.cell(0, 10, string, 0, 1)

    def add_section(self, string: str, amount: int, style: str=""):
        self.set_font('Courier', style, 12)
        space = " "
        text = f"    {string}{space*(70-len(string)-len(self.ddk(amount)))}{self.ddk(amount)}"
        self.cell(0, 10, text, 0, 1)
