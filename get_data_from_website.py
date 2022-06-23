import requests
import random
from fake_useragent import UserAgent
import os


class GetData:
    Response = requests.models.Response

    def __init__(self, url: str):
        self.url = url

    def get_html(self) -> str:
        response = self._data_request()
        if response.status_code == 200:
            return response.text

    def get_json(self) -> str:
        response = self._data_request()
        if response.status_code == 200:
            return response.json()

    def download_file(self, directory_path: str, file_name:str) -> None:
        '''
        :param directory_path: 'directory/directory_inner', 'images/2022/05/23'
        :param file_name: 'img.jpeg', 'doc.pdf', 'price.xlsx'
        '''
        file_bytes = self._data_request().content

        if not os.path.isdir(directory_path):
            os.mkdir(directory_path)

        with open(f'{directory_path}/{file_name}', 'wb') as f:
            f.write(file_bytes)

    def __get_headers_proxy(self):
        '''
        The config file must have dict:
            {
                'http_proxy':'http://user:password@ip:port',
                'user-agent': 'user_agent name'
            }
        '''

        try:
            import lib.config
            users = lib.config.USER_AGENTS_PROXY_LIST
            user = random.choice(users)
            headers = {'user-agent': user['user-agent']}
            proxy_dict = {'http': user['http_proxy']}
            persona = {
                'headers': headers,
                'proxy_dict': proxy_dict
            }
        except ImportError:
            persona = None

        return persona

    def _data_request(self) -> Response:
        user = self.__get_headers_proxy()
        if user:
            headers = {'user-agent': UserAgent(verify_ssl=False).random}
            response = requests.get(self.url, headers=headers, proxies=user['proxy_dict'], timeout=5)
        else:
            headers = {'user-agent': UserAgent(verify_ssl=False).random}
            response = requests.get(self.url, headers=headers, timeout=5)
        return response
