from flask import url_for, request,jsonify
from ...models import db, Afastamento
from ...decorators import json, paginate, etag
from . import api

@api.route('/afastamentos/', methods=['GET'])
@etag
@paginate()
def get_afastamentos():
    return Afastamento.query

@api.route('/afastamentos/<int:id>/', methods=['GET'])
def get_afastamento(id):
    afastamento = Afastamento.query.get_or_404(id)
    return jsonify(afastamento.to_json())

@api.route('/afastamentos/', methods=['POST'])
def new_afastamento():
    afastamento = Afastamento().from_json(request.json)
    db.session.add(afastamento)
    db.session.commit()
    reponse = jsonify({})
    reponse.status_code = 201
    reponse.headers['Location'] = afastamento.get_url()
    return reponse

@api.route('/afastamentos/<int:id>/', methods=['PUT'])
def edit_afastamento(id):
    afastamento = Afastamento.query.get_or_404(id)
    afastamento.from_json(request.json)
    db.session.add(afastamento)
    db.session.commit()
    return jsonify({})

@api.route('/afastamentos/<int:id>/', methods=['DELETE'])
def delete_afastamento(id):
    afastamento = Afastamento.query.get_or_404(id)
    db.session.delete(afastamento)
    db.session.commit()
    return jsonify({})