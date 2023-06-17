import hashlib
import hmac
import json
from datetime import datetime
from urllib.parse import quote, unquote, urlencode

import requests


class PureApi:
    BASE_URL = 'https://pure-api.soulplatform.com'
    BASE_HEADERS = {
        'authority': 'pure-api.soulplatform.com',
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'origin': 'https://pure.app',
        'referer': 'https://pure.app/',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'x-js-user-agent': 'PureFTP/2.3.0 (JS 1.0; Linux 64-bit Linux x86_64 Chrome 113.0.0.0; ru-RU) SoulSDK/0.22.0 (JS)'
    }

    def __init__(self, user_id: str, session_token: str) -> None:
        self.user_id = user_id
        self.session_token = session_token

    def get_next(self, start_at: datetime, page: int) -> dict:
        start_at = to_timestamp(start_at)
        return self.get_feed(
            params=dict(sorted({
                'city_id': 524901,
                'have_photo': 'true',
                'in_pair': 'false',
                'is_around_city': 'true',
                'lang': 'ru',
                'looking_for': 'f,n',
                'ordering': '-is_online, -created_at',
                'page': page,
                'sexuality': 'h,b,q',
                'start_at': start_at,
                'temptations': 21,
            }.items(), key=lambda x: x[0])),
        )

    def get_new(self, start_at: datetime, end_at: datetime) -> dict:
        start_at = to_timestamp(start_at)
        end_at = to_timestamp(end_at)
        return self.get_feed(
            params=dict(sorted({
                'city_id': 524901,
                'end_at': end_at,
                'have_photo': 'true',
                'in_pair': 'false',
                'is_around_city': 'true',
                'lang': 'ru',
                'looking_for': 'f,n',
                'only_new': 'true',
                'sexuality': 'h,b,q',
                'start_at': start_at,
                'temptations': 21,
            }.items(), key=lambda x: x[0])),
        )

    def get_feed(self, params: dict) -> dict:
        query = urlencode(params)
        path = f'/search/feed/?{query}'
        authorization = self.calculate_authorization_hash(
            'get',
            path,
        )
        headers = {
            **self.BASE_HEADERS,
            'authorization': authorization,
        }
        resp = requests.get(f'{self.BASE_URL}{path}', headers=headers)
        return resp.json()

    def set_like(self, user_id: str) -> None:
        path = f'/users/{user_id}/reactions/sent/likes'
        data = {
            'value': 'liked',
            'createdTime': to_timestamp(datetime.now()),
        }
        authorization = self.calculate_authorization_hash(
            'post',
            path,
            json.dumps(data),
        )
        headers = {
            **self.BASE_HEADERS,
            'authorization': authorization,
        }
        resp = requests.post(f'{self.BASE_URL}{path}', headers=headers, json=data)
        try:
            data = resp.json()
        except Exception:
            print(resp.text)
            raise
        assert 'user' in data

    def calculate_authorization_hash(self, method: str, path: str, data: str = '') -> str:
        server_time = get_server_time()
        data = unquote(quote(data))
        msg = f'{method.upper()}+{path}+{data}+{server_time}'
        secure = hmac.new(
            key=bytes(self.session_token, 'utf-8'),
            msg=bytes(msg, 'utf-8'),
            digestmod=hashlib.sha256,
        ).hexdigest()
        return f'hmac {self.user_id}:{server_time}:{secure}'


def get_server_time(delta_time=0) -> float:
    return to_timestamp(datetime.now()) + delta_time


def to_timestamp(value: datetime) -> float:
    return float('{:.3f}'.format(value.timestamp()))
