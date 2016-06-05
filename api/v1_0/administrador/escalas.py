from flask import request,jsonify
from ...models import db, Escala,TipoEscala,Usuario,UsuarioEscala
from ...decorators import json, paginate, etag
from . import api
from ...services import ServicoDiarioService,ServicoSemanalService
from ...controller import UsuarioEscalaController

@api.route('/escalas/', methods=['GET'])
@etag
@paginate()
def get_escalas():
    return Escala.query

@api.route('/escalas/<int:id>/', methods=['GET'])
@etag
@json
def get_escala(id):
    return  Escala.query.get_or_404(id)

@api.route('/escalas/<int:id>/usuario/', methods=['GET'])
@etag
@paginate()
def get_escala_usuario(id):
    escala = Escala.query.get_or_404(id)
    return Usuario.query.join(UsuarioEscala).filter(UsuarioEscala.id_escala == escala.id, UsuarioEscala.data_fim == None)
@api.route('/escalas/<int:id>/generate/', methods=['PUT'])
@json
def new_service_generate(id):
    escala = Escala.query.get_or_404(id)
    hash = {}
    hash[TipoEscala.DIARIA] = ServicoDiarioService().gerar_lista_militares_escalados
    hash[TipoEscala.SEMANAL] = ServicoSemanalService().gerar_lista_militares_escalados
    hash[escala.tipo](escala)
    return {}

@api.route('/escalas/', methods=['POST'])
@json
def new_escala():
    escala = Escala().from_json(request.json)
    db.session.add(escala)
    if 'usuarios' in request.json:
        lista_id_usuario = [usuario['id'] for usuario in request.json['usuarios']]
        UsuarioEscalaController().modificar_lista_usuario(escala,lista_id_usuario)
    db.session.commit()
    return {}, 201, {'Location': escala.get_url()}

@api.route('/escalas/<int:id>/', methods=['PUT'])
@json
def edit_escala(id):
    escala = Escala.query.get_or_404(id)
    escala.from_json(request.json)
    db.session.add(escala)
    if 'usuarios' in request.json and escala.ativo:
        lista_id_usuario = [usuario['id'] for usuario in request.json['usuarios']]
        UsuarioEscalaController().modificar_lista_usuario(escala,lista_id_usuario)
    db.session.commit()
    return {}

@api.route('/escalas/<int:id>/', methods=['DELETE'])
@json
def delete_escala(id):
    escala = Escala.query.get_or_404(id)
    #db.session.delete(escala)
    escala.ativo = not escala.ativo
    UsuarioEscalaController().remover_escala_de_usuarios(escala)
    db.session.add(escala)
    db.session.commit()
    return {}