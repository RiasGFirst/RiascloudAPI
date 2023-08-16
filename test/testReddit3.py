from playwright.sync_api import sync_playwright
from utils.DbUtils import DataBase
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
import time
import os

#Load Env Variable
load_dotenv()
reddit_username = os.getenv("REDDIT_USERNAME")
reddit_password = os.getenv("REDDIT_PASSWORD")
reddit_verify = os.getenv("REDDIT_CONNECTED")


#div._3dLmvT0hpACHFxhncqzCOr


def loginReddit(isHeadless):
    print("Login Reddit")
    with sync_playwright() as p:

        browser = p.chromium.launch(headless=isHeadless)
        page = browser.new_page()
        page.goto('https://www.reddit.com/login')
        page.fill('input#loginUsername', reddit_username)
        page.fill('input#loginPassword', reddit_password)
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


def getSubReddit(subreddit, reddit_session_cookie, before_id=None):
    url_template = "https://www.reddit.com/r/{}/new.json?t=all{}"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Cookie": f"reddit_session={reddit_session_cookie}"
    }
    params = ''

    url = url_template.format(subreddit, params)
    response = requests.get(url=url, headers=headers)

    if response.ok:
        data = response.json()['data']
        new_before = data['children'][0]['data']['name']

        if DataBase().verifySubreddit(subreddit=subreddit):
            before_id = DataBase().getBeforeId(subreddit=subreddit)
            print(f"Before ID: {before_id}")
        else:
            DataBase().addSubreddit(subreddit=subreddit, before_id=new_before)
            print("Subreddit Created")

        print(f"New Before ID: {new_before}")
        if before_id == new_before:
            print("No New Posts")

        for post in data['children']:
            pdata = post['data']
            post_name = pdata['name']

            if post_name == before_id:
                DataBase().updateSubreddit(subreddit=subreddit, before_id=new_before)
                break
            else:
                post_id = pdata['id']
                post_title = pdata['title']
                post_author = pdata['author']
                post_date = pdata['created_utc']
                post_url = pdata.get('url_overridden_by_dest')
                print(post_id, post_title, post_author, post_date, post_url)
        return print("Subreddit Connection Successful")

    else:
        print("Subreddit Connection Failed")
        return None


def main():
    DataBase()
    connected, reddit_session_cookie = loginReddit(isHeadless=False)
    print(f"Status: {connected}")
    print(f"Cookie: {reddit_session_cookie}")
    print("=====================================")
    """
    try:
        print("cosplay Subreddit:")
        before_id = DataBase().getBeforeId(subreddit='cosplay')
        getSubReddit(subreddit='cosplay', reddit_session_cookie=reddit_session_cookie, before_id=before_id)
        print('hentai Subreddit:')
        before_id = DataBase().getBeforeId(subreddit='hentai')
        getSubReddit(subreddit='hentai', reddit_session_cookie=reddit_session_cookie, before_id=before_id)
    except KeyboardInterrupt:
        print('Exiting...')
    """


if __name__ == '__main__':
    main()