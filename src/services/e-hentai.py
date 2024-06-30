from bs4 import BeautifulSoup
import requests
import json
import re


def request(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    return requests.get(url, headers=headers)


#https://e-hentai.org/g/2970144/f48985d980/
def get_gallery_info(url):
    response = request(url)
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get class gm
        gm = soup.find_all('div', class_='gm')[0]
        
        # Get title
        title = gm.find('h1', id='gn').text
        print(title)
        
    else:
        print(f'Error: {response.status_code}')


if __name__ == '__main__':
    get_gallery_info('https://e-hentai.org/g/2970144/f48985d980/')
