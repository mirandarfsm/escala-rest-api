from flask import request,jsonify,g
from ..models import db,Servico
from ..decorators import json, paginate, etag
from . import api

@api.route('/usuarios/me/servicos/', methods=['GET'])
@etag
@paginate()
def get_usuario_servico():
    usuario = g.user
    return {'objects': [servico.to_json_min() for servico in usuario.servicos]}

@api.route('/usuarios/me/servicos/<int:id>', methods=['GET'])
@etag
@json
def get_usuario_servico_detail(id):
    usuario = g.user
    return usuario.servicos.get(id)