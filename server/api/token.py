from flask import Blueprint, jsonify, g,request
from flask_httpauth import HTTPBasicAuth
from .models import Usuario
from .errors import unauthorized
from .decorators import no_cache, json

token = Blueprint('token', __name__)
token_auth = HTTPBasicAuth()

@token_auth.verify_password
def verify_password(username_or_token, password):
    g.user = Usuario.query.filter_by(username=username_or_token).first()
    if not g.user:
        return False
    return g.user.verify_password(password) and g.user.ativo == True

@token_auth.error_handler
def unauthorized_error():
    res = unauthorized('Please authenticate to access this token API')
    res.headers['WWW-Authenticate'] = 'x' + token_auth.authenticate_header()
    return res


@token.route('/request-token')
@no_cache
@token_auth.login_required
@json
def request_token():
    teste = {'token': g.user.generate_auth_token(),'usuario': g.user.to_json()}
    return teste
