from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
from queue import Queue

bmc_news = {'title': [], 'date': [], 'content': []}

def scrape_article(driver):
    title = ''
    date = ''
    content =''

    try:
        title = driver.find_element(By.CLASS_NAME, "entry-title").text
        date = driver.find_element(By.CLASS_NAME, "entry-meta").text
        try:
            content = driver.find_element(By.CLASS_NAME, 'wp-element-caption').text # For captions
        except NoSuchElementException:
            pass
        contents = driver.find_elements(By.TAG_NAME, 'p') # For p elements

        for c in contents:
                content = content + " " + c.text

    except NoSuchElementException:
        print("error")

    if len(title) == 0 or len(date) == 0  or len(content) == 0 :
        print("error")
        pass
    else:
        bmc_news['title'].append(title)
        bmc_news['date'].append(date)
        bmc_news['content'].append(content)

    return bmc_news


def scrape_bmc_news(date, return_dict):
    options = webdriver.ChromeOptions()

    url = 'https://www.baguiomidlandcourier.com.ph/'
    driver = webdriver.Chrome(options = options)
    driver.get(url)

    news_link = driver.find_element(By.CSS_SELECTOR, '.read-img.pos-rel.read-bg-img')
    next = news_link.find_element(By.TAG_NAME, 'a')
    newl = next.get_attribute('href')

    driver.implicitly_wait(10)
    driver.get(newl)

    news_date = driver.find_element(By.CLASS_NAME, 'entry-meta').text
    current_article_date = datetime.strptime(news_date, "%B %d, %Y").date()
    print(current_article_date)
    input_date = datetime.strptime(date, "%Y-%m-%d").date()
    print(input_date)

    while True:
        if current_article_date == input_date:
            # scrape article
            bmc_news = scrape_article(driver)
            
            # go to previous article
            while current_article_date == input_date:
                try:
                    link = driver.find_element(By.CLASS_NAME, 'nav-previous')
                    next = link.find_element(By.TAG_NAME, 'a')
                    newl = next.get_attribute('href')

                    driver.get(newl)
                    driver.implicitly_wait(10)

                    bmc_news = scrape_article(driver)

                    news_date = driver.find_element(By.CLASS_NAME, 'entry-meta').text
                    current_article_date = datetime.strptime(news_date, "%B %d, %Y").date()
                except NoSuchElementException:
                    break
            break;

            try:
                link = driver.find_element(By.CLASS_NAME, 'nav-previous')
                next = link.find_element(By.TAG_NAME, 'a')
                newl = next.get_attribute('href')

                driver.implicitly_wait(10)
                driver.get(newl)
                driver.implicitly_wait(10)

                news_date = driver.find_element(By.CLASS_NAME, 'entry-meta').text
                current_article_date = datetime.strptime(news_date, "%B %d, %Y").date()
            except NoSuchElementException:
                break

        elif current_article_date > input_date:
            # go to previous page
            try:
                link = driver.find_element(By.CLASS_NAME, 'nav-previous')
                next = link.find_element(By.TAG_NAME, 'a')
                newl = next.get_attribute('href')

                driver.get(newl)
                driver.implicitly_wait(10)

                news_date = driver.find_element(By.CLASS_NAME, 'entry-meta').text
                current_article_date = datetime.strptime(news_date, "%B %d, %Y").date()
            except NoSuchElementException:
                break

        else:
            # go to next page
            try:
                link = driver.find_element(By.CLASS_NAME, 'nav-next')
                next = link.find_element(By.TAG_NAME, 'a')
                newl = next.get_attribute('href')

                driver.get(newl)
                driver.implicitly_wait(10)

                news_date = driver.find_element(By.CLASS_NAME, 'entry-meta').text
                current_article_date = datetime.strptime(news_date, "%B %d, %Y").date()
            except NoSuchElementException:
                break
     
    driver.close()
    # return bmc_news
    return_dict["baguio_mc"] = bmc_news



if __name__ == "__main__":
    param = sys.argv[1]
    result = scrape_bmc_news(param)