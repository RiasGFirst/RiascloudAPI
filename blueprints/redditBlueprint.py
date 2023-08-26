from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from sys_file.reddit_API import Reddit
from utils.DbUtils import DataBase
from utils.mailUtils import Mail
from dotenv import load_dotenv
import os

load_dotenv()
reddit_cookie = os.getenv("REDDIT_COOKIES")


redditBlueprint = Blueprint("reddit", __name__, static_folder="static", template_folder="templates")


@redditBlueprint.route("/<msg>", methods=["GET"])
def reddit(msg=None):
    if msg is not None:
        flash(msg, "success")
    return render_template("reddithome.html")


@redditBlueprint.route("/askforaccess", methods=["POST", "GET"])
def askForAccess():
    if request.method == "POST":
        email = request.form["getemail"]
        mail = Mail(receiver_email=email)
        mail.sendMail()
        return redirect(url_for("reddit.reddit", msg="Email sent"))
    else:
        return render_template("redditAskForAccess.html")


@redditBlueprint.route("/get/<subreddit>", methods=["GET"])
def getSubreddit(subreddit):
    api_key = request.cookies.get('api_key')
    client_id = request.cookies.get('client_id')
    if api_key is None or client_id is None:
        print(f"api_key: {api_key} client_id: {client_id}")
        return "Missing api_key or client_id", 400
    else:
        db = DataBase()
        status, msg = db.verifyUser(user_id=client_id, token_id=api_key)
        if status is False:
            return "Invalid api_key or client_id", 400
        else:
            if msg is None:
                return "You don't have any token", 400
            else:
                reddit = Reddit()
                reddit.verifySubreddit(subreddit=subreddit)
                json = reddit.getSubreddit(subreddit=subreddit, user_id=client_id, token_id=api_key, reddit_session_cookie=reddit_cookie)
                return jsonify(json), 200