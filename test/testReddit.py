import requests
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
from bs4 import BeautifulSoup
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
        cookiesJSON = {}

        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f'{reddit_url}/login')
        page.fill('input#loginUsername', reddit_username)
        page.fill('input#loginPassword', reddit_password)
        page.click('button[type=submit]')
        time.sleep(20)
        if page.is_visible("div._1m0iFpls1wkPZJVo38-LSh"):
            page.click('button[aria-label=Close]')
        cookies = page.context.cookies()

        for cookie in cookies:
            name = cookie['name']
            value = cookie['value']
            cookiesJSON[name] = value
        page.close()

        headers = {
            "User-Agent": "Mozilla/5.0",
        }
        response = requests.get(f'{reddit_url}/settings', headers=headers, cookies=cookiesJSON)
        if response.ok:
            soup = BeautifulSoup(response.text, 'html.parser')
            verify_connected = soup.find('p', {'class': '_2nyJGeaFJbXTqTh9OGwxfu _1NdK7EwgYqUxJObBr3ym4o'})
            if verify_connected is not None and verify_connected.text == reddit_verify:
                connected = "Login Successful"
                return connected, cookies, cookiesJSON
            else:
                connected = "Login Failed No Reddit_Session Cookies"
                return connected, cookies, cookiesJSON
        else:
            connected = "Login Failed No Status Code 200"
            return connected, cookies, cookiesJSON


def getSubReddit(cookies, subReddit):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        browserContext = browser.new_context()
        browserContext.add_cookies(cookies)
        page = browserContext.new_page()
        page.goto(f'{reddit_url}/r/{subReddit}', )
        time.sleep(5)
        page.mouse.wheel(0, 100)

        #_1oQyIsiPHYt6nx7VOmd1sz _1RYN-7H8gYctjOQeL8p2Q7
        html = page.inner_html('div.rpBJOHq2PR60pnwJlUyP0')
        soup = BeautifulSoup(html, 'html.parser')

        posts = soup.find_all('div', {'class': '_1oQyIsiPHYt6nx7VOmd1sz'})

        for post in posts:
            print(post)
            print('----------------------------------')
        browser.close()






if __name__ == '__main__':
    status, cookies, cookiesJSON = loginReddit()
    print(status)
    getSubReddit(cookies, 'cosplay')