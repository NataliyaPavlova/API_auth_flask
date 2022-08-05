from flask_restx._http import HTTPStatus


class InvalidAPIUsage(Exception):
    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, message, status_code: HTTPStatus = None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

        self.answer = {
            "code": status_code,
            "message": message,
        }
