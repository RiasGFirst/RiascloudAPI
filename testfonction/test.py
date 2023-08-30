import requests



if __name__ == '__main__':
    print(requests.get("http://127.0.0.1:5000/reddit/get/@", cookies={"api_key": "", "client_id": ""}).json())