import csv

import sys

import requests

from bs4 import BeautifulSoup as bs

import pandas as pd

filename = "gamelog.csv"

TAGS = {"PTS":26, "BLK": 23, "STL": 22, "AST": 21, "TRB": 20}




def openfile(filename):


    fields = []
    rows = []
    with open(filename, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)

        # extracting field names through first row
        fields = next(csvreader)

        # extracting each data row one by one
        for row in csvreader:
            rows.append(row)

        # get total number of rows

    #get rid of the blank rows

    newrows = []
    for i in range(len(rows)):

        if rows[i][1] != '':
            newrows.append(rows[i])



    return fields, newrows

def getFile(link, year):
    print("Getting Data From ", year)
    link = "https://www.basketball-reference.com/players/" + link[0] +"/" +link + "/gamelog/" + year

    r = requests.get(link)

    soup = bs(r.content, 'html.parser')


    table = soup.find('table', id='pgl_basic')
    def rowgetDataText(tr, coltag='td'): # td (data) or th (header)
        return [td.get_text(strip=True) for td in tr.find_all(coltag)]
    rows = []

    trs = table.find_all('tr')
    headerow = rowgetDataText(trs[0], 'th')
    if headerow: # if there is a header row include first
        rows.append(headerow)
        trs = trs[1:]
    for tr in trs: # for every table row
        rows.append(rowgetDataText(tr, 'td') ) # data row
    new_table = []

    removeLines = ['Did Not Dress', 'Inactive', 'Did Not Play', 'Not With Team', 'Player Suspended']

    for i in rows:

        if i != [] and i[7] not in removeLines and i[0] != 'Rk':
            new_table.append(i)

    #from here we have a table which just needs to be converted to csvfile

    csvfile = ""

    for i in new_table:

        for j in i:

            csvfile += j
            csvfile +=','


        csvfile+='\n'
    return csvfile

def writeCSV (csvText, mode):

    if mode == "w":

        with open('gamelog.csv', 'w') as out:
            out.write(csvText)

    elif mode == "a":

        with open('gamelog.csv', 'a') as out:
            out.write(csvText)



def lookup(name):

    link = ""

    r = requests.get("https://www.basketball-reference.com/players/" + name.split()[1][0].lower() + "/")

    soup = bs(r.content, 'html.parser')

    link = "https://www.basketball-reference.com" + soup.find("a", string=name).get("href").replace(".html", "/gamelog")

    return soup.find("a", string=name).get("href").split("/")[3].split(".")[0]

def getSeasons(name):

    seasons = []

    r = requests.get("https://www.basketball-reference.com/players/" + name[0] + "/"+ name + ".html")

    soup = bs(r.content, 'html.parser')

    table = soup.find("table", id="per_game")

    tbody = table.find('tbody')
    th_head = tbody.find_all('th')


    for i in th_head:

        seasons.append(i.text)

    #this gets rid of duplicates
    seasons = list(dict.fromkeys(seasons))

    #this cuts it down to only the first yea rin the season ex 2015-16 -> 2015

    for i in range(len(seasons)):

        seasons[i] = str(seasons[i][:2])+str(seasons[i][5:])

    return seasons


#this is a function that will use basketball references shot log of a player to track where specifically they shoot best from and how the distance affects their shot
def getShotPct(playerTag, distance = 23):

    #links should look like this 
    #https://www.basketball-reference.com/players/c/cartevi01/shooting/2020

    base_link = "https://www.basketball-reference.com/players/"

    return 0

player_name = lookup("Vince Carter")

print(player_name)