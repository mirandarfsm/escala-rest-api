from flask import url_for, request,jsonify
from ...models import db, Afastamento
from ...decorators import json, paginate, etag
from . import api

@api.route('/afastamentos/', methods=['GET'])
@etag
@paginate()
def get_afastamentos():
    c=  Afastamento.query
    print c.all()[0].to_json()
    return c 

@api.route('/afastamentos/<int:id>/', methods=['GET'])
@etag
@json
def get_afastamento(id):
    return Afastamento.query.get_or_404(id)

@api.route('/afastamentos/', methods=['POST'])
@json
def new_afastamento():
    afastamento = Afastamento().from_json(request.json)
    db.session.add(afastamento)
    db.session.commit()
    return {}, 201, {'Location': afastamento.get_url()}

@api.route('/afastamentos/<int:id>/', methods=['PUT'])
@json
def edit_afastamento(id):
    afastamento = Afastamento.query.get_or_404(id)
    afastamento.from_json(request.json)
    db.session.add(afastamento)
    db.session.commit()
    return {}

@api.route('/afastamentos/<int:id>/', methods=['DELETE'])
@json
def delete_afastamento(id):
    afastamento = Afastamento.query.get_or_404(id)
    db.session.delete(afastamento)
    db.session.commit()
    return {}