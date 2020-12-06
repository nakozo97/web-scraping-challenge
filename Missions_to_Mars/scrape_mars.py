from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import requests
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()
    mars_data={}

    # Visit mars.nasa.gov/news - Collect the latest News Title and Paragraph Text.
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Retrieve the parent divs for all articles
    results = soup.find('ul', class_='item_list')
    news_title = results.find('div', class_="content_title").text
    news_p = results.find('div', class_="article_teaser_body").text

    # Visit the url for JPL Featured Space Image
    # https://splinter.readthedocs.io/en/latest/elements-in-the-page.html
    JPL_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(JPL_url)

    time.sleep(1)

    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_href('/spaceimages/details')

    # Scrape page into Soup
    html = browser.html
    image_soup = bs(html, "html.parser")

    # Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
    # Make sure to find the image url to the full size .jpg image.

    mars_image_path = image_soup.find('figure', class_="lede")
    featured_image_url = 'https://www.jpl.nasa.gov' + mars_image_path.a['href']
    print(f"{featured_image_url}")

    # Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    mars_facts_url = 'https://space-facts.com/mars/'
    
    tables = pd.read_html(mars_facts_url)
    df_tables = tables[0]
    df_tables.columns = ['Mars Facts', 'Measurements']
    df_tables = df_tables.set_index('Mars Facts')
    df_tables_html = df_tables.to_html()

    # Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres. You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
    mars_hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hemispheres_url)

    # Scrape page into Soup
    hemispheres_html = browser.html
    hemispheres_soup = bs(hemispheres_html, 'html.parser')

    # Retrieve the parent divs for all hemispheres
    results = hemispheres_soup.find_all('div', class_='item')

    hemispheres_image_urls = []

    for result in results: 
            hemispheres_title = result.find('div', class_="description").h3.text
            hemispheres_href = result.find('div', class_="description").a['href']

            # Scrape page into Soup to into image link
            browser.visit('https://astrogeology.usgs.gov'+ hemispheres_href)
            hemispheres_images_html = browser.html
            hemispheres_images_soup = bs(hemispheres_images_html, 'html.parser')

            images_results = hemispheres_images_soup.find('div', class_='downloads')
            img_url = images_results.find('li').a['href']

            # dictionary
            hemispheres_dict = {}
            hemispheres_dict['hemispheres_title'] = hemispheres_title
            hemispheres_dict['img_url'] = img_url
                                                                  
            hemispheres_image_urls.append(hemispheres_dict)   

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "df_tables_html": df_tables_html,
        "hemispheres_image_urls": hemispheres_image_urls

    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
