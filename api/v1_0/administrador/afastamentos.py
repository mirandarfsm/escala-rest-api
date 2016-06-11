from flask import url_for, request,jsonify
from datetime import datetime
from ...models import db, Afastamento
from ...decorators import json, paginate, etag
from ...errors import ValidationError
from . import api

@api.route('/afastamentos/', methods=['GET'])
@etag
@json
def get_afastamentos():
    return Afastamento.query

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
    # Camada de servico
    afastamento = Afastamento.query.get_or_404(id)
    if afastamento.data_revisao is not None:
        raise ValidationError('Afastamento nao pode ser alterado')
    
    afastamento.from_json(request.json)
    
    if 'ativo' in request.json:
            if request.json['ativo']:
                AfastamentoController().verificar_usuario_tem_servico(afastamento)
            afastamento.ativo = request.json['ativo']
            afastamento.data_revisao = datetime.now()
    
    db.session.add(afastamento)
    db.session.commit()
    return {}

@api.route('/afastamentos/<int:id>/', methods=['DELETE'])
@json
def delete_afastamento(id):
    afastamento = Afastamento.query.get_or_404(id)
    if afastamento.data_revisao is not None:
        raise ValidationError('Afastamento nao pode ser alterado')
    db.session.delete(afastamento)
    db.session.commit()
    return {}