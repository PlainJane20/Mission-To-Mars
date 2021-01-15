# Dependencies
import requests
import time 
import re
import numpy as np
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pymongo

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

db = client.mars_db

# Mars news scraping
all_data = {}
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
response = requests.get(url)

# Create BeautifulSoup object; parse with 'html.parser'
soup = bs(response.text, 'html.parser')

results = soup.find_all('div',class_='slide')
results[0]

html = browser.html
soup = bs(html, 'html.parser')
print(soup.prettify())

# news_title = soup.find('div',class_='content_title').text
# print(news_title)

title_results = soup.find_all('div', class_='content_title')
nasa_titles = []
for result in title_results:
    nasa_titles.append(result.text.strip())
print(nasa_titles)

# news_p = soup.find('div',class_='rollover_description_inner').text
# print(news_p)

paragraph_results = soup.find_all('div', class_='rollover_description_inner')
nasa_paragraphs = []
for result in paragraph_results:
    nasa_paragraphs.append(result.text.strip())
print(nasa_paragraphs)

# JPL Mars Space Images

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

jplimage_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(jplimage_url)

# browser.click_link_by_partial_text("FULL IMAGE")
# browser.click_link_by_partial_text("more info")

# Use xpath of navbar to navigate to Featured Image
time.sleep(1)
xpath = '/html/body/div/div/div/header/div[1]/div[3]/div/nav/div[1]/div[4]/button/span'
browser.find_by_xpath(xpath).click()

time.sleep(1)
xpath = '/html/body/div/div/div/header/div[1]/div[3]/div/nav/div[1]/div[4]/div/div/div/div/div[1]/div/div/div/a/p[1]'
browser.find_by_xpath(xpath).click()

time.sleep(1)
xpath = '/html/body/div/div/div/main/div/div[2]/div/div/div[2]/button/span'
browser.find_by_xpath(xpath).click()

html = browser.html
soup = bs(html, "html.parser")

print(soup.prettify())

# Mars Facts

facts_url = "https://space-facts.com/mars/"
facts_tables = pd.read_html(facts_url)
df_mars_facts = facts_tables[0]
df_mars_facts.columns = ['Description', 'Value']
df_mars_facts.set_index('Description', inplace=True)

df_mars_facts.to_html('../Images/mars_facts.html')

facts_tables = pd.read_html(facts_url)
print(facts_tables)

mars_facts = df_mars_facts.to_html(header=True, index=True)
print(mars_facts)
all_data["mars_facts"] = mars_facts

# Mars Hemispheres
hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(hemispheres_url)
html = browser.html
soup = bs(html, "html.parser")
soup_links = soup.find_all('div', class_="description")
marshemisphere = []

hemtitles = soup.find_all('h3')
hemtitle = []
for name in hemtitles:
    print(name.text)

hemisphere_image_urls = []
hemi_dict = {}
all_data["url_hemisphere"] = []
for link in soup_links:
    url_hemisphere = 'https://astrogeology.usgs.gov' + link.find('a')['href']
    all_data["url_hemisphere"].append(url_hemisphere)

    print(url_hemisphere)
    browser.visit(url_hemisphere)
    time.sleep(1)

html = browser.html
soup = bs(html, 'html.parser')
title = soup.find('h2', class_='title').text
img_url = soup.find('img', class_='wide-image')['src']
hemi_dict["title"]= title
hemi_dict["img_url"]= 'https://astrogeology.usgs.gov' + img_url
hemisphere_image_urls.append(hemi_dict.copy())


all_data["hemisphere_image_urls"] = hemisphere_image_urls
print(all_data)
db.mars_info.insert_one(all_data)
