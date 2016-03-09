from flask import url_for, request,jsonify
from ...models import db, Servico
from ...decorators import json, paginate, etag
from . import api

@api.route('/servicos/', methods=['GET'])
@etag
@paginate()
def get_servicos():
    return Servico.query

@api.route('/servicos/<int:id>', methods=['GET'])
@etag
@json
def get_servico(id):
    return Servico.query.get_or_404(id)

@api.route('/servicos/', methods=['POST'])
@json
def new_servico():
    servico = Servico().from_json(request.json)
    db.session.add(servico)
    db.session.commit()
    return {}, 201, {'Location': servico.get_url()}

@api.route('/servicos/<int:id>', methods=['PUT'])
@json
def edit_servico(id):
    servico = Servico.query.get_or_404(id)
    servico.from_json(request.json)
    db.session.add(servico)
    db.session.commit()
    return {}

@api.route('/servicos/', methods=['DELETE'])
@json
def delete_all_servico():
    servicos = Servico.query.all()
    for servico in servicos:
        db.session.delete(servico)
    db.session.commit()
    return {}

@api.route('/servicos/<int:id>', methods=['DELETE'])
@json
def delete_servico(id):
    servico = Servico.query.get_or_404(id)
    db.session.delete(servico)
    db.session.commit()
    return {}