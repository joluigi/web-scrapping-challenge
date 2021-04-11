
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import requests
from urllib.request import urlopen as uReq


def mars_scraping():

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # 1. Latest Mars news extraction

    # Visiting URL
    url = "https://redplanetscience.com/"
    browser.visit(url)

    # Obtaining data
    html = browser.html
    soup = bs(html, 'html.parser')

    title_list = []
    art_list = []

    title = soup.find_all('div', class_='content_title')
    article = soup.find_all('div', class_='article_teaser_body')

    for titl, art in zip(title, article):
        print(f'Title: {titl.text}')
        print(f'Article extract: {art.text}')
        print('----------------------------------')
        title_list.append(titl.text)
        art_list.append(art.text)

    # 2. Featured Img URL
    # Visiting URL
    space_img_url = "https://spaceimages-mars.com/"
    browser.visit(space_img_url)

    # Scraping the image from the URL

    html_img = browser.html
    soup_img = bs(html_img, 'html.parser')

    header_img = soup_img.find('img', class_="headerimage")['src']

    featured_image_url = space_img_url+header_img

    print(featured_image_url)

    # 3. Mars fact table Extraction
    # Visiting URL

    facts_url = "https://galaxyfacts-mars.com/"
    browser.visit(facts_url)

    # Extracting the tables
    data_tables = pd.read_html(facts_url)
    data_tables[1]

    # 4. Mars Hemisphere image extraction 

    # Visiting the URL
    mult_img_url = ("https://marshemispheres.com/")
    browser.visit(mult_img_url)


    # Scraping the site for Hemisphere images
    mult_img_html = browser.html
    soup = bs(mult_img_html, 'html.parser')

    art_list = soup.find_all('a', class_='itemLink product-item')
    h3_list = soup.find_all('h3')
    mars_img_list = []


    for n, h3 in enumerate(h3_list):

        try:                   
            browser.links.find_by_partial_text(h3.text).click()
            crrnt_page = browser.html
            #print(crrnt_page)
            page_soup = bs(crrnt_page, 'html.parser')
            img_download = page_soup.find_all('div', class_='downloads')
            img_href = img_download[0].a['href']
            print(h3.text)
            mars_img_list.append({'title '+str(n):h3.text, 'img url '+str(n):mult_img_url+img_href})
            print('------------------')
            browser.visit(mult_img_url)

        except:
            browser.visit(mult_img_url)
            print("Scraping finished going back to first page") 
            break
    mars_tot_data ={

        'lat_news': {'title':title_list, 'article':art_list},
        'feat_image':featured_image_url,
        'mars_tables': data_tables,
        'hem_list': mars_img_list
    }

    browser.quit()

    print(mars_img_list)

    return mars_tot_data