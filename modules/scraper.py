import time
from bs4 import BeautifulSoup
import requests
import os
from urllib.parse import urljoin
import re

class Scraper:
    def itemDetails(queue, itemName, currentPrice, itemUrl, itemPicture, oldPrice, itemID):

        headers = {"Accept-Language": "en-US,en;q=0.5"}
    
        for page in range(1,28,1): 

            page = requests.get("https://www.rightstufanime.com/category/Blu~ray?page=" + str(page) + "&show=96", headers=headers)

            soup = BeautifulSoup(page.text, 'html.parser')
    
            item_div = soup.find_all('div', class_='facets-items-collection-view-cell-span3')
  
            #sleep(randint(2,10))
            time.sleep(1)

            for container in item_div:

                #name = container.find('div', class_='facets-item-cell-grid-details').text
                name = container.find('a', class_='facets-item-cell-grid-title').text
                itemName.append(name)
        
                price = container.form.find('span', class_='product-views-price-lead').text
                currentPrice.append(price) 
        
                url_path = [item.get('href') for item in container.find_all('a', class_='facets-item-cell-grid-title')]
                BASE_URL = os.environ.get("BASE_URL", "https://www.rightstufanime.com")
                url = urljoin(BASE_URL, str(*url_path))
                itemUrl.append(url)

                picture = [item.get('src') for item in container.find_all('img')]
                itemPicture.append(*picture)
        
                old_price = container.form.find('div', class_='product-views-price-exact').text
                result = re.findall(r"[-+]?\d*\.\d+|\d+", old_price)
                #print(result)
                oldPrice.append(result[0]) #retrieve the first price (MSRP)
          
                ID = [item.get('data-item-id') for item in container.find_all('div')]
                itemID.append(ID[0])

        queue.put((itemName, currentPrice, itemUrl, itemPicture, oldPrice, itemID))

    def description(totalProducts, itemUrl):
    
        aboutProduct = []
    
        for page3 in range(0, totalProducts):
    
            page3 = requests.get(str(itemUrl[page3]))

            soup3 = BeautifulSoup(page3.text, 'html.parser')

            description_div = soup3.find_all('div', class_='product-details-information-tab-content-container')
        
            time.sleep(5)
        
            for container3 in description_div:
            
                about = container3.find('h2', class_='product-details-information-tab-content-panel-title').text
                aboutProduct.append(about)
            
        return aboutProduct
    
    def products():
        totalProducts = []

        page2 = requests.get("https://www.rightstufanime.com/category/Blu~ray?page=1&show=96")

        soup2 = BeautifulSoup(page2.text, 'html.parser')

        product_div = soup2.find_all('header', class_='facets-facet-browse-header')

        for container2 in product_div:
            totalProducts = container2['data-quantity']

            
        
        return totalProducts