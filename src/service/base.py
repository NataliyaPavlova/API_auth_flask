from flask_sqlalchemy import SQLAlchemy

from src.models.db_models import Base


class BaseService:
    def __init__(
            self,
            db: SQLAlchemy,
            model: Base,
    ):
        self.model = model
        self.db = db
        self.session = self.db.session

    def get(self, _id: str) -> type[Base] | None:
        if not _id:
            return None
        if isinstance(_id, str):
            return self.session.query(self.model).get(_id)
        return None

    def filter_by(self, **kwargs) -> list[type[Base]] | list[None]:
        return self.session.query(self.model).filter_by(**kwargs).all()

    def get_by(self, **kwargs) -> type[Base] | None:
        result = self.session.query(self.model).filter_by(**kwargs).first()
        return result

    def create(self, **kwargs) -> type[Base] | None:
        instance = self.model(**kwargs)
        self.session.add(instance)
        self.session.commit()
        return instance

    def delete(self, _id: str) -> bool:
        if instance := self.get(_id):
            self.session.delete(instance)
            self.session.commit()
            return True
        return False

