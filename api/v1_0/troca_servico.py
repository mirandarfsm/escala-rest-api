from flask import request,jsonify,g
from ..models import db,Servico,Escala,TrocaServico
from ..services import fazer_trocar_servico
from werkzeug.exceptions import abort
from ..decorators import json, paginate, etag
from . import api

@api.route('/usuarios/me/troca-servico', methods=['GET'])
@etag
@paginate()
def get_usuario_troca_servico():
    usuario = g.user
    return usuario.troca_servicos

@api.route('/usuarios/me/troca-servico/<int:id>', methods=['GET'])
@etag
@json
def get_usuario_troca_servico_detail(id):
    #not implemented
    usuario = g.user
    return usuario.troca_servicos.filter(Servico.id==id).first() or abort(404)

@api.route('/usuarios/me/troca-servico/pendentes',methods=['GET'])
@etag
@paginate()
def get_usuario_troca_servico_pedente():
    usuario = g.user
    troca_servicos = TrocaServico.query \
                        .join(TrocaServico.servico) \
                        .join(Servico.escala) \
                        .filter(Escala.id.in_(escala.id for escala in usuario.escalas)) \
                        .filter(TrocaServico.substituto == None) \
                        .filter(TrocaServico.substituido != usuario)
    return troca_servicos

@api.route('/usuarios/me/troca-servico/pendentes/<int:id>',methods=['GET'])
@etag
@json
def get_usuario_troca_servico_pedente_detail(id):
    #not implemented
    usuario = g.user
    troca_servico = TrocaServico.query \
                    .filter(TrocaServico.servicos.any(Servico.escala.in_(usuario.escalas))) \
                    .filter(TrocaServico.data == None) \
                    .filter(TrocaServico.id(id)).first() or abort(404)
    return troca_servico
    
@api.route('/usuarios/me/troca-servico', methods=['POST'])
@json
def new_troca_servico():
    usuario = g.user
    troca_servico = TrocaServico().from_json(request.json)
    troca_servico.substituido = usuario
    db.session.add(troca_servico)
    db.session.commit()
    return {}, 201, {'Location': usuario.get_url()}

@api.route('/usuarios/me/troca-servico/<int:id>/aceitar', methods=['PUT'])
@json
def aceitar_troca_servico(id):
    usuario = g.user
    troca_servico = TrocaServico.query.get_or_404(id)
    fazer_trocar_servico(troca_servico,usuario)
    return {}

@api.route('/usuarios/me/troca-servico/<int:id>', methods=['PUT'])
@json
def edit_troca_servico():
    #implementar
    return {}

@api.route('/usuarios/me/troca-servico/<int:id>', methods=['DELETE'])
@json
def delete_troca_servico(id):
    usuario = g.user
    troca_servico = usuario.troca_servico.filter(Servico.id==id).first() or abort(404)
    db.session.delete(troca_servico)
    db.session.commit()
    return {}