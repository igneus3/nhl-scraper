import requests
from time import sleep

def http_request(url):
    result = None

    # Tying to play nice
    sleep(.500)
    response = requests.get(url)
    if response.status_code == 200:
        result = response.json()

    return result
