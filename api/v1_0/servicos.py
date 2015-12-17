from flask import url_for, request,jsonify
from ..models import db, Servico
from ..decorators import json, paginate, etag
from . import api

@api.route('/servicos/', methods=['GET'])
def get_servicos():
    return jsonify({'urls': [servico.get_url() for servico in Servico.query.all()]})

@api.route('/servicos/<int:id>/', methods=['GET'])
def get_servico(id):
    servico = Servico.query.get_or_404(id)
    return jsonify(servico.to_json())

@api.route('/servicos/', methods=['POST'])
def new_servico():
    servico = Servico().from_json(request.json)
    db.session.add(servico)
    db.session.commit()
    reponse = jsonify({})
    reponse.status_code = 201
    reponse.headers['Location'] = servico.get_url()
    return reponse

@api.route('/servicos/<int:id>/', methods=['PUT'])
def edit_servico(id):
    servico = Servico.query.get_or_404(id)
    servico.from_json(request.json)
    db.session.add(servico)
    db.session.commit()
    return jsonify({})

@api.route('/servicos/<int:id>/', methods=['DELETE'])
def delete_servico(id):
    servico = Servico.query.get_or_404(id)
    db.session.delete(servico)
    db.session.commit()
    return jsonify({})