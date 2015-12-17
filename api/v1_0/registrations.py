from flask import url_for, request
from ..models import db, Registration
from ..decorators import json, paginate, etag
from . import api


@api.route('/registrations/', methods=['GET'])
@etag
@paginate()
def get_registrations():
    return Registration.query


@api.route('/registrations/<int:student_id>/<int:class_id>', methods=['GET'])
@etag
@json
def get_registration(student_id, class_id):
    return Registration.query.get_or_404((student_id, class_id))


@api.route('/registrations/', methods=['POST'])
@json
def new_registration():
    reg = Registration().from_json(request.json)
    db.session.add(reg)
    db.session.commit()
    return {}, 201, {'Location': reg.get_url()}


@api.route('/registrations/<int:student_id>/<int:class_id>', methods=['DELETE'])
@json
def delete_registration(student_id, class_id):
    reg = Registration.query.get_or_404((student_id, class_id))
    print(reg.student.id, reg.class_.id)
    db.session.delete(reg)
    db.session.commit()
    return {}
