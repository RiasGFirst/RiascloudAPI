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
        images_lenght = gm.find('div', id='gdd').find_all('tr')[-2].find_all('td')[1].text.replace(' pages', '')


        # Get class gtb
        gtb = soup.find('div', class_='gtb')
        # Get number of pages
        pages = gtb.find('table', class_='ptt')
        pages = pages.find_all('td')[-2].text
        print(f"Title: {title}, Pages: {pages}, Images: {images_lenght}")
        return title, pages, images_lenght

    else:
        print(f'Error: {response.status_code}')
        return None, None, None


def get_gallery_images(url, pages):
    images = []
    for lenght in range(int(pages)):
        print(f'Page: {lenght}')
        response = request(f'{url}?p={lenght}')
        if response.ok:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Get class gdt
            gdt = soup.find('div', id='gdt')
            # Get images
            for a in gdt.find_all('a'):
                images.append(a['href'])

        else:
            print(f'Error: {response.status_code}')

    return images


def download_images(urls, path_to_save):
    for url in urls:
        response = request(url)
        if response.ok:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Get image
            img = soup.find('img', id='img')
            image_src = img['src']
            name = image_src.split('/')[-1]
            print(name)

        else:
            print(f'Error: {response.status_code}')

    """
    response = request(images_src)
    if response.ok:
        with open(f'images/{index}.jpg', 'wb') as file:
            file.write(response.content)
    else:
        print(f'Error: {response.status_code}')
"""


def main(url, path_to_save):
    title, pages, images_lenght = get_gallery_info(url)
    images_url = get_gallery_images(url, pages)
    download_images(images_url, path_to_save)



if __name__ == '__main__':

    #https://e-hentai.org/g/2970144/f48985d980/
    title, pages, images_lenght = get_gallery_info('https://e-hentai.org/g/2970144/f48985d980/')
    images_url = get_gallery_images('https://e-hentai.org/g/2970144/f48985d980/', pages)
    download_images(images_url)

    #https://e-hentai.org/g/2974549/09feea297e/
    #title, pages, images_lenght = get_gallery_info('https://e-hentai.org/g/2974549/09feea297e/')
    #get_gallery_images('https://e-hentai.org/g/2974549/09feea297e/', pages, images_lenght)

    #https://e-hentai.org/g/2974531/3d4b597549/
    #get_gallery_info('https://e-hentai.org/g/2974531/3d4b597549/')
