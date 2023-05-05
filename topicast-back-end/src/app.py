from flask import Flask, request, jsonify

from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

from baguio_mc import scrape_bmc_news
from baguio_news import scrape_baguio_news
from lda import initiate_topic_modelling

compiled_data = {
    "title": [],
    "date": [],
    "content": []
}



app = Flask(__name__)

@app.route("/api/hello")
def handle_form_submission():
    # checkbox1 = request.form.get("checkbox1")
    # checkbox2 = request.form.get("checkbox2")
    # checkbox3 = request.form.get("checkbox3")
    # Do something with the form data here...
    return {"message": ["??", "???"]}


@app.route("/api/retrieve_topics", methods=["POST"])
def handle_retrieve_topics():
    midlandbox = request.json['checkbox1']
    baguionews = request.json['checkbox2']

    if (midlandbox and baguionews):
        return jsonify({'message': ["midlandbox", "baguionews"]})
    elif midlandbox:
        return jsonify({'message': "midlandbox"})
    elif baguionews:
        return jsonify({'message': "baguionews"})
    else:
        return jsonify({'message': "none"})


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
