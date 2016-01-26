from datetime import datetime,date
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import NotFound
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import url_for, current_app
from flask.ext.sqlalchemy import SQLAlchemy
from .helpers import args_from_url
from .errors import ValidationError

db = SQLAlchemy()

def string2date(string):
    return datetime.strptime(string, '%Y-%m-%d').date()

def date2string(date):
    return date.strftime('%Y-%m-%d')

class TipoServico(object):
    PRETO = 1
    VERMELHO = 2
    ROXA = 3

class Servico(db.Model):
    __tablename__ = 'servico'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column('usuario_id', db.Integer, db.ForeignKey('usuario.id'))
    escala_id = db.Column('escala_id', db.Integer, db.ForeignKey('escala.id'))
    data = db.Column(db.Date, default=datetime.utcnow)
    tipo = db.Column(db.Integer)

    def __init__(self,data=None,tipo=None,id=None,usuario_id=None,escala_id=None):
        self.id = id 
        self.data = data
        self.tipo = tipo
        self.usuario_id = usuario_id
        self.escala_id = escala_id
        if usuario_id:
            self.usuario = Usuario.query.get_or_404(usuario_id)
        if escala_id:
            self.escala = Escala.query.get_or_404(escala_id)
    def __repr__(self):
        return repr((date2string(self.data),self.tipo,self.escala))

    def get_url(self):
        return url_for('api.get_servico', id=self.id, _external=True)

    def to_json(self):
        return {
            'url': self.get_url(),
            'usuario': url_for('api.get_usuario', id=self.usuario_id,_external=True),
            'escala': url_for('api.get_escala', id=self.escala_id,_external=True),
            'data': date2string(self.data),
            'tipo': self.tipo
        }

    def from_json(self, json):
        try:
            usuario_id = args_from_url(json['usuario'], 'api.get_usuario')['id']
            self.usuario = Usuario.query.get_or_404(usuario_id)
        except (KeyError, NotFound):
            raise ValidationError('Invalid usuario URL')
        try:
            escala_id = args_from_url(json['escala'], 'api.get_escala')['id']
            self.escala = Escala.query.get_or_404(escala_id)
        except (KeyError, NotFound):
            raise ValidationError('Invalid escala URL')
        try:
            date = string2date(json['data'])
            self.data = date 
        except KeyError:
            raise ValidationError('Invalid data: '+json['data'])
        try:
            self.tipo = json['tipo']
        except KeyError as e:
            raise ValidationError('Invalid servico: missing ' + e.args[0])
        return self

usuario_escala = db.Table ('usuario_escala',
     db.Column('usuario_id', db.Integer, db.ForeignKey('usuario.id')),
     db.Column('escala_id', db.Integer, db.ForeignKey('escala.id'))
)

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True)
    nome_guerra = db.Column(db.String(50))
    email = db.Column(db.String(50))
    especialidade = db.Column(db.String(100))
    posto = db.Column(db.String(25))
    saram = db.Column(db.Integer)
    data_promocao = db.Column(db.Date, default=datetime.utcnow)
    username = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))
    afastamentos = db.relationship('Afastamento',cascade="all, delete-orphan")
    servicos = db.relationship('Servico',backref=db.backref('usuario', lazy='joined'),lazy='dynamic', cascade='all, delete-orphan')
    escalas = db.relationship('Escala', secondary=usuario_escala,lazy='dynamic')


    def get_url(self):
        return url_for('api.get_usuario', id=self.id, _external=True)

    def to_json(self):
        return {
            'id': self.id,
            'url': self.get_url(),
            'name': self.name,
            'nome_guerra': self.nome_guerra,
            'email': self.email,
            'especialidade': self.especialidade,
            'posto': self.posto,
            'saram': self.saram,
            'username': self.username,
            'data_promocao': date2string(self.data_promocao),
            'escalas': url_for('api.get_usuario_escala',id=self.id, _external=True),
            'afastamentos': url_for('api.get_usuario_afastamento',id=self.id, _external=True),
            'servicos': url_for('api.get_usuario_servico',id=self.id, _external=True)
        }

    def from_json(self, json):
        try:
            date = string2date(json['data_promocao'])
            self.data_promocao = date
        except KeyError as e:
            raise ValidationError('Invalid date: '+ e.args[0])
        try:
            self.username = json['username']
            self.password = json['username']
            self.nome_guerra = json['nome_guerra']
            self.name = json['name']
            self.email = json['email']
            self.especialidade = json['especialidade']
            self.posto = json['posto']
            self.saram = json['saram']
        except KeyError as e:
            raise ValidationError('Invalid usuario: missing ' + e.args[0])
        return self

    def __repr__(self):
        return repr((self.name,self.saram,self.antiguidade,self.servicos.all()))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        print self.username,self.password_hash
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expires_in=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return Usuario.query.get(data['id'])

    @property
    def antiguidade(self):
        return int(self.data_promocao.year/self.data_promocao.month/self.data_promocao.day)

    def vermelhas(self):
        return [servico for servico in self.servicos.all() if servico.tipo == TipoServico.VERMELHO]

    def pretas(self):
        return [servico for servico in self.servicos.all() if servico.tipo == TipoServico.PRETO]
    
    def roxas(self):
        return [servico for servico in self.servicos.all() if servico.tipo == TipoServico.ROXA]

    def by_vermelha_key(milico):
        servicos = milico.vermelhas()
        return milico.hash_service(servicos)
        
    def by_preta_key(milico):
        servicos = milico.pretas()
        return milico.hash_service(servicos)
     
    def by_roxa_key(milico):
        servicos = milico.roxas()
        return milico.hash_service(servicos)
        
    def hash_service(milico,servicos):
        total = 0
        if len(servicos) > 0:
            total += reduce(lambda x,y: x*y*3,map(lambda x: x.data.year * x.data.month * x.data.day*3,servicos))
        total += milico.antiguidade
        return total

class Escala(db.Model):
    __tablename__ = 'escala'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True)
    servicos = db.relationship('Servico',backref=db.backref('escala', lazy='joined'),lazy='dynamic', cascade='all, delete-orphan')
    usuarios = db.relationship('Usuario',secondary=usuario_escala,lazy='dynamic')
    feriados = []
    roxas = []

    def __repr__(self):
        return repr((self.name))
    
    def get_url(self):
        return url_for('api.get_escala', id=self.id, _external=True)

    def to_json(self):
        return {
            'id': self.id,
            'url': self.get_url(),
            'name': self.name,
            'usuarios': [usuario.to_json() for usuario in self.usuarios.all()],
            'usuarios_url': url_for('api.get_escala_usuario',id=self.id, _external=True),
            'servicos_url': url_for('api.get_escala_servico',id=self.id, _external=True)
        }

    def from_json(self, json):
        if json['usuarios']:
            try:
                for usuario in json['usuarios']:
                    print usuario
                    usuario_id = args_from_url(usuario['url'], 'api.get_usuario')['id']
                    self.usuarios.append(Usuario.query.get_or_404(usuario_id))
            except (KeyError, NotFound) as e:
                raise ValidationError('Invalid escala: missing ' + e.args[0])    
        try:
            self.name = json['name']
        except KeyError as e:
            raise ValidationError('Invalid escala: missing ' + e.args[0])
        return self


class Afastamento(db.Model):
    __tablename__ = 'afastamento'
    id = db.Column(db.Integer, primary_key=True)
    motivo = db.Column(db.String(50))
    data_inicio = db.Column(db.Date)
    data_fim = db.Column(db.Date)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    ativo = db.Column(db.Boolean,default=False)

    def __init__(self,motivo=None,data_inicio=None,data_fim=None,id=None,usuario_id=None):
        self.id = id 
        self.motivo = motivo
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.usuario_id = usuario_id
        if usuario_id:
            self.usuario = Usuario.query.get_or_404(usuario_id)

    def get_url(self):
        return url_for('api.get_afastamento', id=self.id, _external=True)

    def to_json(self):
        return {    
            'url': self.get_url(),
            'usuario': url_for('api.get_usuario', id=self.usuario_id, _external=True), 
            'motivo': self.motivo,
            'data_inicio': date2string(self.data_inicio),
            'data_fim': date2string(self.data_fim),
            'ativo': self.ativo
        }

    def from_json(self, json):
        try:
            self.usuario_id = args_from_url(json['usuario'], 'api.get_usuario')['id']
            self.usuario = Usuario.query.get_or_404(self.usuario_id)
        except (KeyError, NotFound):
            raise ValidationError('Invalid usuario URL')
        try:
            dt_inicio = string2date(json['data_inicio'])
            self.data_inicio = dt_inicio
        except KeyError as e:
            raise ValidationError('Invalid data_inicio: '+ e.args[0])
        try:
            dt_fim = string2date(json['data_fim'])
            self.data_fim = dt_fim
        except KeyError as e:
            raise ValidationError('Invalid data_fim: '+ e.args[0])
        try:
            self.motivo = json['motivo']
        except KeyError as e:
            raise ValidationError('Invalid afastamento: missing ' + e.args[0])
        return self


