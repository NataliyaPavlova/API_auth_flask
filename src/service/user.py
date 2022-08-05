from src.models.db_models import Base
from src.models.db_models import User
from src.service.base import BaseService
from src.storages.db_connect import db

from src.models.db_models import Role


class UserService(BaseService):
    COLUMN_LIST = (
        User.id,
        User.login,
        User.password,
        User.created,
        User.modified,
        User.role_id,
        Role.title.label('role_title'),
    )

    def get(self, _id: str) -> type[Base] | None:
        user = self.session.query(
            *self.COLUMN_LIST
        ).join(Role).filter(User.id == _id).first()
        return user

    def filter_by(self, **kwargs) -> list[type[Base]] | list[None]:
        users = self.session.query(
            *self.COLUMN_LIST
        ).join(Role).all()
        return users

    def update(self, _id, **kwargs) -> type[Base] | None:
        role_id = kwargs.get('role_id', None)
        if not _id or not role_id:
            return None
        user = self.session.query(User).get(_id)
        role = self.session.query(Role).get(role_id)
        if user and role:
            user.role_id = role.id
            self.session.add(user)
            self.session.commit()
            return self.get(_id)
        return None


def get_user_service() -> UserService:
    return UserService(db, User)
