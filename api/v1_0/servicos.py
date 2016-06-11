from flask import request,jsonify,g
from ..models import db,Servico,UsuarioEscala
from ..decorators import json, paginate, etag
from werkzeug.exceptions import abort
from . import api

@api.route('/usuarios/me/servicos/', methods=['GET'])
@etag
@json
def get_usuario_servico():
    usuario = g.user
    return Servico.query.join(UsuarioEscala).filter(UsuarioEscala.id_usuario == usuario.id)

@api.route('/usuarios/me/servicos/<int:id>/', methods=['GET'])
@etag
@json
def get_usuario_servico_detail(id):
    usuario = g.user
    return Servico.query.join(UsuarioEscala).filter(UsuarioEscala.id_usuario == usuario.id).filter(Servico.id == id).first()