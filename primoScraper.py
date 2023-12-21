import asyncio
from pprint import pprint
import bs4, requests, webbrowser, argparse
from telegram import Bot

parser = argparse.ArgumentParser()
parser.add_argument("--object", dest='object', help="name of new tracking")
parser.add_argument("--category", dest='category', help="name of tracking category")
parser.add_argument("--minPrice", dest='minPrice', help="minimum price for the tracking")
parser.add_argument("--maxPrice", dest='maxPrice', help="maximum price for the tracking")
args = parser.parse_args()

BOT_TOKEN = 'YOUR_TOKEN'

CHAT_ID = 'YOUR_CHAT_ID'

async def invia_messaggio(msg):
    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=msg)

async def main():
    if args.object is not None and args.category is not None:
        LINK = "https://www.subito.it/annunci-italia/vendita/usato/?q="+args.object
        PRE_LINK_ANNUNCIO = "https://www.subito.it/"+args.category

        minPrice = -1
        maxPrice = -1

        response = requests.get(LINK)
        response.raise_for_status()
        soup=bs4.BeautifulSoup(response.text, 'html.parser')
        div_annunci=soup.find('div', class_='ListingContainer_col__1TZpb ListingContainer_items__3lMdo col items')

        a_annunci=div_annunci.find_all('a')
        p_paragraf=div_annunci.find_all('p')
        link_annunci = []
        prezzi_annunci = []

        if args.minPrice:
            minPrice = args.minPrice

        if args.maxPrice:
            maxPrice = args.maxPrice

        for a_annuncio in a_annunci:
            link_annuncio = str(a_annuncio.get('href'))
            price =''.join(text.strip() for text in a_annuncio.p.find_all(text=True, recursive=False))
            price = price[:-2]
            min_ = int(minPrice)
            max_ = int(maxPrice)
            pprint(price)
            if len(price)!=0:
                for c in ",.":
                    price = price.replace(c, "")
                p = int(price)
                if (min_ != -1 and min_ <= p) and (max_ != -1 and max_ >= p):
                    pprint(price)
                    pprint(link_annuncio)
                    await invia_messaggio("Nuovo Annuncio: "+link_annuncio)
                    if PRE_LINK_ANNUNCIO in link_annuncio:

                        link_annunci.append(link_annuncio)

        f = open('risultati_salvati.txt', 'a')
        old_link_annunci = [riga.rstrip('\n') for riga in open('risultati_salvati.txt')]
        new_link_annunci = []

        for link_annuncio in link_annunci:
            if link_annuncio not in old_link_annunci:
                new_link_annunci.append(link_annuncio)
                f.write('%s\s' % link_annuncio)
        f.close()

        # Invia una notifica Telegram per ogni nuovo link trovato
        ##for link in links:
        ##    bot = Bot(token=BOT_TOKEN)
        ##    bot.send_message(chat_id=CHAT_ID, text="messaggio")

        #if new_link_annunci: (--> web <--)
        #    print('ci sono nuovi risultati')
        #    for new_link in new_link_annunci:
        #        webbrowser.open(new_link)
        #else:
        #    print('nuovo annuncio')

        input('tutto apposto bro')


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
