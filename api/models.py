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
        #print type(timestamp)
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
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), index=True)
    nome_guerra = db.Column(db.String(50))
    email = db.Column(db.String(50))
    especialidade = db.Column(db.String(100))
    posto = db.Column(db.String(25))
    saram = db.Column(db.String(25))
    data_promocao = db.Column(db.Date, default=datetime.utcnow)
    username = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))
    ativo = db.Column(db.Boolean, default=True)
    perfis = db.relationship('UsuarioPerfil',back_populates="usuario", lazy='joined')
    afastamentos = db.relationship('Afastamento',back_populates="usuario", lazy='dynamic')
    escalas = db.relationship('UsuarioEscala',back_populates="usuario", lazy = 'dynamic')
    
    def get_url(self):
        return url_for('administracao.get_usuario', id=self.id, _external=True)

    def to_json(self):
        json = to_json(self, self.__class__)
        json['perfis'] = [usuario_perfil.perfil for usuario_perfil in self.perfis]
        del json['password_hash']
        return json

    def from_json(self, json):
        if 'perfis' in json:
            for perfil in json['perfis']:
                self.add_perfil(perfil)
        try:
            self.data_promocao = timestamp2date(json['data_promocao'])
        except KeyError as e:
            raise ValidationError('Invalid date: '+ e.args[0])
        try:
            self.username = json['username']
            self.password = json['username']
            self.nome_guerra = json['nome_guerra']
            self.nome = json['nome']
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
    
    def add_perfil(self,perfil):
        usuario_perfil = UsuarioPerfil(perfil = perfil) 
        self.perfis.append(usuario_perfil)
    
    def has_perfil(self,perfil):
        perfis = [usuario_perfil.perfil for usuario_perfil in self.perfis]
        #print perfis
        return perfil in perfis

class UsuarioPerfil(db.Model):
    __tablename__ = 'usuario_perfil'
    id = db.Column(db.Integer, primary_key = True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    usuario = db.relationship('Usuario', back_populates="perfis")
    perfil = db.Column(db.Integer)
    
    def to_json(self):
        pass
    
class Afastamento(db.Model):
    __tablename__ = 'afastamento'
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.relationship('Usuario', back_populates="afastamentos")
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    data_inicio = db.Column(db.Date)
    data_fim = db.Column(db.Date)
    motivo = db.Column(db.String(50))
    observacao = db.Column(db.String(300))
    data_revisao = db.Column(db.DateTime)
    ativo = db.Column(db.Boolean,default=False)

    def get_url(self):
        return url_for('administracao.get_afastamento', id=self.id, _external=True)

    def to_json(self):
        json = to_json(self, self.__class__)
        json['usuario'] = self.usuario.to_json()
        return json

    def from_json(self, json, id_usuario=None):
        if 'observacao' in json:
            self.observacao = json['observacao']
        try:
            self.id_usuario = id_usuario if id_usuario else json['usuario']['id'] #args_from_url(json['usuario']['url'], 'administracao.get_usuario')['id']
            self.usuario = Usuario.query.get_or_404(self.id_usuario)
        except (KeyError, NotFound):
            raise ValidationError('Invalid usuario ID')
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
        except KeyError as e:
            raise ValidationError('Invalid afastamento: missing ' + e.args[0])
        return self
    
class Escala(db.Model):
    __tablename__ = 'escala'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), index=True)
    tipo = db.Column(db.Integer,default=0)
    ativo = db.Column(db.Boolean, default=True)
    datas_especias = db.relationship('DataEspecial',back_populates = "escala", lazy = 'dynamic')
    usuarios = db.relationship('UsuarioEscala', back_populates = "escala", lazy = 'dynamic')
    
    def __repr__(self):
        return repr((self.nome))
    
    def get_url(self):
        return url_for('administracao.get_escala', id=self.id, _external=True)

    def to_json(self):
        json = to_json(self, self.__class__)
        json['datas'] = [data.to_json() for data in self.datas_especias]
        return json

    def from_json(self, json):
        try:
            self.nome = json['nome']
            self.tipo = json['tipo']
        except KeyError as e:
            raise ValidationError('Invalid escala: missing ' + e.args[0])
        return self
    
    def get_datas_vermelhas(self):
        return self.datas_especias.filter(DataEspecial.tipo == TipoServico.VERMELHO).all()
    
    def get_datas_roxas(self):
        return self.datas_especias.filter(DataEspecial.tipo == TipoServico.ROXA).all()

class DataEspecial(db.Model):
    __tablename__ = 'data_especial'
    id = db.Column(db.Integer, primary_key=True)
    id_escala = db.Column(db.Integer,db.ForeignKey('escala.id'))
    escala = db.relationship('Escala', back_populates = "datas_especias")
    data = db.Column(db.Date)
    tipo = db.Column(db.Integer)
    
    def to_json(self):
        json = to_json(self, self.__class__)
        return json

    def from_json(self, json):
        try:
            self.id_escala = json['escala']['id']
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
    id = db.Column(db.Integer, primary_key=True)
    id_escala = db.Column(db.Integer, db.ForeignKey('escala.id'))
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    escala = db.relationship('Escala', back_populates = "usuarios")
    usuario = db.relationship('Usuario', back_populates = "escalas")
    servicos = db.relationship('Servico',back_populates = "usuario_escala",lazy='dynamic')
    data_cadastro = db.Column(db.DateTime)
    data_fim = db.Column(db.DateTime)
    
    def to_json(self):
        json = to_json(self, self.__class__)
        json['usuario'] = self.usuario.to_json()
        json['escala'] = self.escala.to_json()
        return json
    
    def from_json(self, json):
        try:
            self.id_usuario = json['usuario']['id']
            self.usuario = Usuario.query.get_or_404(self.id_usuario)
        except (KeyError, NotFound):
            raise ValidationError('Invalid usuario id')
        try:
            self.id_escala = json['escala']['id']
            self.escala = Escala.query.get_or_404(self.id_escala)
        except (KeyError, NotFound):
            raise ValidationError('Invalid escala id')
        return self
    
    def vermelhas(self):
        return [servico for servico in self.servicos if servico.tipo == TipoServico.VERMELHO]

    def pretas(self):
        return [servico for servico in self.servicos if servico.tipo == TipoServico.PRETO]
    
    def roxas(self):
        return [servico for servico in self.servicos if servico.tipo == TipoServico.ROXA]

    def by_vermelha_key(usuario_escala):
        servicos = usuario_escala.roxas()
        return usuario_escala.hash_service(servicos)
        
    def by_preta_key(usuario_escala):
        servicos = usuario_escala.pretas()
        return usuario_escala.hash_service(servicos)
     
    def by_roxa_key(usuario_escala):
        servicos = usuario_escala.vermelhas()
        return usuario_escala.hash_service(servicos)
        
    def hash_service(usuario_escala,servicos):
        total = 0
        if len(servicos) > 0:
            total += reduce(lambda x,y: x*y*3,map(lambda x: x.data.year * x.data.month * x.data.day*3,servicos))
        total += usuario_escala.usuario.antiguidade
        return total

class Servico(db.Model):
    __tablename__ = 'servico'
    id = db.Column(db.Integer, primary_key=True)
    id_usuario_escala = db.Column(db.Integer, db.ForeignKey('usuario_escala.id'))
    usuario_escala = db.relationship('UsuarioEscala',back_populates='servicos')
    data = db.Column(db.Date, default=datetime.utcnow)
    tipo = db.Column(db.Integer)
            
    def get_url(self):
        return url_for('administracao.get_servico', id=self.id, _external=True)

    def to_json(self):
        json = to_json(self, self.__class__)
        json['usuario_escala'] = self.usuario_escala.to_json()
        return json

    def from_json(self, json):
        try:
            self.id_usuario_escala = json['usuario_escala']['id']
            self.usuario_escala = UsuarioEscala.query.get_or_404(self.id_usuario_escala)
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
    id_substituto = db.Column(db.Integer, db.ForeignKey('usuario_escala.id'))
    id_substituido = db.Column(db.Integer, db.ForeignKey('usuario_escala.id'))
    id_servico = db.Column(db.Integer, db.ForeignKey('servico.id'))
    substituto = db.relationship('UsuarioEscala',foreign_keys=[id_substituto], lazy='joined')
    substituido = db.relationship('UsuarioEscala',foreign_keys=[id_substituido], lazy='joined')
    servico = db.relationship("Servico",lazy='joined')
    motivo = db.Column(db.String(50))
    data_solicitacao = db.Column(db.DateTime)
    data_troca_servico = db.Column(db.DateTime)
    
    def get_url(self):
        return url_for('api.get_usuario_troca_servico', id=self.id, _external=True)

    def to_json(self):
        json = to_json(self, self.__class__)
        json['servico'] = self.servico.to_json()
        json['substituido'] = self.substituido.to_json()
        json['substituto'] = self.substituto.to_json()
        return json

    def from_json(self, json):
        try:
            self.id_servico = json['servico']['id']
            self.servico = Servico.query.get_or_404(self.id_servico)
        except (KeyError, NotFound):
            raise ValidationError('Invalid servico ID')
        self.substituido = self.servico.usuario_escala
        self.data_solicitacao = datetime.now()
        return self