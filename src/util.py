from datetime import datetime
from logging import error
import requests
from time import sleep

def http_request(url):
    result = None

    # Tying to play nice
    sleep(.500)
    response = requests.get(url)
    if response.status_code == 200:
        if response.headers.get('content-type') == 'application/json':
            result = response.json()
        else:
            result = response.text

    return result

def http_request_with_retry(url, retry_attempts=3):
    result = None
    count = 0
    while (True):
        if count > 0:
            sleep(5)

        try:
           result = http_request(url)
           break;
        except Exception as e:
            count += 1

            error(f'[ERROR] {datetime.now()} {type(e).__name__} error occurred when making HTTP request. Retrying request. Retry attempt {count}/{retry_attempts}.')

            if count >= retry_attempts:
                error(f'[ERROR] {datetime.now()} All retry attempts failed.  Aborting.')
                raise e

    return result
