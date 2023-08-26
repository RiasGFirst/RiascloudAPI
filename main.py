from flask import Flask, render_template, request ,redirect, url_for, flash
from blueprints.redditBlueprint import redditBlueprint
from utils.mailUtils import Mail
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
app.register_blueprint(redditBlueprint, url_prefix="/reddit")

@app.route("/")
def home():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)