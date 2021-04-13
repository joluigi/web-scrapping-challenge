
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
    lat_new_dict = []
    i = 0

    title = soup.find_all('div', class_='content_title')
    article = soup.find_all('div', class_='article_teaser_body')
    
    print('------Article Extraction start-----')
    for titl, art in zip(title, article):
        i+=1
        print(f'Title: {titl.text}')
        print(f'Article extract: {art.text}')
        print('----------------------------------')
        title_list.append(titl.text)
        art_list.append(art.text)
        lat_new_dict.append([{'title':titl.text},{'art':art.text}])
    print('-----Article Extraction ended-------')

    # 2. Featured Img URL
    # Visiting URL
    print('Visiting SpaceImages url: Started')
    space_img_url = "https://spaceimages-mars.com/"
    browser.visit(space_img_url)
    print('Visiting SpaceImages url: Ended')

    # Scraping the image from the URL

    html_img = browser.html
    soup_img = bs(html_img, 'html.parser')

    header_img = soup_img.find('img', class_="headerimage")['src']

    featured_image_url = space_img_url+header_img
    print('-------Featured image process started-------')
    print(featured_image_url)
    print('-------Featured image process ended-------')

    # 3. Mars fact table Extraction
    # Visiting URL
    print('Visiting facts url: Started')
    facts_url = "https://galaxyfacts-mars.com/"
    browser.visit(facts_url)
    print('Visiting facts url: Ended')
    
    print('------Table Extraction started-------')
    # Extracting the tables
    data_tables = pd.read_html(facts_url)
    table_list = data_tables[0].set_index(0).drop('Mars - Earth Comparison')
    final_table = table_list.rename(columns={1:'Mars', 2:'Earth' })\
                    .to_dict('index')
    # Converting Table to HTML
    html_table = pd.DataFrame.to_html(table_list.rename(columns={1:'Mars', 2:'Earth' }))
    print(final_table)
    print('------Table Extraction ended-------')

    # 4. Mars Hemisphere image extraction 

    # Visiting the URL
    print('Visiting hemispheres url: Started')
    mult_img_url = ("https://marshemispheres.com/")
    browser.visit(mult_img_url)
    print('Visiting hemispheres url: Completed')

    print('------Hemisphere Extraction started-------')
    # Scraping the site for Hemisphere images
    mult_img_html = browser.html
    soup = bs(mult_img_html, 'html.parser')

    #art_list = soup.find_all('a', class_='itemLink product-item')
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
            mars_img_list.append([{'title':h3.text},{'img_link':mult_img_url+img_href}])
            browser.visit(mult_img_url)

        except:
            browser.visit(mult_img_url)
            print("Scraping finished going back to first page") 
            break
    print(mars_img_list)
    print('------Hemisphere Extraction started-------')

    mars_tot_data ={

        'lat_news': lat_new_dict,
        'feat_image':featured_image_url,
        'mars_tables': final_table,
        'hem_list': mars_img_list
    }

    print(mars_tot_data)

    browser.quit()
    return mars_tot_data