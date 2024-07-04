import requests
from requests.auth import HTTPProxyAuth

# Liste des proxys avec leurs adresses IPv6 et ports
PROXIES = []

# URL de test pour vérifier le proxy
TEST_URL = "https://httpbin.org/ip"


def check_proxy(proxy):
    try:
        response = requests.get(TEST_URL, proxies={"https": proxy})
        if response.status_code == 200:
            print(f"Proxy {proxy} fonctionne correctement.")
        else:
            print(f"Proxy {proxy} a renvoyé un code de statut {response.status_code}.")
    except requests.exceptions.RequestException as e:
        print(f"Proxy {proxy} a échoué. Erreur: {e}")


def main():
    for proxy in PROXIES:
        check_proxy(proxy)


if __name__ == "__main__":
    main()
