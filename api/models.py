from datetime import datetime,date
import time
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import NotFound
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import url_for, current_app
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import types
from .helpers import args_from_url
from .errors import ValidationError

db = SQLAlchemy()

def to_json(inst, cls):
    """
    Jsonify the sql alchemy query result.
    """
    convert = dict()
    convert['DATE'] = date2timestamp
    # add your coversions for things like datetime's 
    # and what-not that aren't serializable.
    d = dict()
    for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        current_type = str(c.type)
        if current_type in convert.keys() and v is not None:
            try:
                d[c.name] = convert[current_type](v)
            except:
                d[c.name] = "Error:  Failed to covert using ", str(convert[c.type])
        elif v is None:
            d[c.name] = str()
        else:
            d[c.name] = v
    return d

def timestamp2date(timestamp):
    #return datetime.fromtimestamp(timestamp/1e3)
    if timestamp:
        print type(timestamp)
        return datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
    return timestamp

def date2timestamp(date):
    #return time.mktime(date.timetuple())*1e3
    if date:
        return datetime.combine(date,datetime.min.time()).isoformat()
    return date

class TipoServico(object):
    PRETO = 0
    VERMELHO = 1
    ROXA = 2

class TipoEscala(object):
    DIARIA = 0
    SEMANAL = 1

class Perfil(object):
    ADMINISTRADOR = 0
    ESCALANTE = 1
    USUARIO = 2

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.BigInteger, primary_key=True)
    nome = db.Column(db.String(50), index=True)
    nome_guerra = db.Column(db.String(50))
    email = db.Column(db.String(50))
    especialidade = db.Column(db.String(100))
    posto = db.Column(db.String(25))
    saram = db.Column(db.String(25))
    data_promocao = db.Column(db.Date, default=datetime.utcnow)
    username = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))

    def get_url(self):
        return url_for('administracao.get_usuario', id=self.id, _external=True)

    def to_json(self):
        dict = to_json(self, self.__class__)
        del dict['password_hash']
        return dict

    def from_json(self, json):
        try:
            self.data_promocao = timestamp2date(json['data_promocao'])
        except KeyError as e:
            raise ValidationError('Invalid date: '+ e.args[0])
        try:
            self.username = json['username']
            self.password = json['username']
            self.nome_guerra = json['nome_guerra']
            self.nome = json['name']
            self.email = json['email']
            self.especialidade = json['especialidade']
            self.posto = json['posto']
            self.saram = json['saram']
        except KeyError as e:
            raise ValidationError('Invalid usuario: missing ' + e.args[0])
        return self

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
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
        return [servico for servico in self.servicos if servico.tipo == TipoServico.VERMELHO]

    def pretas(self):
        return [servico for servico in self.servicos if servico.tipo == TipoServico.PRETO]
    
    def roxas(self):
        return [servico for servico in self.servicos if servico.tipo == TipoServico.ROXA]

    def by_vermelha_key(milico):
        servicos = milico.roxas()
        return milico.hash_service(servicos)
        
    def by_preta_key(milico):
        servicos = milico.pretas()
        return milico.hash_service(servicos)
     
    def by_roxa_key(milico):
        servicos = milico.vermelhas()
        return milico.hash_service(servicos)
        
    def hash_service(milico,servicos):
        total = 0
        if len(servicos) > 0:
            total += reduce(lambda x,y: x*y*3,map(lambda x: x.data.year * x.data.month * x.data.day*3,servicos))
        total += milico.antiguidade
        return total

class UsuarioPerfil(db.Model):
    __tablename__ = 'usuario_perfil'
    id = db.Column(db.BigInteger, primary_key = True)
    usuario = db.relationship('Usuario',backref='perfis')
    perfil = db.Column(db.Integer)
    
class Afastamento(db.Model):
    __tablename__ = 'afastamento'
    id = db.Column(db.BigInteger, primary_key=True)
    usuario = db.relationship('Usuario')
    data_inicio = db.Column(db.Date)
    data_fim = db.Column(db.Date)
    motivo = db.Column(db.String(50))
    observacao = db.Column(db.String(300))
    data_aprovado = db.Column(db.DateTime)
    ativo = db.Column(db.Boolean,default=False)

    def get_url(self):
        return url_for('administracao.get_afastamento', id=self.id, _external=True)

    def to_json(self):
        return to_json(self, self.__class__)

    def from_json(self, json):
        if 'usuario' in json:
            try:
                self.usuario_id = json['usuario']['id'] #args_from_url(json['usuario']['url'], 'administracao.get_usuario')['id']
                self.usuario = Usuario.query.get_or_404(self.usuario_id)
            except (KeyError, NotFound):
                raise ValidationError('Invalid usuario URL')
        try:
            dt_inicio = timestamp2date(json['data_inicio'])
            self.data_inicio = dt_inicio
        except KeyError as e:
            raise ValidationError('Invalid data_inicio: '+ e.args[0])
        try:
            dt_fim = timestamp2date(json['data_fim'])
            self.data_fim = dt_fim
        except KeyError as e:
            raise ValidationError('Invalid data_fim: '+ e.args[0])
        try:
            self.motivo = json['motivo']
            self.observacao = json['observacao']
        except KeyError as e:
            raise ValidationError('Invalid afastamento: missing ' + e.args[0])
        return self
    
class Escala(db.Model):
    __tablename__ = 'escala'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(50), index=True)
    tipo = db.Column(db.Integer,default=0)
    
    def __repr__(self):
        return repr((self.name))
    
    def get_url(self):
        return url_for('administracao.get_escala', id=self.id, _external=True)

    def to_json(self):
        return to_json(self, self.__class__)

    def from_json(self, json):
        try:
            self.name = json['name']
            self.tipo = json['tipo']
        except KeyError as e:
            raise ValidationError('Invalid escala: missing ' + e.args[0])
        return self

class DataEspecial(db.Model):
    __tablename__ = 'data_especial'
    id = db.Column(db.BigInteger, primary_key=True)
    escala = db.relationship('Escala')
    data = db.Column(db.Date)
    tipo = db.Column(db.Integer)
    
    def to_json(self):
        return to_json(self, self.__class__)

    def from_json(self, json):
        if 'escala' in json:
            try:
                self.escala_id = json['escala']['id']
                self.escala = Escala.query.get_or_404(self.escala_id)
            except (KeyError, NotFound):
                raise ValidationError('Invalid escala URL')
        try:
            self.data = timestamp2date(json['data'])
            self.tipo = json['tipo']
        except KeyError as e:
            raise ValidationError('Invalid data especial: missing ' + e.args[0])
        return self

class UsuarioEscala(db.Model):
    __tablename__ = 'usuario_escala'
    id = db.Column(db.BigInteger, primary_key=True)
    escala = db.relationship('Escala')
    usuario = db.relationship('Usuario')
    data_cadastro = db.Column(db.DataTime)
    data_fim = db.Column(db.DataTime)
    
    def to_json(self):
        return to_json(self, self.__class__)
    
    def from_json(self, json):
        try:
            self.usuario_id = json['usuario']['id']
            self.usuario = Usuario.query.get_or_404(self.usuario_id)
        except (KeyError, NotFound):
            raise ValidationError('Invalid usuario id')
        try:
            self.escala_id = json['escala']['id']
            self.escala = Escala.query.get_or_404(self.escala_id)
        except (KeyError, NotFound):
            raise ValidationError('Invalid escala id')
        self.data_cadastro = datetime.now()
        return self

class Servico(db.Model):
    __tablename__ = 'servico'
    id = db.Column(db.BigInteger, primary_key=True)
    usuario_escala = db.relationship('UsuarioEscala',backref='servicos')
    data = db.Column(db.Date, default=datetime.utcnow)
    tipo = db.Column(db.Integer)
            
    def get_url(self):
        return url_for('administracao.get_servico', id=self.id, _external=True)

    def to_json(self):
        return to_json(self, self.__class__)

    def from_json(self, json):
        try:
            self.usuario_escala_id = json['usuario_escala']['id']
            self.usuario_escala = UsuarioEscala.query.get_or_404(self.usuario_escala_id)
        except (KeyError, NotFound, TypeError):
            raise ValidationError('Invalid usuario_escala id')
        try:
            self.data = timestamp2date(json['data'])
            self.tipo = json['tipo']
        except KeyError as e:
            raise ValidationError('Invalid servico: missing ' + e.args[0])
        return self

class TrocaServico(db.Model):
    __tablename__ = 'troca_servico'
    id = db.Column(db.Integer, primary_key=True)
    substituto = db.relationship('UsuarioEscala')
    substituido = db.relationship('UsuarioEscala')
    motivo = db.Column(db.String(50))
    data_solicitacao = db.Column(db.DateTime)
    data_troca_servico = db.Column(db.DateTime)
    servico = db.relationship("Servico", foreign_keys=[servico_id])
    
    def get_url(self):
        return url_for('api.get_usuario_troca_servico', id=self.id, _external=True)

    def to_json(self):
        return to_json(self, self.__class__)

    def from_json(self, json):
        try:
            servico_id = json['servico']['id']
            self.servico = Servico.query.get_or_404(servico_id)
        except (KeyError, NotFound):
            raise ValidationError('Invalid servico URL')
        self.substituido = self.servico.usuario_escala
        self.data_solicitacao = datetime.now()
        return self