from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def index():
    return request.remote_addr
