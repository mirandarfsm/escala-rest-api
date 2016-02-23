from flask import request,jsonify,g
from ..models import db, Usuario,Afastamento,Servico,Escala,TrocaServico
from ..services import fazer_trocar_servico
from ..decorators import json, paginate, etag
from . import api

@api.route('/usuario/', methods=['GET'])
@etag
@json
def get_usuarios():
    return g.user

@api.route('/usuario/escalas/', methods=['GET'])
@etag
@json
def get_usuario_escala():
    usuario = g.user
    return {'objects': [escala.to_json_min() for escala in usuario.escalas]}

@api.route('/usuario/escalas/<int:id>', methods=['GET'])
@etag
@json
def get_usuario_escala_detail(id):
    usuario = g.user
    return usuario.escalas.get(id)

@api.route('/usuario/servicos/', methods=['GET'])
@etag
@json
def get_usuario_servico():
    usuario = g.user
    return {'objects': [servico.to_json_min() for servico in usuario.servicos]}

@api.route('/usuario/servicos/<int:id>', methods=['GET'])
@etag
@json
def get_usuario_servico_detail(id):
    usuario = g.user
    return usuario.servicos.get(id)

@api.route('/usuario/afastamentos/', methods=['GET'])
@etag
@json
def get_usuario_afastamento():
    usuario = g.user
    return {'objects': [afastamento.to_json_min() for afastamento in usuario.afastamentos]}

@api.route('/usuario/afastamentos/<int:id>', methods=['GET'])
@etag
@json
def get_usuario_afastamento_detail(id):
    usuario = g.user
    return usuario.afastamentos.filter(Afastamento.id==id).one()

@api.route('/usuario/troca/servico/', methods=['GET'])
@etag
@json
def get_usuario_troca_servico():
    usuario = g.user
    return{'objects': [troca_servico.to_json_min() for troca_servico in usuario.troca_servicos]}

@api.route('/usuario/troca/servico/pendentes/',methods=['GET'])
@etag
@json
def get_usuario_troca_servico_pedente():
    usuario = g.user
    troca_servicos = TrocaServico.query \
                        .join(TrocaServico.servico) \
                        .join(Servico.escala) \
                        .filter(Escala.id.in_(escala.id for escala in usuario.escalas)) \
                        .filter(TrocaServico.substituto == None) \
                        .filter(TrocaServico.substituido != usuario)
    return {'objects': [troca_servico.to_json_min() for troca_servico in troca_servicos]}


@api.route('/usuario/troca/servico/<int:id>', methods=['GET'])
@etag
@json
def get_usuario_troca_servico_detail(id):
    #not implemented
    usuario = g.user
    return usuario.troca_servicos.get(id)

@api.route('/usuario/troca/servico/pendentes/<int:id>',methods=['GET'])
@etag
@json
def get_usuario_troca_servico_pedente_detail(id):
    #not implemented
    usuario = g.user
    troca_servico = TrocaServico.query.filter(TrocaServico.servicos.any(Servico.escala.in_(usuario.escalas))).filter(TrocaServico.data == None).filter(TrocaServico.id(id)).one()
    return troca_servico


@api.route('/usuario/<int:id>', methods=['PUT'])
@json
def edit_usuario(id):
    usuario = g.user
    try:
        usuario.password = json['password']
        usuario.email = json['email']
    except KeyError as e:
        raise ValidationError('Invalid usuario: missing ' + e.args[0])
    db.session.add(usuario)
    db.session.commit()
    return {}

@api.route('/usuario/afastamentos/', methods=['POST'])
@json
def new_afastamento():
    usuario = g.user
    afastamento = Afastamento().from_json(request.json)
    afastamento.usuario = usuario
    db.session.add(afastamento)
    db.session.commit()
    return {}, 201, {'Location': afastamento.get_url()}

@api.route('/usuario/afastamentos/<int:id>', methods=['PUT'])
@json
def edit_afastamento(id):
    afastamento = Afastamento.query.get_or_404(id)
    afastamento.from_json(request.json)
    db.session.add(afastamento)
    db.session.commit()
    return {}

@api.route('/usuario/afastamentos/<int:id>', methods=['DELETE'])
@json
def delete_afastamento():
    afastamento = Afastamento.query.get_or_404(id)
    db.session.delete(afastamento)
    db.session.commit()
    return {}

@api.route('/usuario/troca/servico/', methods=['POST'])
@json
def new_troca_servico():
    usuario = g.user
    troca_servico = TrocaServico().from_json(request.json)
    troca_servico.substituido = usuario
    print troca_servico
    db.session.add(troca_servico)
    db.session.commit()
    return {}, 201, {'Location': usuario.get_url()}

@api.route('/usuario/troca/servico/<int:id>/aceitar/', methods=['PUT'])
@json
def aceitar_troca_servico(id):
    usuario = g.user
    troca_servico = TrocaServico.query.get_or_404(id)
    fazer_trocar_servico(troca_servico,usuario)
    return {}

@api.route('/usuario/troca/servico/<int:id>', methods=['PUT'])
@json
def edit_troca_servico():
    #implementar
    return {}

@api.route('/usuario/troca/servico/<int:id>', methods=['DELETE'])
@json
def delete_troca_servico(id):
    troca_servico = TrocaServico.query.get_or_404(id)
    db.session.delete(troca_servico)
    db.session.commit()
    return {}