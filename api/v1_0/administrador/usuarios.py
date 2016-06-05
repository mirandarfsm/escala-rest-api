from flask import request,jsonify
from ...models import db, Usuario
from ...decorators import json, paginate, etag
from . import api
from ...controller import UsuarioEscalaController

@api.route('/usuarios/', methods=['GET'])
@etag
@paginate()
def get_usuarios():
    return Usuario.query

@api.route('/usuarios/<int:id>/', methods=['GET'])
@etag
@json
def get_usuario(id):
    return Usuario.query.get_or_404(id) 

@api.route('/usuarios/<int:id>/escala/', methods=['GET'])
@etag
@paginate()
def get_usuario_escala(id):
    usuario = Usuario.query.get_or_404(id)
    return usuario.escalas
    #return usuario.escalas.filter(UsuarioEscala.dt_fim == None)

@api.route('/usuarios/<int:id>/afastamento/', methods=['GET'])
@etag
@paginate()
def get_usuario_afastamento(id):
    usuario = Usuario.query.get_or_404(id)
    return usuario.afastamentos

@api.route('/usuarios/', methods=['POST'])
@json
def new_usuario():
    usuario = Usuario().from_json(request.json)
    db.session.add(usuario)
    db.session.commit()
    return {}, 201, {'Location': usuario.get_url()}

@api.route('/usuarios/<int:id>/', methods=['PUT'])
@json
def edit_usuarios(id):
    usuario = Usuario.query.get_or_404(id)
    usuario.from_json(request.json)
    db.session.add(usuario)
    db.session.commit()
    return {}

@api.route('/usuarios/<int:id>/', methods=['DELETE'])
@json
def desativar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    #db.session.delete(usuario)
    usuario.ativo = not usuario.ativo
    UsuarioEscalaController().remover_usuario_de_escalas(usuario)
    db.session.add(usuario)
    db.session.commit()
    return {}
