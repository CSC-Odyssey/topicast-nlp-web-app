from flask import Flask, request, jsonify

from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

compiled_data = {
    "title": [],
    "date": [],
    "content": []
}


def scrape_sunstar(date):

    articles = driver.find_elements(By.CLASS_NAME, 'col-md-3')
    list_articles = []
    for article in articles:
        title = article.find_element(By.CLASS_NAME, 'article-title').text
        link = article.find_element(By.TAG_NAME, 'a')
        date = article.find_element(By.CLASS_NAME, 'article-date').text
    
        newl = link.get_attribute('href')
    
        driver.implicitly_wait(10)
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(newl)
        driver.implicitly_wait(10)
    
        content = driver.find_element(By.CLASS_NAME, 'article-body').text
    
        per_article = {
            'title': title,
            'date': date,
            'content': content
        }
    
        list_articles.append(per_article)
        df = pd.DataFrame(list_articles)
    
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    return None


app = Flask(__name__)

@app.route("/api/hello")
def handle_form_submission():
    # checkbox1 = request.form.get("checkbox1")
    # checkbox2 = request.form.get("checkbox2")
    # checkbox3 = request.form.get("checkbox3")
    # Do something with the form data here...
    return {"message": ["??", "???"]}


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
