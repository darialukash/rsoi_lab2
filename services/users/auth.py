from flask import g, request, jsonify
from functools import wraps
from flask_httpauth import HTTPBasicAuth
from services.users.models import User

basic_auth = HTTPBasicAuth()


@basic_auth.verify_password
def verify_password(email, password):
    user = User.query.filter_by(email=email).first()
    if user is None:
        return False
    g.current_user = user
    return user.check_password(password)


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not verify_password(auth.username, auth.password):
            resp = jsonify({"message": "Please authenticate."})
            resp.status_code = 401
            resp.headers["WWW-Authenticate"] = 'Basic realm="Example"'
            return resp
        user = User.query.filter_by(email=auth.username).first()
        if kwargs["id"] != str(user.id):
            resp = jsonify({"message": "Please use proper password.",
                            "user_id": user.id,
                            "id": kwargs["id"]})
            resp.status_code = 401
            return resp
        kwargs["id"] = user.id
        return f(*args, **kwargs)

    return decorated
