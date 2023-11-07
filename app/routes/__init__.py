from functools import wraps
import json
from flask_login import current_user


def JSONResponse(content: dict,
                 status_code: int,
                 headers: dict = {'ContentType': 'application/json'}) -> tuple:
    return json.dumps(content, default=str), status_code, headers


def login_required_json(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated:
            return JSONResponse({'error': 'Unauthorized'}, 401)
        return f(*args, **kwargs)

    return decorated
