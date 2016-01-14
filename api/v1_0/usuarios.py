from flask import request,jsonify
from ..models import db, Usuario
from ..decorators import json, paginate, etag
from . import api


@api.route('/usuarios/', methods=['GET'])
def get_usuarios():
    return jsonify({'usuarios': [usuario.to_json() for usuario in Usuario.query.all()]})

@api.route('/usuarios/<int:id>', methods=['GET'])
def get_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    return jsonify(usuario.to_json())

@api.route('/usuarios/<int:id>/escala/', methods=['GET'])
def get_usuario_escala(id):
    usuario = Usuario.query.get_or_404(id)
    return jsonify({'urls': [escala.get_url() for escala in usuario.escalas.all()]})

@api.route('/usuarios/<int:id>/servico/', methods=['GET'])
def get_usuario_servico(id):
    usuario = Usuario.query.get_or_404(id)
    return jsonify({'urls': [servico.get_url() for servico in usuario.servicos.all()]})

@api.route('/usuarios/<int:id>/afastamento/', methods=['GET'])
def get_usuario_afastamento(id):
    usuario = Usuario.query.get_or_404(id)
    return jsonify({'urls': [afastamento.get_url() for afastamento in usuario.afastamentos]})

@api.route('/usuarios/', methods=['POST'])
def new_usuario():
    usuario = Usuario().from_json(request.json)
    db.session.add(usuario)
    db.session.commit()
    reponse = jsonify({})
    reponse.status_code = 201
    reponse.headers['Location'] = usuario.get_url()
    return reponse

@api.route('/usuarios/<int:id>', methods=['PUT'])
def edit_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    usuario.from_json(request.json)
    db.session.add(usuario)
    db.session.commit()
    return jsonify({})

@api.route('/usuarios/<int:id>', methods=['DELETE'])
def delete_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({})
