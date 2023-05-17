from queue import Queue

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import re
import time
import json


def scrape_article(slug, user_input_date):
    post = {'slug': str(slug)}
    url = "https://new.baguio.gov.ph/api/news/article"
    headers = {
        "authority": "new.baguio.gov.ph",
        "method": "POST",
        "path": "/api/news/article",
        "scheme": "https",
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.5",
        "authorization": "Bearer null",
        "content-length": "84",
        "content-type": "application/json",
        "origin": "https://new.baguio.gov.ph",
        "referer": f"https://new.baguio.gov.ph/news/{str(slug)}",
        "sec-ch-ua": '"Brave";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    }
    
    response = requests.post(url, json=post, headers=headers)
    
    title = ''
    date = ''
    content =''

    # repeatable process           
    
    try:
        if response.status_code == 200:
            data = json.loads(response.text)
            for item in data["data"]:
                title = item['title']
                date = user_input_date
                content = item['body']
        else:
            print("Failed to fetch data")
    except NoSuchElementException:
        pass
    
    if len(title) == 0 or len(date) == 0  or len(content) == 0 :
        return ['empty', 'empty', 'empty']
    else:
        return [title, date, content]


def bn_navigate_scrape_website(user_input_date, return_dict):
    user_input_date = str(user_input_date)
    headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'}
    url = f'https://new.baguio.gov.ph/api/news/search?page=1&office=0&keyword=&from={user_input_date}&to={user_input_date}&admin=undefined&barangay=undefined&public=true'

    response = requests.get(url)
    links = []

    if response.status_code == 200:
        data = json.loads(response.text)
        for item in data["data"]:
            links.append(item["slug"])
    else:
        print("Failed to fetch data")

    if links:
        bn_news = {'title': [], 'date': [], 'content': []}

        for url in links:
            bn_news_list = scrape_article(url, user_input_date)
            bn_news['title'].append(bn_news_list[0])
            bn_news['date'].append(bn_news_list[1])
            bn_news['content'].append(bn_news_list[2])

        if bn_news:
            return_dict['baguio_news'] = bn_news
        else:
            return_dict['baguio_news'] = bn_news

    else:
        return ['none']


if __name__ == "__main__":
    param = sys.argv[1]
    result = bn_navigate_scrape_website(param)