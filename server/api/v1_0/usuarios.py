from flask import request,jsonify,g
from ..models import db, Usuario
from ..decorators import json, paginate, etag
from . import api
from ..errors import ValidationError

@api.route('/usuarios/me/', methods=['GET'])
@etag
@json
def get_usuario_detail():
    return g.user

@api.route('/usuarios/me/change-password/', methods=['PUT'])
@json
def edit_usuario():
    usuario = g.user
    try:
        new_password = request.json['new']
        old_password = request.json['old']
    except KeyError as e:
        raise ValidationError('Invalid usuario: missing ' + e.args[0])
    if (not usuario.verify_password(old_password)):
        raise ValidationError("Incorrect password!")
    if (new_password == old_password):
        raise ValidationError("Password is the same!")    
    usuario.password = new_password
    db.session.add(usuario)
    db.session.commit()
    return {}




