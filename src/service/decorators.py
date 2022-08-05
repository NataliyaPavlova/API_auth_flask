from functools import wraps

from flask import jsonify, request


def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            a_token = request.headers.get('Access-Token')
            if not a_token:
                return jsonify(msg="Admins only!"), 403


            claims = {'is_administrator': True}
            if claims['is_administrator']:
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Admins only!"), 403

        return decorator
    return wrapper
