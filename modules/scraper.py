import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
from requests_html import HTMLSession
import os
from urllib.parse import urljoin
import re

class Scraper:
    def itemDetails(queue):

        headers = {"Accept-Language": "en-US,en;q=0.5"}
        itemName = []
        currentPrice = []
        itemUrl = []
        itemPicture = []
        oldPrice = []
        itemID = []
    
        for page in range(1,28,1): 

            chrome_options = Options()
            chrome_options.add_argument("--headless")  # Enable headless mode
            chrome_options.add_argument("--log-level=3")

            # Create a new instance of the browser with configured options
            driver = webdriver.Chrome(options=chrome_options)

            driver.get("https://www.rightstufanime.com/category/Blu~ray?page=" + str(page) + "&show=96")
            wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
            element = wait.until(EC.visibility_of_element_located((By.ID, "search-result-title")))

            html_content = driver.page_source

            soup = BeautifulSoup(html_content, 'html.parser')
    
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
        totalProducts = 0

        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Enable headless mode
        chrome_options.add_argument("--log-level=3")

        # Create a new instance of the browser with configured options
        driver = webdriver.Chrome(options=chrome_options)

        driver.get("https://www.rightstufanime.com/category/Blu~ray")

        wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
        element = wait.until(EC.visibility_of_element_located((By.ID, "search-result-title")))

        html_content = driver.page_source

        soup2 = BeautifulSoup(html_content, 'html.parser')

        h1_tag = soup2.find('h1', class_='facets-facet-browse-title')

        if h1_tag is not None:
            totalProducts = h1_tag.get('data-quantity')
            
        return totalProducts
