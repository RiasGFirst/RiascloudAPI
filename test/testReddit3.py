from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from pprint import pprint
import requests
import json
import time
import os

#Load Env Variable
load_dotenv()
reddit_username = os.getenv("REDDIT_USERNAME")
reddit_password = os.getenv("REDDIT_PASSWORD")
reddit_verify = os.getenv("REDDIT_CONNECTED")
subredditDB_file = '../db/subreddit.json'


#div._3dLmvT0hpACHFxhncqzCOr


def loginReddit():
    print("Login Reddit")
    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)
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


def createJSONBD(file_path):
    # verify if file exist
    if os.path.isfile(file_path):
        print("File Exist")
    else:
        with open(file_path, 'w') as f:
            f.write('{"subreddit": {}}')
            f.close()
        print("File created")


def whatIsBeforeId(subreddit, file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
        if data['subreddit'][subreddit]:
            before_id = data['subreddit'][subreddit]['before_id']
            return before_id
        else:
            return None


def addBeforeId(subreddit, before_id, file_path):
    with open(file_path, 'r') as f:
        data = json.loads(f.read())
        # verify if subreddit exist in the file
        if subreddit in data['subreddit']:
            data['subreddit'][subreddit]['before_id'] = before_id
            with open(file_path, 'w') as fe:
                json.dump(data, fe, indent=4)
                return "Before ID Updated"
        else:
            # add new subreddit
            data['subreddit'][subreddit] = {"before_id": before_id}
            with open(file_path, 'w') as fw:
                json.dump(data, fw, indent=4)
                return "New Subreddit Added"


def getSubReddit(subreddit, reddit_session_cookie):
    url_template = "https://www.reddit.com/r/{}/new.json?t=all{}"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Cookie": f"reddit_session={reddit_session_cookie}"
    }
    params = '&limit=5'

    url = url_template.format(subreddit, params)
    response = requests.get(url=url, headers=headers)

    if response.ok:
        before_id = whatIsBeforeId(subreddit=subreddit, file_path=subredditDB_file)
        data = response.json()['data']
        new_before = data['children'][0]['data']['name']
        print(new_before)
        if before_id == new_before:
            print("No New Posts")

        for post in data['children']:
            pdata = post['data']
            post_name = pdata['name']

            if post_name == before_id:
                addBeforeId(subreddit=subreddit, before_id=new_before, file_path=subredditDB_file)
                print("Set New Before")
                break
            else:
                post_id = pdata['id']
                post_title = pdata['title']
                post_author = pdata['author']
                post_date = pdata['created_utc']
                post_url = pdata.get('url_overridden_by_dest')
                print(post_id, post_title, post_author, post_date, post_url)
        return print(addBeforeId(subreddit=subreddit, before_id=new_before, file_path=subredditDB_file))

    else:
        print("Subreddit Connection Failed")
        return None


def main():

    #connected, reddit_session_cookie = loginReddit()
    #print(f"Status: {connected}")
    #print(f"Cookie: {reddit_session_cookie}")
    #print("=====================================")
    reddit_session_cookie = ""
    try:
        print("SubredditDB File:")
        createJSONBD(file_path=subredditDB_file)
        print("cosplay Subreddit:")
        getSubReddit(subreddit='cosplay', reddit_session_cookie=reddit_session_cookie)
        print('hentai Subreddit:')
        getSubReddit(subreddit='hentai', reddit_session_cookie=reddit_session_cookie)
    except KeyboardInterrupt:
        print('Exiting...')


if __name__ == '__main__':
    main()