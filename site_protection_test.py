import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time

MAX_ITER = 100 # Количество запросов к странице
header = {'user-agent': 'Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/29.0'}

url = 'https://www.tss.ru/catalog/dvigateli/benzinovye_dvigateli_tss/dvigatel_benzinovyy_tss_excalibur_s420_t0_val_konusnyy_26_47_8_taper_023839/'



def random_user_agent() -> dict:
    return {'user-agent': UserAgent(verify_ssl=False).random}

def simple_check(max_iter: int):
    i = 0
    while i < max_iter:
        response = requests.get(url, headers=header)
        print(response.status_code)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            print(soup.title.get_text())
            i += 1
        else:
            break

def check_with_cookie(max_iter: int):
    cookie = requests.Session()
    i = 0
    while i < max_iter:
        print(random_user_agent())
        response = cookie.get(url, headers=random_user_agent())
        print(response.status_code)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            print(soup.title.get_text())
            i += 1
        else:
            break
        # time.sleep(3)


if __name__ == '__main__':
    # simple_check(MAX_ITER)
    check_with_cookie(MAX_ITER)