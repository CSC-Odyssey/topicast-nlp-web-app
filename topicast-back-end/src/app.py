from flask import Flask, request, jsonify

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
