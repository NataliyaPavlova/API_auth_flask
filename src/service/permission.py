from src.models.db_models import Base
from src.models.db_models import Permission
from src.service.base import BaseService
from src.storages.db_connect import db


class PermissionService(BaseService):
    def add(self, title: str) -> type[Base] | None:
        if title:
            if self.get_by(title=title):
                return None

            permission = self.create(title=title)
            return permission
        return None

    def update(self, **kwargs):
        if instance := self.get(_id=kwargs.get('id', None)):
            if title := kwargs.get('title', None):
                instance.title = title
                self.session.add(instance)
                self.session.commit()
                return True
            return None
        return None


def get_permission_service() -> PermissionService:
    return PermissionService(db, Permission)
