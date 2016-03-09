from flask import request,jsonify,g
from ..models import db, Usuario
from ..decorators import json, paginate, etag
from . import api

@api.route('/usuarios/me/', methods=['GET'])
@etag
@json
def get_usuario_detail():
    return g.user

@api.route('/usuarios/me/', methods=['PUT'])
@json
def edit_usuario():
    usuario = g.user
    try:
        usuario.password = json['password']
        usuario.email = json['email']
    except KeyError as e:
        raise ValidationError('Invalid usuario: missing ' + e.args[0])
    db.session.add(usuario)
    db.session.commit()
    return {}



