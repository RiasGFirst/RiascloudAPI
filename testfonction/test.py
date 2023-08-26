import requests



if __name__ == '__main__':
    print(requests.get("http://127.0.0.1:5000/reddit/get/hentai", cookies={"api_key": "3e27b0a7-3789-4e29-b9b0-b628c0ac8753", "client_id": "5eea3f38"}).json())
    print(requests.get("http://127.0.0.1:5000/reddit/get/hentai", cookies={"api_key": "e6db2046-01c6-4cb7-8703-6103767267e9", "client_id": "361cdbe0"}).json())