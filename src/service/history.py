from src.models.db_models import History
from src.service.base import BaseService
from src.storages.db_connect import db


class HistoryService(BaseService):
    pass


def get_history_service() -> HistoryService:
    return HistoryService(db, History)
