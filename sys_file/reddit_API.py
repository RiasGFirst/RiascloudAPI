from playwright.sync_api import sync_playwright
from utils.DbUtils import DataBase
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
import time
import json
import os


class Reddit:

    def __init__(self):
        load_dotenv()
        self.reddit_username = os.getenv("REDDIT_USERNAME")
        self.reddit_password = os.getenv("REDDIT_PASSWORD")
        self.reddit_verify = os.getenv("REDDIT_CONNECTED")

    # Login Modules
    def loginReddit(self, isHeadless):
        with sync_playwright() as p:

            browser = p.chromium.launch(headless=isHeadless)
            page = browser.new_page()
            page.goto('https://www.reddit.com/login')
            page.fill('input#loginUsername', self.reddit_username)
            page.fill('input#loginPassword', self.reddit_password)
            page.click('button[type=submit]')
            time.sleep(20)
            if isHeadless is False:
                if page.is_visible("div._1m0iFpls1wkPZJVo38-LSh"):
                    page.click('button[aria-label=Close]')
            cookies = page.context.cookies()

            for cookie in cookies:
                if cookie['name'] == 'reddit_session':
                    reddit_session_cookie = cookie['value']
            page.close()

            headers = {
                "User-Agent": "Mozilla/5.0",
                "Cookie": f"reddit_session={reddit_session_cookie}"
            }

            response = requests.get('https://www.reddit.com/settings', headers=headers)

            if response.ok:
                soup = BeautifulSoup(response.text, 'html.parser')
                verify_connected = soup.find('p', {'class': '_2nyJGeaFJbXTqTh9OGwxfu _1NdK7EwgYqUxJObBr3ym4o'})
                if verify_connected is not None and verify_connected.text == self.reddit_verify:
                    self.reddit_cookie = reddit_session_cookie
                    connected = "Login Successful"
                    return connected, reddit_session_cookie
                else:
                    connected = "Login Failed No Reddit_Session Cookies"
                    return connected, reddit_session_cookie
            else:
                connected = "Login Failed No Status Code 200"
                return connected, reddit_session_cookie

    def loginRedditWithCookie(self, reddit_session_cookie):
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Cookie": f"reddit_session={reddit_session_cookie}"
        }

        response = requests.get('https://www.reddit.com/settings', headers=headers)

        if response.ok:
            soup = BeautifulSoup(response.text, 'html.parser')
            verify_connected = soup.find('p', {'class': '_2nyJGeaFJbXTqTh9OGwxfu _1NdK7EwgYqUxJObBr3ym4o'})
            if verify_connected is not None and verify_connected.text == self.reddit_verify:
                connected = "Login Successful"
                return connected, reddit_session_cookie
            else:
                connected = "Login Failed No Reddit_Session Cookies"
                return connected, reddit_session_cookie
        else:
            connected = "Login Failed No Status Code 200"
            return connected, reddit_session_cookie

    # Subreddit Modules
    # Verify Subreddit in table
    def verifySubreddit(self, subreddit, reddit_session_cookie):
        if not DataBase().verifySubreddit(subreddit=subreddit):
            jsonToReturn = {}
            headers = {
                "User-Agent": "Mozilla/5.0",
                "Cookie": f"reddit_session={reddit_session_cookie}"
            }
            url_template = "https://www.reddit.com/r/{}/new.json?t=all{}"
            params = '&limit=5'

            url = url_template.format(subreddit, params)
            print(url)
            response = requests.get(url=url, headers=headers)

            if response.ok:
                DataBase().addSubreddit(subreddit=subreddit)
                return "Subreddit Added"
            else:
                return "Subreddit not Added"

            #DataBase().addSubreddit(subreddit=subreddit)
            return "Subreddit Added"

    def getSubreddit(self, subreddit, user_id, token_id, reddit_session_cookie, before_id=None):

        jsonPost = []
        jsonToReturn = {}
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Cookie": f"reddit_session={reddit_session_cookie}"
        }
        url_template = "https://www.reddit.com/r/{}/new.json?t=all{}"
        params = '&limit=5'

        url = url_template.format(subreddit, params)
        response = requests.get(url=url, headers=headers)

        if response.ok:

            data = response.json()['data']
            new_before = data['children'][0]['data']['name']

            DBSubredditData = DataBase().getUserSubreddit(user_id=user_id, token_id=token_id, subreddit=subreddit)
            if DBSubredditData is not None:
                before_id = DBSubredditData[3]
            else:
                DataBase().addUserSubreddit(user_id=user_id, token_id=token_id, subreddit=subreddit, before_id=new_before)
                #print("Subreddit Created")

            #print(f"New Before ID: {new_before}")
            if before_id == new_before:
                # print("No New Posts")
                return json.dumps({"Subreddit": {"name": subreddit, "posts": "No New Posts"}})

            for post in data['children']:
                pdata = post['data']
                post_name = pdata['name']

                if post_name == before_id:
                    DataBase().addUserSubreddit(user_id=user_id, token_id=token_id, subreddit=subreddit, before_id=new_before)
                    break
                else:
                    post_id = pdata['id']
                    post_title = pdata['title']
                    post_author = pdata['author']
                    post_date = pdata['created_utc']
                    post_image_url = pdata.get('url_overridden_by_dest')
                    post_json = {
                        "post_id": post_id,
                        "post_title": post_title,
                        "post_author": post_author,
                        "post_date": post_date,
                        "post_image_url": post_image_url
                    }
                    jsonPost.append(post_json)
                    #print(f"Post ID:{post_id}, Post Title: {post_title}, Post Author: {post_author}, Post Date: {post_date}, Post Image URL: {post_image_url}")
                    jsonToReturn = {
                        "name": subreddit,
                        "posts": jsonPost
                    }
            return json.dumps({"Subreddit": jsonToReturn})
        else:
            return print("Subreddit Connection Failed")