from src.models.db_models import Base
from src.models.db_models import Permission
from src.models.db_models import Role
from src.models.db_models import RolePermission
from src.service.base import BaseService
from src.storages.db_connect import db


class RoleService(BaseService):
    def add(self, title: str) -> type[Base] | None:
        if title:
            if self.get_by(title=title):
                return None

            permission = self.create(title=title)
            return permission
        return None

    def update(self, **kwargs) -> type[Base] | None:
        if instance := self.get(_id=kwargs.get('id', None)):
            if title := kwargs.get('title', None):
                instance.title = title
                self.session.add(instance)
                self.session.commit()
                return instance
        return None

    def get_permissions(self, id: str) -> type[Base] | None:
        permissions = self.session.query(Permission). \
            join(RolePermission). \
            filter(RolePermission.role_id == id). \
            all()
        return permissions

    def add_permission(self, id: str, **kwargs) -> type[Base] | None:
        role = self.session.query(Role).get(id)
        permission_id = kwargs.get('permission_id', None)
        if not permission_id:
            return None
        permission = self.session.query(Permission).get(permission_id)
        if not role or not permission:
            return None
        role_permission = RolePermission(
            role_id=role.id,
            permission_id=permission.id,
        )
        self.session.add(role_permission)
        self.session.commit()
        return self.get_permissions(id)


def get_role_service() -> RoleService:
    return RoleService(db, Role)
