from flask import current_app, g
from flask.ext.httpauth import HTTPBasicAuth
from .models import Usuario
from .errors import unauthorized

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username_or_token, password):
    if current_app.config['USE_TOKEN_AUTH']:
        # token authentication
        g.user = Usuario.verify_auth_token(username_or_token)
        return g.user is not None
    else:
        # username/password authentication
        g.user = Usuario.query.filter_by(username=username_or_token).first()
        return g.user is not None and g.user.verify_password(password)

@auth.error_handler
def unauthorized_error():
    return unauthorized('Please authenticate to access this token API')