import requests
import pandas as pd
from time import sleep
from bs4 import BeautifulSoup

users = {"gl1":"Gl1",
"gl2": "Gl2",
"Gl. 3.": "Gl3",
"gl4": "Gl4",
"gl5_egmont": "Gl5",
"gl6": "Gl6",
"Gamle 7" : "Gl7",
"gamle8" : "Gl8",
"ml2_egmont": "Ml2",
"ML3_egmont": "Ml3",
"ml4":"Ml4",
"ml5": "Ml5",
"ml6": "Ml6",
"ML7_egmont": "Ml7",
"ml8_penthouse": "Ml8",
"Ny2": "Ny2",
"Ny3": "Ny3",
"NY4": "Ny4",
"Ny 5": "Ny5",
"ny6": "Ny6",
"ny7": "Ny7",
"Ny8": "Ny8",
"AU_egmont":"AU",
"EgmontX": "EgmontX",}

def get_sub_orders(s, url):
    rs = s.get(url).content
    print(url)
    sleep(0.5)
    soup = BeautifulSoup(rs, 'lxml')
    try:
        parsed_table = soup.find_all('table')[0]
    except:
        raise Exception("No table found")
    data = [[td.a['href'] if td.find('a') else 
        ''.join(td.stripped_strings)
             for td in row.find_all('td')]
            for row in parsed_table.find_all('tr')]
    try:
        return [("https://studenterbolaget.dk/"+order[0], users[order[2]]) for order in data[1:]]
    except KeyError:
        return [("https://studenterbolaget.dk/"+order[0], order[0]) for order in data[1:]]



def get_order(s, url, user):
    r = s.get(url).content
    print(url)
    sleep(0.5)
    df_list = pd.read_html(r)
    df = df_list[0]
    df["tags"] = user
    return df

def scrape(orderlist):
    s = requests.Session()
    var = input("studenterbolaget cookie name: ")
    cookie_name = var if var else ""
    var2 = input("studenterbolaget cookie value: ")
    cookie_value = var2 if var2 else "" 
    s.cookies.update({cookie_name: cookie_value})
    url_base = "https://studenterbolaget.dk/user/234/orders/"
    
    for order in orderlist:
        sub_orders = get_sub_orders(s, url_base+order)
        for url, user  in sub_orders:
            df = get_order(s,url, user)
            yield df

