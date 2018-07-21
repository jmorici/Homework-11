from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd

def scrape():

    
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    latest_news = soup.find("li", class_="slide")
    news_title = latest_news.find("h3").text
    news_p = latest_news.find(class_="article_teaser_body").text

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    soup.find(class_="main_feature").footer.a["data-fancybox-href"]
    base_url = "https://www.jpl.nasa.gov"
    style = soup.find(class_="main_feature").find(class_="carousel_items").article["style"]
    featured_image_url = base_url + style.split("url")[1].strip(";(')")

    url = 'https://twitter.com/marswxreport?lang=en'

    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_weather = soup.find("li", class_="js-stream-item").find("p", class_="tweet-text").text

    url = 'https://space-facts.com/mars/'

    table = pd.read_html(url)[0]

    table.rename(columns={0:"metric", 1:"value"}, inplace=True)

    table_html = table.to_html(index=False)

    table_html = table_html.replace('\n', '')

    table_html = table_html.replace("<table border=\"1\" class=\"dataframe\">", "").replace("</table>", "").strip()

    url_parent = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(url_parent)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    base_url = "https://astrogeology.usgs.gov"
    links = [base_url + item.find(class_="description").a["href"] for item in soup.find_all("div", class_="item")]

    hemisphere_image_urls = []

    for url in links:
        
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        
        title = soup.find("div", class_="content").find("h2", class_="title").text.replace(" Enhanced", "")
        img_url = base_url + soup.find("img", class_="wide-image")["src"]
        
        hemisphere_image_urls.append({"title": title, "img_url": img_url})


    browser.quit()


    mars = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "table_html": table_html,
        "hemisphere_image_urls": hemisphere_image_urls
    }


    return mars
