from flask import request,g
from sqlalchemy import exc
from ..models import db,Afastamento
from ..decorators import json, paginate, etag
from werkzeug.exceptions import abort
from . import api

@api.route('/usuarios/me/afastamentos/', methods=['GET'])
@etag
@paginate()
def get_usuario_afastamento():
    usuario = g.user
    return usuario.afastamentos

@api.route('/usuarios/me/afastamentos/<int:id>', methods=['GET'])
@etag
@json
def get_usuario_afastamento_detail(id):
    usuario = g.user
    try:
        return usuario.afastamentos.filter(Afastamento.id==id).one()
    except exc.NoResultFound, exc.MultipleResultsFound:
        abort(404)

@api.route('/usuarios/me/afastamentos/', methods=['POST'])
@json
def new_afastamento():
    usuario = g.user
    afastamento = Afastamento().from_json(request.json)
    afastamento.usuario = usuario
    db.session.add(afastamento)
    db.session.commit()
    return {}, 201, {'Location': afastamento.get_url()}

@api.route('/usuarios/me/afastamentos/<int:id>', methods=['PUT'])
@json
def edit_afastamento(id):
    usuario = g.user
    afastamento = usuario.afastamentos.filter(Afastamento.id==id).one()
    afastamento.from_json(request.json)
    db.session.add(afastamento)
    db.session.commit()
    return {}

@api.route('/usuarios/me/afastamentos/<int:id>', methods=['DELETE'])
@json
def delete_afastamento():
    usuario = g.user
    afastamento = usuario.afastamentos.filter(Afastamento.id==id).one()
    db.session.delete(afastamento)
    db.session.commit()
    return {}