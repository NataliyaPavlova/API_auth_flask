from typing import List

from sqlalchemy import String, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from src.models.mixins import IDMixin
from src.models.mixins import TimestampMixin
from datetime import datetime
from sqlalchemy import DateTime

Base = declarative_base()


class User(IDMixin, TimestampMixin, Base):
    __tablename__ = 'user'

    login = Column(
        String(length=128),
        unique=True,
        nullable=False,
    )
    password = Column(
        String(length=128),
        unique=True,
        nullable=False,
    )
    role_id = Column(
        UUID(as_uuid=True),
        ForeignKey('role.id'),
    )
    role = relationship(
        'Role',
        back_populates='user',
    )
    history = relationship(
        'History',
        back_populates='user',
    )


class History(IDMixin, Base):
    __tablename__ = 'history'

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey('user.id'),
    )
    user = relationship(
        'User',
        back_populates='history'
    )
    user_agent = Column(
        String(length=128),
    )
    created = Column(
        DateTime,
        nullable=False,
        default=datetime.now,
    )
    columns_out = [user_agent, created]

    @staticmethod
    def query_prepared_to_json(ar: List) -> List[dict] | List[None]:
        res = []
        for obj in ar:
            res.append(obj.as_dict())
        return res

    def as_dict(self) -> dict | None:
        """Make the dict from the record."""
        return {c.name: str(getattr(self, c.name)) for c in self.columns_out}


class Role(IDMixin, TimestampMixin, Base):
    __tablename__ = 'role'

    title = Column(
        String(length=30),
        nullable=False,
    )
    user = relationship(
        'User',
        back_populates='role'
    )
    permissions = relationship('RolePermission', backref='roles')


class Permission(IDMixin, TimestampMixin, Base):
    __tablename__ = 'permission'

    title = Column(
        String(length=50),
        nullable=False,
    )
    roles = relationship('RolePermission', backref='permissions')


class RolePermission(IDMixin, TimestampMixin, Base):
    __tablename__ = 'role_permission'

    role_id = Column(
        UUID(as_uuid=True),
        ForeignKey('role.id'),
        primary_key=True
    )

    permission_id = Column(
        UUID(as_uuid=True),
        ForeignKey('permission.id'),
        primary_key=True
    )
