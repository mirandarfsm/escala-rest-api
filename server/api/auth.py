from flask import current_app, g
from flask_httpauth import HTTPBasicAuth
from .models import Usuario
from .errors import unauthorized

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username_or_token, password):
    if current_app.config['USE_TOKEN_AUTH']:
        # token authentication
        g.user = Usuario.verify_auth_token(username_or_token)
        return g.user is not None and g.user.ativo == True
    else:
        # username/password authentication
        g.user = Usuario.query.filter_by(username=username_or_token).first()
        return g.user is not None and g.user.verify_password(password) and g.user.ativo == True

@auth.error_handler
def unauthorized_error():
    res = unauthorized('Please authenticate to access this token API')
    res.headers['WWW-Authenticate'] = 'x' + auth.authenticate_header()
    return res