from typing import Dict
from typing import List

import bcrypt
from sqlalchemy.dialects.postgresql import UUID
from src.models.db_models import History
from src.models.db_models import User
from src.service.history import get_history_service
from src.service.token import Token
from src.service.user import get_user_service
from src.settings import Settings

settings = Settings()

user_service = get_user_service()
history_service = get_history_service()


class Auth:

    def __init__(self, username: str, pwd: str, **kwargs) -> None:
        self.username = username
        self.password = pwd

        for attr, value in kwargs.items():
            setattr(self, attr, value)

    def signup(self) -> UUID | None:
        if user_service.get_by(login=self.username):
            return None
        mySalt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(self.password.encode(), mySalt)

        user = user_service.create(
            login=self.username,
            password=hashed.decode(),
        )
        return user.id

    def login(self, **kwargs) -> User | None:
        user = user_service.get_by(login=self.username)
        if not user:
            return None
        if not bcrypt.checkpw(self.password.encode(), user.password.encode()):
            return None
        history_service.create(
            user=user,
            user_id=user.id,
            user_agent=self.agent
        )
        return user

    def logout(self, **kwargs) -> None:
        pass

    def get_session(self, **kwargs) -> None:
        pass

    def change(self, **kwargs) -> User | None:
        user = user_service.get_by(login=self.username)
        if not user:
            return None
        if 'login' in kwargs and kwargs['login']:
            other_user = user_service.get_by(login=kwargs['login'])
            if other_user:
                return None
            user = user_service.update(user.id, login=kwargs['login'])
        if 'pwd' in kwargs and kwargs['pwd']:
            mySalt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(kwargs['pwd'].encode(), mySalt)
            user = user_service.update(user.id, password=hashed.decode())

        return user

    def get_history(self) -> List[History] | List[None]:
        user = user_service.get_by(login=self.username)
        return user.histories


class AuthService(Auth):

    def __init__(self, username: str, pwd: str, **kwargs) -> None:
        super().__init__(username, pwd, **kwargs)
        self.a_token = Token('', is_access=True)
        self.r_token = Token('', is_refresh=True)

    def get_session(self, access_token: str, refresh_token: str) -> Dict | None:
        self.a_token.token = access_token.encode()
        self.r_token.token = refresh_token.encode()
        if not self.r_token.is_valid:
            return None
        if not self.a_token.is_valid:
            self.a_token.new()
            self.r_token.prolong()
        user_id = self.a_token.get_user_id()
        history_service.create(
            user_id=user_id,
            user_agent=self.agent
        )
        return {'Access-Token': str(self.a_token.token.decode()),
                'Refresh-Token': str(self.r_token.token.decode())}

    def login(self) -> Dict | None:
        user = super().login()
        if not user:
            return None

        data = {
            'user_id': str(user.id),
            'is_administrator': (user.login == 'administrator')
        }
        return {
            'Access-Token': self.a_token.new(data=data),
            'Refresh-Token': self.r_token.new(data=data),
        }

    def logout(self, access_token: str, refresh_token: str) -> None:
        self.a_token.token = access_token
        self.r_token.token = refresh_token
        self.r_token.save()
