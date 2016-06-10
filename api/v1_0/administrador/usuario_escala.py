'''
Created on 10 de jun de 2016

@author: mirandarfsm
'''
from flask import url_for, request,jsonify
from ...models import db, UsuarioEscala
from ...decorators import json, paginate, etag
from ...controller import UsuarioEscalaController
from . import api

@api.route('/usuario-escala/', methods=['GET'])
@etag
@json
def get_UsuarioEscalas():
    return UsuarioEscala.query

@api.route('/usuario-escala/<int:id>/', methods=['GET'])
@etag
@json
def get_UsuarioEscala(id):
    return UsuarioEscala.query.get_or_404(id)

@api.route('/usuario-escala/', methods=['POST'])
@json
def new_UsuarioEscala():
    usuario_escala = UsuarioEscala().from_json(request.json)
    db.session.add(usuario_escala)
    db.session.commit()
    return {}, 201, {'Location': UsuarioEscala.get_url()}

@api.route('/usuario-escala/<int:id>/', methods=['DELETE'])
@json
def delete_UsuarioEscala(id):
    usuario_escala = UsuarioEscala.query.get_or_404(id)
    UsuarioEscalaController.remover_usuario_escala(usuario_escala)
    #db.session.delete(UsuarioEscala)
    db.session.commit()
    return {}