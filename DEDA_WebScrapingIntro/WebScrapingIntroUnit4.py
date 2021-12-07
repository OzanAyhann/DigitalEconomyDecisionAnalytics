"""
DEDA Unit 4
OOP and Web Scraping Framework
Authors: Isabell Fetzer and Junjie Hu
"""


"""
Web Scraping encompasses any method allowing for extracting data from websites. Requests allows us to send an HTTP request to a webpage. BeautifulSoup parses the HTML in order to retrieve the desired information. 
Project: We wish to scrape the first page of the South China Morning Post’s news website. We acquire data about the news title, the news link and the news publication date and produce a tabular output stored as .csv file. 
"""
# Load moduls 
import requests
from bs4 import BeautifulSoup as soup
from datetime import datetime, date # needed to retrieve the date of publication 
# Receiving source code from the South China Morning Post website 
scmp_url = 'https://www.scmp.com/knowledge/topics/china-economy/news'
url_request = requests.get(scmp_url)


"""
After accessing the HTML page, BeautifulSoup allows for ‘parsing’ the webpage source code, i.e. analysing its syntax. In this regard, regular expression is extensively used. 
"""
# Returns the content of the response,  …
url_content = url_request.content # … in bytes
url_text = url_request.text # … in unicode
# Using BeautifulSoup to parse webpage source code
parsed_content = soup(url_content)
parsed_text = soup(url_text, 'lxml') # ‘html.parser’ also possible


"""
There are some of the most versatile methods in BeautifulSoup: 
find_all() retrieves matching tags from all the nested HTML tags, which are called descendants. If a list is passed in, all matching objects will be retrieved. 
"""
filtered_parts = parsed_text.find_all('div', class_ = "sc-bdfBwQ cMShZj") 
page_info = list() # create empty list 
# For loop iterates over every line in text 
for section in filtered_parts: 
    unit_info = dict() # create empty dictionary where we gradually attach items to
    # (1) Filter title, link and text content 
    filtered_part1 = section.find_all('a', class_ = "sc-hKgILt") 
    # print(filtered_part1[0])
    # (2) Refilter to obtain date
    filtered_part2 = section.find_all('span', class_ = 'sc-iqHYGH hkvqJt') # for date 
    # print(filtered_part2[0])
    if filtered_part1 == []: # Error handling 
        continue
    # (1) Filter title and link
    news_title = filtered_part1[2].text.strip() # find title item
    news_link = filtered_part1[0].get('href').strip() # find title item
    news_link = f"https://www.scmp.com{news_link}" # adjust link
    #print(news_title)
    #print(news_link)
    # Scanning scraped text (filtered_part1) for right titles 
    news_text = filtered_part1[3].text.strip() # find text 
    # print(news_link)
    # Correcting title errors 
    if section == filtered_parts[0]:
      news_title = news_title.replace(news_title, news_text) 
    for line in news_title: 
      if "|" in line: 
        news_title = f"{news_title} {news_text}"
    unit_info['news_title'] = news_title # add news_title to the dictionary
    unit_info['news_link'] = news_link # add news_link to the dictionary

     # (2) Filter date 
    try:
      news_date = datetime.strptime(filtered_part2[0].text.strip(),'%d %b %Y - %H:%M%p')
      news_date = news_date.date() # cuts off the time 
      # print(news_date)
    except:
      t_day = date.today()
      date_series = filtered_part2[0].text.strip()
      if (date_series.endswith('hours ago')) or (date_series[1].startswith('minutes ago')):
        news_date = t_day
      else:
        news_date = t_day
    
    unit_info['news_time'] = news_date # add news_date to the dictionary
    page_info.append(unit_info) # attach dictionary to list
print(page_info)

# Load moduls 
import pandas as pd
import os
direct = os.getcwd()
# Calling DataFrame constructor on our list 
df = pd.DataFrame(page_info, columns=['news_title', 'news_link', 'news_time'])
print(df)
# Exporting to .csv file 
df.to_csv(direct + '/CSMP_Scraped_News.csv')


"""
Object-Oriented Programming (OOP)
"""
"""
OOP aims to structure the program by bundling related properties and characteristics into individual objects. Classes are required to build objects. To define a class we use the keyword 'class' and should start with a capital letter, according to PEP8. Classes defined functions called methods, which identify the behaviours and properties that an object created from the class can perform with its data. 
"""
# The class Person is inherited from class object
class Person(object):
    # Using __init__ to initialize a class to take arguments
    # self is default argument that points to the instance
    def __init__(self, first, last, gender, age):
        self.first_name = first
        self.last_name = last
        self.gender = gender
        self.age = age

        
"""
Inheritance allows us to define a class that inherits all the methods and properties from another class. Hereby the class being inherited from is called base class or Parent class and the class that inherits from another class is referred to as derived class or Child class. Python provides the init method which creates instances automatically.
"""
class Student(Person):
   # The class Student inherited from class Person
    def __init__(self, first, last, gender, age, school):
     # super() method allows us to handle the arguments from parent class without copying
        super().__init__(first, last, gender, age)
        # Child class can also be added new arguments
        self.school = school
    def describe(self):  # describe is a method of class Student
        print('{0} {1} is a {2} years old {3} who studies at {4}.'.format( self.first_name,
                                                                          self.last_name,
                                                                          self.age,
                                                                          self.gender,
                                                                          self.school))
# student1 is an instance of class Student
student1 = Student('Laura', 'Doe', 'Female', 10 , 'C_School')
print(issubclass(Student, Person))
print(isinstance(student1, Student))
# Using the attributes in the object student1
print(student1.school)
# Using the methods in the object student1
print(student1.describe())


"""
We now alter the code in ReadRSS.py file by using the class. There are some methods with name surrounded by double underscore called ‘magic method’. Further more see: https://www.python-course.eu/python3_magic_methods.php
"""
# !pip install feedparser
import feedparser
class ReadRSS(object):
    def __init__(self, url):
        self.url = url
        self.response = feedparser.parse(self.url)
        
    def __eq__(self, other):
        # __eq__() is a magic method that enables comparison two object with ==
        if self.url == other.url:
            return True
        else:
            return False
        
    def __repr__(self):
    # __repr__() is a magic method that enables customization default printed format
        return "The website url is: " + self.url

    def get_titles(self):
        titles = []
        for item in self.response["entries"]:
            titles.append(item["title"])
        print("\nTITLES:\n")
        print('\n'.join(titles))
        return titles

    def get_specificitem(self, item_name):
        scripts = []
        for item in self.response["entries"]:
            scripts.append(item[f"{item_name}"])
        print(f"\n{item_name}:\n")
        print('\n'.join(scripts))
        return scripts
    
# ReadRSSClass is the file name of the module code
r = ReadRSS("https://feeds.a.dj.com/rss/RSSMarketsMain.xml")
r2 = ReadRSS("https://feeds.a.dj.com/rss/RSSMarketsMain.xml")
print(r)
print(f'The type of r is: {type(r)}')
if r == r2: # Here we use == to validate if two responses of two url are equal
    print("Two urls are the same")
else:
    print("Two urls are not the same")
# Print out the titles
titles = r.get_titles()


"""
Application: On Scraping Daily Weather Report of China Cities
"""
"""
This is a preliminary tutorial for scraping web pages
With a lot of comments, one can easily get touch web scraping with Python
Python Version: 3.6
@Author: Junjie Hu, jeremy.junjie.hu@gmail.com
"""
# Import all the packages you need, always remember that you can find 99% packages you need in python
import requests  # take the website source code back to you
import urllib  # some useful functions to deal with website URLs
from bs4 import BeautifulSoup as soup  # a package to parse website source code
import numpy as np  # all the numerical calculation related methods
import re  # regular expression package
import itertools  # a package to do iteration works
import pickle  # a package to save your file temporarily
import pandas as pd  # process structured data

save_path = 'output/'  # the path you save your files

base_link = 'http://www.tianqihoubao.com/lishi/'  # This link can represent the domain of a series of websites

def city_collection():
    request_result = requests.get(base_link)  # get source code
    parsed = soup(request_result.content)  # parse source code

    dt_items = parsed.find_all('dt')  # find the items with tag named 'dt'
    for item in dt_items:
        # iterate within all the items
        province_name = item.text.strip()  # get name of the province
        province_link2cities = item.find('a')['href']  # get link to all the cities in the province
        province = {'province_link': province_link2cities}
        provinces[province_name] = province  # save dict in the dict

    for province in provinces.keys():
        # iterate with the province link to find all the cities
        cities = {}
        print(provinces[province]['province_link'])
        request_province = requests.get(urllib.parse.urljoin(base_link, provinces[province]['province_link']))
        # use the urllib package to join relative links in the proper way
        parsed_province = soup(request_province.content)
        dd_items = parsed_province.find_all('dd')
        for dd_item in dd_items:
            print(dd_item)
            cities_items = dd_item.find_all('a')
            for city_item in cities_items:
                city_name = city_item.text.strip()
                city_link = city_item.get('href').split('.')[0]
                cities[city_name] = city_link
        provinces[province]['cities'] = cities
    return provinces

def weather_collection(link):
    """
    use the link to collect the weather data
    :param link: url link
    :return: dict, weather of a city everyday
    """
    weather_page_request = requests.get(link)
    parsed_page = soup(weather_page_request.content)
    tr_items = parsed_page.find_all('tr')
    month_weather = dict()
    for tr_item in tr_items[1:]:
        # print(tr_item)
        # daily_weather = dict()
        td_items = tr_item.find_all('td')
        date = td_items[0].text.strip()
        split_pattern = r'[\n\r\s]\s*'
        weather_states = ''.join(re.split(split_pattern, td_items[1].text.strip()))
        temperature = ''.join(re.split(split_pattern, td_items[2].text.strip()))
        wind = ''.join(re.split(split_pattern, td_items[3].text.strip()))
        month_weather[date] = {
            'weather': weather_states,
            'tempe': temperature,
            'wind': wind
        }
        # month_weather.append(daily_weather)
    return month_weather

# Nice way to get a date string with certain format
years = np.arange(start=2020, stop=2020)
months = np.arange(start=1, stop=13)
it = list(itertools.product(years, months))
date = [str(ele[0]) + format(ele[1], '02d') for ele in it]  # '02d' means 2 digits

#  ==== We have already download the links to all the cities=====
#  ==== Otherwise, uncomment the function below to retrieve provinces information ======
provinces = dict()  # initialize a dictionary to hold provinces information
# This dictionary includes 'province_link' which is the links to find the cities for each province and the 'cities' contains city names and links

# provinces_info = city_collection()  # Use this function to retrieve links to all the cities

# This is called context management, with open can close the document automatically when the
with open('output_cities_link.pkl', 'rb') as cities_file:  # write, change 'rb' -> 'wb'
    provinces_info = pickle.load(cities_file)
    print(provinces_info)
    # pickle.dump(provinces_info, cities_file)  # write

weather_record = dict()
# The structure is dict in dict
# first layer keyword is province name
# In each province you can find the cities
# In each city, you can find the date, in the date, you can find weather record

for key in provinces_info.keys():
    # Iterate over different provinces
    print(key)
    for city_name, city_link in provinces_info[key]['cities'].items():
        # Iterate cities within each provinces
        print(city_name)
        for month_date in date:
            # Iterate over different months
            print(city_name)
            print(month_date)
            print(provinces_info[key]['cities'][city_name])
            print("On Scraping...")
            month_weather = weather_collection(
                urllib.parse.urljoin(base_link, city_link) + '/month/' + month_date + '.html')
            weather_record[key] = {city_name: {month_date: month_weather}}
print('Finished Scraping.')

# Exercise: Try to convert the "json"-like format to pandas DataFrame
