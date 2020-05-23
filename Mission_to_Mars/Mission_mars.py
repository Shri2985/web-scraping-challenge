from flask import Flask, render_template, redirect
import pandas as pd
import pymongo
from flask_pymongo import PyMongo
from splinter import Browser
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
import cssutils


def scrape_info():
	executable_path = {'executable_path': 'chromedriver.exe'}
	browser = Browser('chrome', **executable_path, headless=False)
	#b#rowser = init_browser()
	url ='https://mars.nasa.gov/news/'
	browser.visit(url)	
	time.sleep(3)
	# Mars News
	html = browser.html
	soup = BeautifulSoup(html, 'html.parser')
	# news11=soup.find_all('div', class_="content_title")
	# news12=soup.find_all('div', class_="article_teaser_body")
	# news1=news11[1].text
	# news2=news12[0].text
	news1 = soup.find_all('div', class_="content_title")[1].text
	news2 = soup.find_all('div', class_="article_teaser_body")[0].text


	####JPL Mars Space Images - Featured Image
	url1 ='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
	browser.visit(url1)
	time.sleep(1)
	html1 = browser.html
	soup = BeautifulSoup(html1, 'html.parser')
	image = soup.find_all('article', class_="carousel_item")[0]["style"]
	style=cssutils.parseStyle(image)
	url=style['background-image']
	url=url.replace('url(','').replace(')','')
	full_image = 'https://www.jpl.nasa.gov' + url

	### Mars Weather
	url2 ='https://twitter.com/marswxreport?lang=en'
	browser.visit(url2)
	time.sleep(1)
	html2 = browser.html
	soup = BeautifulSoup(html2, 'html.parser')
	weather1=soup.find_all('div', class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")
	weather=weather1[0].text
	
	####Mars Facts
	url3 = 'https://space-facts.com/mars/'
	tables = pd.read_html(url3)
	df = tables[0]
	df.columns = ['description','values']
	#df=df.set_index('description')
	htmldata = df.to_html(index = False)

	

	###Mars Hemispheres
	url4 ='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
	browser.visit(url4)
	time.sleep(1)
	html4 = browser.html
	soup = BeautifulSoup(html4, 'html.parser')
	image1 = soup.find_all('img', class_="thumb")[0]["src"]
	image2 = soup.find_all('img', class_="thumb")[1]["src"]
	image3 = soup.find_all('img', class_="thumb")[2]["src"]
	image4 = soup.find_all('img', class_="thumb")[3]["src"]
	image1_name=soup.find_all('h3')[0].text
	image2_name=soup.find_all('h3')[1].text
	image3_name=soup.find_all('h3')[2].text
	image4_name=soup.find_all('h3')[3].text


	image1 = 'https://astrogeology.usgs.gov'+image1
	image2 = 'https://astrogeology.usgs.gov'+image2
	image3 = 'https://astrogeology.usgs.gov'+image3
	image4 = 'https://astrogeology.usgs.gov'+image4


	mars_data = {
	"news1":news1,
	"news2":news2,
	"full_image":full_image,
	"weather":weather,
	"image1":image1,
	"image2":image2,
	"image3":image3,
	"image4":image4,
	"image1_name":image1_name,
	"image2_name":image2_name,
	"image3_name":image3_name,
	"image4_name":image4_name,
	"data":htmldata
	}

	# Close the browser after scraping
	browser.quit()
	# Return results
	return mars_data
