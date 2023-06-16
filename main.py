from requests import get
import pandas as pd
import numpy
import time
from multiprocessing import Pool
from urllib.parse import urljoin, urlencode
from time import sleep
from random import randint
import threading
import queue as queue
import discord
import os
from discord.ext import commands
from discord_webhook import DiscordWebhook, DiscordEmbed
from modules.scraper import Scraper
from modules.disc import Discord

activity = discord.Game(name = '-help')
intents = discord.Intents.default()
intents.typing = False  # Disable typing event
intents.presences = False  # Disable presence event
bot = commands.Bot(command_prefix='-', activity=activity, status=discord.Status.online, intents=intents)

start = time.time()

headers = {"Accept-Language": "en-US,en;q=0.5"}

total = Scraper.products()
print(total)
totalProduct = []
totalProduct.append(*total)
totalItems = int(totalProduct[0]) #convert the string product to an integer

itemID = []
itemName = []
itemUrl = []
itemPicture = []
currentPrice = []
oldPrice = []
aboutItem = []

queue = queue.Queue()
new_thread = threading.Thread(target=Scraper.itemDetails(itemName, currentPrice, itemUrl, itemPicture, oldPrice, itemID), args=(queue, ))
new_thread.start()
new_thread.join()
itemName, currentPrice, itemUrl, itemPicture, oldPrice, itemID = queue.get()

#itemName, currentPrice,itemUrl, itemPicture, oldPrice, itemID = itemDetails()
#pages = np.arange(1, 28) #pages 1-27 *NOT READING PAGE 12*

#print(itemUrl[1])        
#aboutItem = description(totalItems, itemUrl)        
        
items = pd.DataFrame({
'ID': itemID,
'Name': itemName,
'MSRP': oldPrice,
'Current Price': currentPrice,
'URL': itemUrl,
'Picture': itemPicture
})

items['Current Price'] = items['Current Price'].str.replace('$', '').astype(float)
items['MSRP'] = items['MSRP'].astype(float)
items['ID'] = items['ID'].astype(int)

pd.set_option('max_colwidth', 400)
pd.set_option('display.colheader_justify', 'center')

end = time.time()
hours, rem = divmod(end-start, 3600)
minutes, seconds = divmod(rem, 60)
print("HOURS:MINUTES:SECONDS:MS")
print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))

print(len(itemUrl))
#print(len(aboutItem))

# to see your dataframe
#print(items)
#display(items)

# to see the datatypes of your columns
print(items.dtypes)
tracker = []
    
bot.run(os.environ.get('DISCORD_TOKEN'))

search = input("Search for your desired Bluray or DVD: ")
print('\n')
found = items['Name'].str.contains(search)
#print(found)
limit = found.count()

for i in range(limit):
    if (found[i]):
        print('{:<9s}{:<139s}{:<10s}{:<10s}'.format('ID', 'Name', 'MSRP', 'Current Price'))
        print('{:<9d}{:<130s}{:<10.2f}{:<10.2f}'.format(items.loc[i].at['ID'], items.loc[i].at['Name'], items.loc[i].at['MSRP'], items.loc[i].at['Current Price']))
        print('\n')

add = int(input('Enter the Item ID You Would Like to Track: '))
print('\n')

found1 = items['ID'] == add
limit1 = found1.count()

for i in range(limit1):
    if (found1[i]):
        itemIndex = i
track_url = items.loc[itemIndex].at['URL']
print(track_url)
# to see where you're missing data and how much data is missing 
#print(items.isnull().sum())

# to move all your scraped data to a CSV file
items.to_csv('rightstufanime.csv')