"""Fetches GDP per capita and number of Secure Internet Server data from worldbank API and displays a scatter plot

Script requests 2016 GDP per Capita and 2016 Secure Internet Server metric data from WorldBank API
and displays a scatterplot to compare the two datasets.

File Name: WorldBankGrapherGDPvsInternetServers.py
Author: Shuen Yasui
Date created: 8/12/2017
Last Modified: 8/20/2017]
Python Version: 3.6
"""

import urllib
import requests
import time
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def scrapeGDP():
    #Fetch GDP per capita (current US$) from Worldbank
    url = "http://api.worldbank.org/countries/all/indicators/NY.GDP.PCAP.CD?format=json&date=2016&per_page=400"
    json_data = requests.get(url).json()
    f = open('GDPperCapita2016.txt', 'w', encoding="utf-8")
    for x in json_data[1]:
        v = x["value"]
        if v is None:
            v = "-1"
        txt = x["country"]["value"] + ";" + v + "\n"
        f.write(txt)
    f.close()
def scrapeIntServ():
    #Fetch Secure Internet servers (per 1 million people) from Worldbank
    url = "http://api.worldbank.org/countries/all/indicators/IT.NET.SECR.P6?format=json&date=2016&per_page=300"
    json_data = requests.get(url).json()
    f = open('SecIntServPer1mill2016.txt', 'w', encoding="utf-8")
    for x in json_data[1]:
        v = x["value"]
        if v is None:
            v = "-1"
        txt = x["country"]["value"] + ";" + v + "\n"
        f.write(txt)
    f.close()
def populateCountryHash(countryHash, lines, col):
    #Parses JSON data into hash-table.
    pastWorld = False
    for line in lines:
        if pastWorld:
            cEndPos = line.find(";", 0)
            cEndLine = line.find("\n", cEndPos)
            c = line[0:cEndPos]
            v = float(line[(cEndPos+1):cEndLine])
            if(v != -1):
                if countryHash.get(c, None) == None:
                    if col < 2:
                        countryHash[c] = [v]
                else:
                    countryHash[c].append(v)
            else:
                if countryHash.get(c, None) != None:
                    del countryHash[c]
        else:
            cEndPos = line.find(";", 0)
            c = line[0:cEndPos]
            if c == "World":
                pastWorld = True
def Main():
    # scrapeGDP() and scrapeIntServ() may be commented out if JSON data already fetched.
    scrapeGDP()
    scrapeIntServ()
    f = open('GDPperCapita2016.txt', 'r', encoding="utf-8")
    lines = f.readlines()
    f.close()
    countryHash = {}
    populateCountryHash(countryHash, lines, 1)
    f = open('SecIntServPer1mill2016.txt', 'r', encoding="utf-8")
    lines = f.readlines()
    f.close()
    populateCountryHash(countryHash, lines, 2)
    df = pd.DataFrame.from_dict(countryHash, orient='index')
    df.columns = ["GDP per capita", "Secure Internet servers (per 1 million people)"]
    sns.set(font_scale=0.9)
    sns.set_style("white")
    ax = sns.regplot(x="GDP per capita", y="Secure Internet servers (per 1 million people)", data=df, order=1, scatter_kws={"s": 20})
    ax = sns.regplot(x="GDP per capita", y="Secure Internet servers (per 1 million people)", data=df, order=2, scatter=None)
    ax.set_title("GDP per capita versus number of secure internet servers in 2016")
    for x in df.index:
        ax.annotate(x, (df.get_value(x,"GDP per capita"),df.get_value(x,"Secure Internet servers (per 1 million people)")))
    plt.show()
Main()