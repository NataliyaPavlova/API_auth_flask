from datetime import datetime, timedelta
from typing import Dict

import jwt
from src.settings import Settings
from src.storages.tokens import redis_client

settings = Settings()


class Token:

    def __init__(self, token, is_access=False, is_refresh=False):
        self.token = token.encode()
        self.is_access = is_access
        self.is_refresh = is_refresh
        self.ttl = settings.access_ttl if self.is_access else settings.refresh_ttl

    @property
    def is_expired(self) -> bool:
        try:
            data = jwt.decode(self.token, settings.app_secret.encode(),
                              algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return True
        return False

    @property
    def is_valid(self) -> bool:
        if self.is_expired:
            return False
        if self.is_refresh:
            if not self.get_payload():
                return False
            key = f"{self.get_payload()['user_id']}_save_used_refresh"
            val = redis_client.get(key)
            if val:
                return False
        return True

    def get_payload(self) -> Dict | None:
        if self.is_expired:
            return None
        data = jwt.decode(self.token, settings.app_secret.encode(),
                          algorithms=['HS256'])
        return data

    def new(self, data=None, ts_from=datetime.utcnow(),
            period_mins=None) -> None:
        data = data if data else self.get_payload()
        if not data:
            return None
        minutes = period_mins if period_mins else self.ttl
        new_token = jwt.encode({
            'user_id': data['user_id'],
            'is_administrator': data.get['is_administrator'],
            'exp': ts_from + timedelta(minutes=minutes)
        }, settings.app_secret.encode(), algorithm='HS256')
        self.token = new_token

    def save(self) -> None:
        data = self.get_payload()
        if data:
            key = f"{data['user_id']}_save_used_refresh"
            redis_client.set(key=key, val=self.token,
                             ttl=settings.invalid_tokens_ttl)

    def prolong(self, period=60) -> None:
        data = self.get_payload()
        if not data:
            return None
        self.new(ts_from=data['exp'], period_mins=period)

    def get_user_id(self) -> str:
        payload = self.get_payload()
        return payload['user_id']
