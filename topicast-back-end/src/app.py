from flask import Flask, request, jsonify

from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

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


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
