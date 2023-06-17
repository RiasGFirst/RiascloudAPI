from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from pprint import pprint
import requests
import sqlite3
import time
import os

#Load Env Variable
load_dotenv()
reddit_username = os.getenv("REDDIT_USERNAME")
reddit_password = os.getenv("REDDIT_PASSWORD")
reddit_verify = os.getenv("REDDIT_CONNECTED")

#div._3dLmvT0hpACHFxhncqzCOr


def loginReddit():
    with sync_playwright() as p:

        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('https://www.reddit.com/login')
        page.fill('input#loginUsername', reddit_username)
        page.fill('input#loginPassword', reddit_password)
        page.click('button[type=submit]')
        time.sleep(20)
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


def createTable(conn):
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subreddit TEXT NOT NULL,
            before TEXT
        )
    ''')
    conn.commit()


def subredditExists(conn, subreddit):
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM stats WHERE subreddit = ?", (subreddit,))
    count = c.fetchone()[0]
    return count > 0


def insertStats(conn, subreddit, before):
    c = conn.cursor()
    c.execute('''
            INSERT INTO stats (subreddit, before) VALUES (?, ?)
        ''', (subreddit, before))
    conn.commit()


def updateBefore(conn, subreddit, new_before):
    c = conn.cursor()

    c.execute('''
        UPDATE stats
        SET before = ?
        WHERE subreddit = ?
    ''', (new_before, subreddit))

    conn.commit()


def getSubReddit(subreddit, reddit_session_cookie, before_id=None, conn=None):
    if subredditExists(conn, subreddit) is False:
        insertStats(conn, subreddit, before_id)

    url_template = "https://www.reddit.com/r/{}/new.json?t=all{}"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Cookie": f"reddit_session={reddit_session_cookie}"
    }
    params = '&limit=5'

    url = url_template.format(subreddit, params)
    response = requests.get(url=url, headers=headers)

    if response.ok:
        data = response.json()['data']

        new_before = data['children'][0]['data']['name']
        print(new_before)
        if before_id == new_before:
            updateBefore(conn, subreddit, new_before)
            print("No New Posts")

        for post in data['children']:
            pdata = post['data']
            post_name = pdata['name']

            if post_name == before_id:
                updateBefore(conn, subreddit, new_before)
                print("Set New Before")
                break
            else:
                post_id = pdata['id']
                post_title = pdata['title']
                post_author = pdata['author']
                post_date = pdata['created_utc']
                post_url = pdata.get('url_overridden_by_dest')
                print(post_id, post_title, post_author, post_date, post_url)

    else:
        print("Subreddit Connection Failed")
        return None


def main():
    connected, reddit_session_cookie = loginReddit()
    print(f"Status: {connected}")
    print(f"Cookie: {reddit_session_cookie}")
    print("=====================================")
    print("cosplay Subreddit:")
    conn = sqlite3.connect('./db/reddit-subreddit.db')
    createTable(conn)
    try:
        getSubReddit(subreddit='cosplay', reddit_session_cookie=reddit_session_cookie, conn=conn)
    except KeyboardInterrupt:
        print('Exiting...')
    finally:
        conn.close()


if __name__ == '__main__':
    main()