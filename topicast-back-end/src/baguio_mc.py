from queue import Queue

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import re
import time

def scrape_article(url):
    response = requests.get(str(url))
    soup = BeautifulSoup(response.content, 'html.parser')

    title = ''
    date = ''
    content =''

    try:
        title = soup.find('h1', attrs={'class': 'entry-title'}).text.strip()
        date = soup.find('span', attrs={'class': 'item-metadata posts-date'}).text.strip()
        try:
            content_raw = soup.find('div', attrs={'class': 'entry-content read-details'}).text.strip()
            delimiter = 'Continue Reading'
            content = content_raw.split(delimiter)[0]
        except NoSuchElementException:
            pass
    except NoSuchElementException:
        pass

    if len(title) == 0 or len(date) == 0  or len(content) == 0 :
        return ['empty', 'empty', 'empty']
    else:
        return [title, date, content]


def mc_navigate_scrape_website(user_input_date, return_dict):
    user_input_date = str(user_input_date)

    url = 'https://www.baguiomidlandcourier.com.ph/category/city/'
    counter = 0

    links = []

    while (url is not None) and (counter != 10):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            main_container = soup.find('div', attrs={'id': 'aft-archive-wrapper'})

            for news_div in soup.find_all('div', attrs={'class' : 'col-66 float-l pad read-details color-tp-pad'}):
                news_div_date = news_div.find('span', attrs={'class' : 'item-metadata posts-date'}).text.strip()
                news_div_date_formatted = datetime.strptime(news_div_date, '%B %d, %Y').strftime('%Y-%m-%d')

                if user_input_date == news_div_date_formatted:
                    news_div_title = news_div.find('div', attrs={'class' : 'read-title'})
                    news_div_h4 = news_div_title.find('h4')
                    news_div_href = news_div_h4.find('a').get('href')
                    links.append(news_div_href)

            next_page_url = soup.find('a', attrs={'class' : 'next page-numbers'}).get('href')
            if next_page_url is not None:
                url = str(next_page_url)
            else:
                url = None

            counter += 1
        except:
            pass

    bmc_news = {'title': [], 'date': [], 'content': []}
    for url in links:
        bmc_news_list = scrape_article(url)
        bmc_news['title'].append(bmc_news_list[0])
        bmc_news['date'].append(user_input_date)
        bmc_news['content'].append(bmc_news_list[2])

    if bmc_news:
        return_dict["baguio_mc"] = bmc_news
    else:
        return_dict['baguio_mc'] = bmc_news
    

if __name__ == "__main__":
    param = sys.argv[1]
    result = mc_navigate_scrape_website(param)