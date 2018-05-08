
# coding: utf-8

# In[ ]:



#import dependencies#import 
import time
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
from selenium import webdriver
import requests as req
import re

from splinter import browser
from selenium import webdriver


# In[ ]:




#scrape the NASA Mars News SIte, collect news title, paragraph text, assign#scrape t 
#to variables for later reference
url = "https://mars.nasa.gov/news/" 
response = req.get(url)

soup = bs(response.text, 'html5lib')

title = soup.find("div", class_="content_title").text
paragraph_text = soup.find("div", class_="rollover_description_inner").text


# In[ ]:


print(paragraph_text)


# In[128]:


#Visit the URL for JPL's Space images
#splinter to navigate the site and find the image url for the current featured
#image and assign it to featured_image_url (use .jpg)
executable_path = {'executable_path' : 'chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)
featured_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(url)


# In[129]:


html = browser.html
soup = bs(html, "html.parser")


# In[130]:


browser.click_link_by_partial_text('FULL IMAGE')
#time.sleep(5)


# In[131]:


browser.click_link_by_partial_text('more info')


# In[134]:


new_html = browser.html
new_soup = bs(new_html, 'html.parser')
temp_img_url = new_soup.find('img', class_='main_image')
back_half_img_url = temp_img_url.get('src')

featured_image_url = "https://www.jpl.nasa.gov" + back_half_img_url

print(featured_image_url)


# ## Mars Weather

# In[137]:



#get mars weather's latest tweet from the website#get mar 
url_weather = "https://twitter.com/marswxreport?lang=en"
browser.visit(url_weather)


# In[139]:


html_weather = browser.html
soup = bs(html_weather, "html.parser")
#temp = soup.find('div', attrs={"class": "tweet", "data-name": "Mars Weather"})
mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
print(mars_weather)


# ## Mars Facts

# In[140]:


#Mars Facts....visit webpage, use pandas to scrape the page for facts, 
#convert pandas table to html table string. 
request_mars_space_facts = req.get("https://space-facts.com/mars/")


# In[141]:


mars_space_table_read = pd.read_html(request_mars_space_facts.text)
mars_space_table_read


# In[142]:


df = mars_space_table_read[0]
df


# In[143]:


df.set_index(0, inplace=True)
mars_data_df = df
mars_data_df


# In[144]:


mars_data_html = mars_data_df.to_html()
mars_data_html


# In[145]:


mars_data_html.replace('\n', '')


# In[146]:


mars_data_df.to_html('mars_table.html')


# ## Mars Hemispheres

# In[164]:


#..Visit the USGS Astrogeology site to obtain hgih resolution images for 
#....each of Mar's hemispheres
usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(usgs_url)


# In[165]:


html = browser.html
soup = bs(html, 'html.parser')
mars_hemis=[]


# In[166]:


# loop through the four tags and load the data to the dictionary

for i in range (4):
    time.sleep(5)
    images = browser.find_by_tag('h3')
    images[i].click()
    html = browser.html
    soup = bs(html, 'html.parser')
    partial = soup.find("img", class_="wide-image")["src"]
    img_title = soup.find("h2",class_="title").text
    img_url = 'https://astrogeology.usgs.gov'+ partial
    dictionary={"title":img_title,"img_url":img_url}
    mars_hemis.append(dictionary)
    browser.back()


# In[167]:


print(mars_hemis)

