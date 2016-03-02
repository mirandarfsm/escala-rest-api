from flask import request,g
from ..models import db, Escala
from ..decorators import json, paginate, etag
from . import api

@api.route('/usuarios/me/escalas/', methods=['GET'])
@etag
@paginate()
def get_usuario_escala():
    usuario = g.user
    return {'objects': [escala.to_json_min() for escala in usuario.escalas]}

@api.route('/usuarios/me/escalas/<int:id>', methods=['GET'])
@etag
@json
def get_usuario_escala_detail(id):
    usuario = g.user
    return usuario.escalas.get(id)

