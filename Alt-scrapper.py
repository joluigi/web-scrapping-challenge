import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import requests
from urllib.request import urlopen as uReq

# Defining URL to scrape

url = "https://redplanetscience.com/"
client = uReq(url)
soup = bs(client.read(), 'html.parser')
print(soup.prettify())