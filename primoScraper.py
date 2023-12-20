import bs4, requests, webbrowser
import argparse

import argparse
import requests
from bs4 import BeautifulSoup, Tag
import json
import os
import platform
import requests
import re
import time as t
from datetime import datetime, time

LINK = "https://www.subito.it/annunci-italia/vendita/usato/?q=bici"
PRE_LINK_ANNUNCIO = "https://www.subito.it/biciclette"

"""
parser = argparse.ArgumentParser()
parser.add_argument("--add", dest='name', help="name of new tracking to be added")
parser.add_argument("--url", help="url for your new tracking's search query")
parser.add_argument("--minPrice", help="minimum price for the query")
parser.add_argument("--maxPrice", help="maximum price for the query")
parser.add_argument("--delete", help="name of the search you want to delete")
parser.add_argument('--daemon', '-d', dest='daemon', action='store_true',
                    help="keep refreshing search results forever (default delay 120 seconds)")
parser.set_defaults(daemon=False)
parser.add_argument('--delay', dest='delay', help="delay for the daemon option (in seconds)")
parser.set_defaults(delay=120)

args = parser.parse_args()

queries = dict()
apiCredentials = dict()
dbFile = "searches.tracked"
telegramApiFile = "telegram_api_credentials"

if __name__ == '__main__':

    ### Setup commands ###

    if args.list:
        print(datetime.now().strftime("%Y-%m-%d, %H:%M:%S") + " printing current status...")
        print_queries()

    if args.short_list:
        print(datetime.now().strftime("%Y-%m-%d, %H:%M:%S") + " printing quick sitrep...")
        print_sitrep()

    if args.url is not None and args.name is not None:
        run_query(args.url, args.name, False, args.minPrice if args.minPrice is not None else "null",
                  args.maxPrice if args.maxPrice is not None else "null", )
        print(datetime.now().strftime("%Y-%m-%d, %H:%M:%S") + " Query added.")

    if args.delete is not None:
        delete(args.delete)

    if args.activeHour is None:
        args.activeHour = "0"

    if args.pauseHour is None:
        args.pauseHour = "0"

    # Telegram setup

    if args.token is not None and args.chatid is not None:
        apiCredentials["token"] = args.token
        apiCredentials["chatid"] = args.chatid
        save_api_credentials()

    ### Run commands ###

    if args.refresh:
        refresh(True)

    print()
    save_queries()

    if args.daemon:
        notify = False  # Don't flood with notifications the first time
        while True:
            if in_between(datetime.now().time(), time(int(args.activeHour)), time(int(args.pauseHour))):
                refresh(notify)
                notify = True
                print()
                print(str(args.delay) + " seconds to next poll.")
                save_queries()
            t.sleep(int(args.delay))
"""

response = requests.get(LINK)
response.raise_for_status()
soup=bs4.BeautifulSoup(response.text, 'html.parser')
div_annunci=soup.find('div', class_='ListingContainer_col__1TZpb ListingContainer_items__3lMdo col items')
##p_prezzo=soup.find('p', class_='index-module_price__N7M2x SmallCard-module_price__yERv7 index-module_small__4SyUf')

a_annunci=div_annunci.find_all('a')
p_paragraf=div_annunci.find_all('p')
link_annunci = []
prezzi_annunci = []

##for p_prezzi in p_paragraf:
##p_prezzo = str(p_prezzo.get('p'))
    
from pprint import pprint

for a_annuncio in a_annunci:
    link_annuncio = str(a_annuncio.get('href'))
    price=''.join(text.strip() for text in a_annuncio.p.find_all(text=True, recursive=False))
    pprint(price)
    pprint(link_annuncio)
    if PRE_LINK_ANNUNCIO in link_annuncio:
        link_annunci.append(link_annuncio)
        

##pprint(a_annuncio)
##pprint(''.join(text.strip() for text in a_annuncio.p.find_all(text=True, recursive=False)))
#pprint(link_annunci)

#from pprint import pprint
#print(link_annunci)

f = open('risultati_salvati.txt', 'a')
old_link_annunci = [riga.rstrip('\n') for riga in open('risultati_salvati.txt')]
new_link_annunci = []

for link_annuncio in link_annunci:
    if link_annuncio not in old_link_annunci:
        new_link_annunci.append(link_annuncio)
        f.write('%s\s' % link_annuncio)
f.close()

#if new_link_annunci:
#    print('ci sono nuovi risultati')
#    for new_link in new_link_annunci:
#        webbrowser.open(new_link)
#else:
#    print('nuovo annuncio')
input('tutto apposto bro')
