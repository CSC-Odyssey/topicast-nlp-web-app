from flask import Flask, request, jsonify
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By

import pandas as pd

from initiate_lda import initiate_topic_modelling

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
    selectedDate = request.json['selectedDate']
    parsed_date = datetime.strptime(selectedDate, "%m/%d/%Y").strftime("%Y-%m-%d")

    website_str = ""

    print("Running")
    return jsonify({'message': "none"})

    # if (midlandbox and baguionews):
    #     website_str = "both"
    # elif midlandbox:
    #     website_str = "baguio_mc"
    # elif baguionews:
    #     website_str = "baguio_news"
    # else:
    #     website_str = "none"

    # results = initiate_topic_modelling(parsed_date, website_str)

    # if results:
    #     return jsonify(results)
    # else:
    #     return jsonify({'message': "none"})
    


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True, passthrough_errors=True, use_debugger=False, use_reloader=False)
