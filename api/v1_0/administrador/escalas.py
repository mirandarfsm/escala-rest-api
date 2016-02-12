from flask import request,jsonify
from ..models import db, Escala
from ..decorators import json, paginate, etag
from . import api
from ..services import gerar_lista_militares_escalados 

@api.route('/escalas/', methods=['GET'])
def get_escalas():
    return jsonify({'escalas': [escala.to_json() for escala in Escala.query.all()]})

@api.route('/escalas/<int:id>', methods=['GET'])
def get_escala(id):
    escala = Escala.query.get_or_404(id)
    return jsonify(escala.to_json())

@api.route('/escalas/<int:id>/usuario/', methods=['GET'])
def get_escala_usuario(id):
    escala = Escala.query.get_or_404(id)
    return jsonify({'usuarios': [usuario.to_json() for usuario in escala.usuarios.all()]})

@api.route('/escalas/<int:id>/servico/', methods=['GET'])
def get_escala_servico(id):
    escala = Escala.query.get_or_404(id)
    return jsonify({'urls': [servico.get_url() for servico in escala.servicos.all()]})

@api.route('/escalas/<int:id>/afastamento/', methods=['GET'])
def get_escala_afastamento(id):
    escala = Escala.query.get_or_404(id)
    return jsonify({'urls': [afastamento.get_url() for afastamento in escala.afastamentos.all()]})

@api.route('/escalas/<int:id>/generate/', methods=['GET'])
def new_service_generate(id):
    escala = Escala.query.get_or_404(id)
    usuarios = gerar_lista_militares_escalados(escala)
    return jsonify({'usuarios': [usuario.to_json() for usuario in usuarios]})

@api.route('/escalas/', methods=['POST'])
def new_escala():
    escala = Escala().from_json(request.json)
    db.session.add(escala)
    db.session.commit()
    reponse = jsonify({})
    reponse.status_code = 201
    reponse.headers['Location'] = escala.get_url()
    return reponse

@api.route('/escalas/<int:id>', methods=['PUT'])
def edit_escala(id):
    escala = Escala.query.get_or_404(id)
    escala.from_json(request.json)
    db.session.add(escala)
    db.session.commit()
    return jsonify({})

@api.route('/escalas/<int:id>', methods=['DELETE'])
def delete_escala(id):
    escala = Escala.query.get_or_404(id)
    db.session.delete(escala)
    db.session.commit()
    return jsonify({})