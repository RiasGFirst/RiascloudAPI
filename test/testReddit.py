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

        browser = p.chromium.launch(headless=False)
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
        page.mouse.wheel(0, 10000000000000)
        time.sleep(20)

        #_1oQyIsiPHYt6nx7VOmd1sz _1RYN-7H8gYctjOQeL8p2Q7
        html = page.inner_html('div.rpBJOHq2PR60pnwJlUyP0')
        soup = BeautifulSoup(html, 'html.parser')

        posts = soup.find_all('div', {'class': '_1oQyIsiPHYt6nx7VOmd1sz'})
        posts.pop(0)

        for post in posts:

            # Récupérer l'ID du post
            post_id = post.find('div', {'class': '_1oQyIsiPHYt6nx7VOmd1sz'})
            print("post_id: ", post_id)

            # Récupérer l'auteur
            author = post.find('a', {'class': '_2tbHP6ZydRpjI44J3syuqC'}).text
            print("author: ", author)

            # Récupérer le titre
            title = post.find('h3', class_='_eYtD2XCVieq6emjKBH3m').text
            print("title: ", title)

            # Récupérer l'image ou la vidéo
            div = post.find('div', {'class': '_3JgI-GOrkmyIeDeyzXdyUD _2CSlKHjH7lsjx0IpjORx14'})
            print("div: ", div)
            if div is not None:
                # search for image
                image_url = div.find('img', {'class': '_35oEP5zLnhKEbj5BlkTBUA'})
                print("image_url: ", image_url)
                # search for video if image not found
                if image_url is None:
                    video_url = div.find('source')
                    if video_url is not None:
                        video_url = video_url['src']
                        print("video_url: ", video_url)
            print("=====================================")

        page.close()
        browser.close()


if __name__ == '__main__':
    status, cookies, cookiesJSON = loginReddit()
    print(status)
    getSubReddit(cookies, 'cosplay')