from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
import time
import os

#Load Env Variable
load_dotenv()
reddit_url = os.getenv("REDDIT_URL")
reddit_username = os.getenv("REDDIT_USERNAME")
reddit_password = os.getenv("REDDIT_PASSWORD")
reddit_verify = os.getenv("REDDIT_CONNECTED")

#div._3dLmvT0hpACHFxhncqzCOr


def loginReddit():
    with sync_playwright() as p:
        reddit_session_cookie = None
        connected = None

        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f'{reddit_url}/login')
        page.fill('input#loginUsername', reddit_username)
        page.fill('input#loginPassword', reddit_password)
        page.click('button[type=submit]')
        time.sleep(5)
        if page.is_visible("div._1m0iFpls1wkPZJVo38-LSh"):
            page.click('button[aria-label=Close]')
        cookies = page.context.cookies()

        for cookie in cookies:
            if cookie['name'] == 'reddit_session':
                reddit_session_cookie = cookie['value']
                break
        headers = {
            "User-Agent": "Mozilla/5.0",
            'Cookie': f'reddit_session={reddit_session_cookie}'
        }
        response = requests.get(f'{reddit_url}/settings', headers=headers)
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


connected, reddit_session_cookie = loginReddit()
print(connected)