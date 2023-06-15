from sys_file.reddit_API import *
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from flask import Flask
import requests
import time
import json
import os


app = Flask(__name__)


@app.route("/reddit/login", methods=['GET'])
def reddit_login():
    status, session_cookie = loginReddit()
    jsonObj = {
        "status": status,
        "cookie": session_cookie
    }
    return jsonObj


if __name__ == '__main__':
    app.run(debug=True)
    print("API running...")