# -*- coding: utf-8 -*-
"""
Created on Wed May 25 14:54:23 2022

@author: oadiguzel
"""


from time import sleep
from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
from tkinter import *
numFound = 0

master = Tk()
l1 = Label(master,text = "Please enter earphones brand(s)")
l1.pack()
l2 = Label(master,text = "(sony or sony,philips)")
l2.pack()
e = Entry(master)
e.pack()

e.focus_set()

def callback():
    global brands
    brands = e.get() # This is the text you may want to use later
    master.destroy()

b = Button(master, text = "OK", width = 10, command = callback)
b.pack()

mainloop()

def scraping(brands,page):
    global numFound
    url = f"https://www.cimri.com/bluetooth-kulaklik/en-ucuz-{brands}-bluetooth-kulaklik-fiyatlari?page={page}&sort=price%2Casc"
    result = requests.get(url)
    #print(result.text)
    
    soup = BeautifulSoup(result.text, "html.parser")
    #print(soup.prettify())
    
    dic = soup.find_all("script")
    #print(dic)
    
    jo = json.loads(soup.find('script', type='application/json').text)
    
    numFound = jo[list(jo.keys())[1]]["pageProps"]["search"]["numFound"]
    liste = jo[list(jo.keys())[1]]["pageProps"]["search"]["products"]

    full_dic = {}
    for i in liste:
        part_dic = {}
        part_dic["price"] = i["topOffers"][0]["price"]
        part_dic["title"] = i["title"]
        part_dic["url"] = "www.cimri.com" + i["url"]
        part_dic["rate"] = i["review"]["rate"]
        part_dic["merchant"] = i["topOffers"][0]["merchant"]["name"]
        part_dic["m-url"] = i["topOffers"][0]["merchant"]["url"]
        full_dic[i["id"]] = part_dic
        
    df = pd.DataFrame().from_dict(full_dic,orient="index")
    df = df.sort_values("price")
    df.index.name = "product_id"
    return df

df = pd.DataFrame()
page = 1
temp = scraping(brands,page)
while len(df) < numFound:
    temp = scraping(brands,page)
    if len(df) == 0:
        df = temp
    else:
        df = df.append(temp)
    page =+ 1
df = df.reset_index()
df.index = range(1,len(df)+1)
df.index.name = "queue"
df.to_csv("//Mac/Home/Desktop/earphone_list.csv")

print(df)
#driver.close()