from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd



def init_browser():
   executable_path = {'executable_path': ChromeDriverManager().install()}
   browser = Browser('chrome', **executable_path, headless=False)

def scrape():
   browser = init_browser()
   mars_dict ={}

   # scraped the [Mars News Site](https://redplanetscience.com/)

   news_url = 'https://redplanetscience.com'

   browser.visit(news_url)

   html = browser.html

   news_soup = bs(html, 'html.parser')



  # Retrieve the latest news title and paragraph
   news_title = news_soup.find_all('div', class_='content_title')[0].text
   news_p = news_soup.find_all('div', class_='article_teaser_body')[0].text

 

   #JPL Mars Space Images - Featured Image

   images_url = 'https://spaceimages-mars.com'

   browser.visit(images_url)

   html = browser.html

   images_soup = bs(html, 'html.parser')



   #Retrieve featured image link
   relative_image_path = images_soup.find_all('img')[3]["src"]
   featured_image_url = images_url + relative_image_path
 


   # Mars facts to be scraped
   facts_url = 'https://galaxyfacts-mars.com'
   tables = pd.read_html(facts_url)



   mars_facts_df = tables[1]
   mars_facts_df.columns = ["Description", "Value"]
   mars_facts_df



   mars_html_table = mars_facts_df.to_html()
   mars_html_table
   mars_html_table.replace('\n', '')


   # Mars Hemispheres 

   hemispheres_url="https://marshemispheres.com/"
   browser.visit(hemispheres_url)
   hemispheres_html = browser.html
   hemispheres_soup = bs(hemispheres_html, 'html.parser')

   hemisphere_image_urls = []
   mars_hemispheres = hemispheres_soup.find_all('div', class_='item')


   for mar in mars_hemispheres:
      #Search title
      hemisphere = mar.find('div', class_="description")
      title = hemisphere.h3.text
   
      #Create link to find each hemispheres image URL.
      hemisphere_link = hemispheres_url + hemisphere.a["href"]    
      browser.visit(hemisphere_link)
      image_html = browser.html
      image_soup = bs(image_html, 'html.parser')
      image_url = image_soup.find('img', class_='wide-image')  
       
      #Create Python dictionary to store the data using the keys `img_url` and `title`.
      image_dict = {}
      image_dict['title'] = title
      image_dict['img_url'] = image_url
      #Append the dictionary with the image url string and the hemisphere title to a list. 
      hemisphere_image_urls.append(image_dict)


   mars_dict = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "fact_table": str(mars_html_table),
        "hemisphere_images": hemisphere_image_urls
   }

   return mars_dict

 




