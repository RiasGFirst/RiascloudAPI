from playwright.sync_api import sync_playwright
from utils.DbUtils import DataBase
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
import pprint
import time
import os


class Reddit:

    def __init__(self):
        load_dotenv()
        self.reddit_username = os.getenv("REDDIT_USERNAME")
        self.reddit_password = os.getenv("REDDIT_PASSWORD")
        self.reddit_verify = os.getenv("REDDIT_CONNECTED")
        self.reddit_cookie = None

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
                if verify_connected is not None and verify_connected.text == reddit_verify:
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
    def verifySubreddit(self, subreddit):
        if not DataBase().verifySubreddit(subreddit=subreddit):
            DataBase().addSubreddit(subreddit=subreddit)
            return "Subreddit Added"

    def getSubreddit(self, subreddit, user_id, token_id, reddit_session_cookie, before_id=None):
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
                print("Subreddit Created")

            print(f"New Before ID: {new_before}")
            if before_id == new_before:
                print("No New Posts")

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
                    post_url = pdata.get('url_overridden_by_dest')
                    print(f"Post ID:{post_id}, Post Title: {post_title}, Post Author: {post_author}, Post Date: {post_date}, Post URL: {post_url}")
            return print("Subreddit Connection Successful")
        else:
            return print("Subreddit Connection Failed")


def main():
    reddit = Reddit()
    #connected, reddit_session_cookie = reddit.loginReddit(isHeadless=False)
    #print(f"Status: {connected}")
    #print(f"Cookie: {reddit_session_cookie}")
    print("=====================================")
    reddit_session_cookie="37565806251051%2C2023-08-15T20%3A02%3A27%2C2b0c2d7c73a1389e5fe177103e8f48571f82fda5"
    reddit.verifySubreddit(subreddit='cosplay')
    reddit.getSubreddit(subreddit='cosplay', user_id='40328594', token_id='04ee8b23-7adb-4db7-ad65-6f0d8efff05e', reddit_session_cookie=reddit_session_cookie, before_id=None)
    print("=====================================")


if __name__ == '__main__':
    main()