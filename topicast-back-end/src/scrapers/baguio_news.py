from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import pandas as pd
from datetime import datetime
import re
import time

def scrape_baguio_news(date):
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')

    url = 'https://new.baguio.gov.ph/news'
    driver = webdriver.Chrome(options = options)
    driver.get(url)

    time.sleep(5)
    date_str = '2023-04-24'
    start_date_input = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[1]/div[1]/div/div/div[3]/div/div[1]/div/input')
    start_date_input.send_keys(Keys.CONTROL + 'a')
    start_date_input.send_keys(Keys.DELETE)
    start_date_input.send_keys(pd.to_datetime(date_str).strftime('%m/%d/%Y'))
    time.sleep(10)
    end_date_input = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[1]/div[1]/div/div/div[3]/div/div[2]/div/input')
    end_date_input.send_keys(Keys.CONTROL + 'a')
    end_date_input.send_keys(Keys.DELETE)
    end_date_input.send_keys(pd.to_datetime(date_str).strftime('%m/%d/%Y'))
    end_date_input.send_keys(Keys.RETURN)

    b_news = {
        "title": [],
        "date": [],
        "content": []
    }

    while True:
        article_links = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[1]/div[1]/div/div/div[4]/div')

        links_raw = article_links.find_elements(By.TAG_NAME, 'a')
        links = [link.get_attribute('href') for link in links_raw]

        print(links)

        for link in links:
            time.sleep(3)
            # Navigate to the article URL and scrape the title, date, and content
            driver.get(link)
            title = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[1]/div[1]/div[1]/div[2]/div/div[1]/div/div/div[1]/span').text
            date = date_str                             
            contents_raw = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[1]/div[1]/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div/div')
            contents_raw2 = contents_raw.find_elements(By.XPATH, './/p')
            contents = [content.text for content in contents_raw2]
            print(contents)

            b_news['title'].append(title)
            b_news['date'].append(date)
            b_news['content'].append(' '.join(contents))
            
        break

    return b_news