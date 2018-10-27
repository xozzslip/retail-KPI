from flask import Flask, request
app = Flask(__name__)

@app.route("/", methods=('POST', 'GET'))
def hello():
    if request.method == 'GET':
        return "OK!"
    else:
        