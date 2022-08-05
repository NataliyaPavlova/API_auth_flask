import uuid
from datetime import datetime

from sqlalchemy import DateTime, Column
from sqlalchemy.dialects.postgresql import UUID


class IDMixin(object):
    __table_args__ = {'extend_existing': True}
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )


class TimestampMixin(object):
    __table_args__ = {'extend_existing': True}

    created = Column(
        DateTime,
        nullable=False,
        default=datetime.now,
    )
    modified = Column(
        DateTime,
        nullable=False,
        default=datetime.now,
    )
