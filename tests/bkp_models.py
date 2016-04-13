import json
import unittest
from datetime import date,datetime
from werkzeug.exceptions import BadRequest
from api.app import create_app
from api.models import db, Usuario,Afastamento,Escala,Servico
from api.errors import ValidationError

class TestBD(unittest.TestCase):

    def setUp(self):
        self.app = create_app('test_config')
        self.ctx = self.app.app_context()
        self.ctx.push()
        #db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def popular_bd(self):
        self.popula_usuario()
        self.popupla_escala()
        self.popula_afastamento()

    def popula_usuario(self):
        u1 = Usuario(name = 'teste1', saram = 12211, email = 'teste@1')
        u2 = Usuario(name = 'teste2', saram = 12212, email = 'teste@2')
        u3 = Usuario(name = 'teste3', saram = 12213, email = 'teste@3')
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        db.session.commit()

    def popupla_escala(self):
        e1 = Escala(name = 'teste1')
        e2 = Escala(name = 'teste2')
        e3 = Escala(name = 'teste3')
        db.session.add(e1)
        db.session.add(e2)
        db.session.add(e3)
        db.session.commit()

    def popula_afastamento(self):
        a1 = Afastamento(motivo = 'teste1',data_inicio=date.today(),data_fim=date.today())
        a2 = Afastamento(motivo = 'teste2',data_inicio=date.today(),data_fim=date.today())
        a3 = Afastamento(motivo = 'teste3',data_inicio=date.today(),data_fim=date.today())
        db.session.add(a1)
        db.session.add(a2)
        db.session.add(a3)
        db.session.commit()

class TestUsuario(TestBD):
    
    def test_usuario_to_json(self):
        user = Usuario(name = 'teste', saram = 1221, email = 'teste@')
        db.session.add(user)
        db.session.commit()
        user_saved = Usuario.query.all()[0]
        self.assertEqual(user.to_json(),user_saved.to_json())

    def test_usuario_from_json(self):
        usuario_dict = {
            'name': 'teste',
            'saram': 1221,
            'email': 'teste@',
            'data_promocao': '2015-11-11'
        }
        usuario = Usuario().from_json(usuario_dict)
        db.session.add(usuario)
        db.session.commit()
        usuario_saved = Usuario.query.all()[0]
        self.assertEqual(usuario_dict['name'],usuario_saved.name)
        self.assertEqual(usuario_dict['saram'],usuario_saved.saram)


    def test_save_usuario(self):
        u = Usuario(name = 'teste', saram = 1221, email = 'teste@')
        db.session.add(u)
        db.session.commit()
        user = Usuario.query.get_or_404(1)
        self.assertEqual(user.name,u.name)
        self.assertEqual(user.saram,u.saram)
        self.assertEqual(user.email,u.email)

    def test_adiconar_usuario_no_afastamento(self):
        self.popular_bd()
        afastamento = Afastamento.query.all()[0]
        usuario = Usuario.query.all()[0]
        afastamento.usuario = usuario
        db.session.commit()
        afastamento_saved = Afastamento.query.get_or_404(afastamento.id)
        self.assertEqual(afastamento_saved.usuario,usuario)
        self.assertEqual(afastamento.usuario.id,afastamento_saved.usuario.id)
        self.assertEqual(afastamento.usuario.name,afastamento_saved.usuario.name)

    def test_adiconar_usuario_na_escala(self):
        self.popular_bd()
        usuario = Usuario.query.all()[0]
        escala = Escala.query.all()[0]
        escala.usuarios.append(usuario)
        db.session.commit()
        escala_saved = Escala.query.get_or_404(escala.id)
        self.assertEqual(escala_saved.usuarios[0],usuario)
        self.assertEqual(escala.usuarios[0].id,escala_saved.usuarios[0].id)
        self.assertEqual(escala.usuarios[0].name,escala_saved.usuarios[0].name)

class TestEscala(TestBD):

    def test_escala_to_json(self):
        escala = Escala(name = 'teste')
        db.session.add(escala)
        db.session.commit()
        escala_saved = Escala.query.all()[0]
        self.assertEqual(escala.name,escala_saved.to_json()['name'])

    def test_usuario_from_json(self):
        escala_dict = {
            'name': 'teste'
        }
        escala = Escala().from_json(escala_dict)
        db.session.add(escala)
        db.session.commit()
        escala_saved = Escala.query.all()[0]
        self.assertEqual(escala_dict['name'],escala_saved.name)

    def test_save_escala(self):
        e = Escala(name = 'teste')
        db.session.add(e)
        db.session.commit()
        escala = Escala.query.get_or_404(1)
        self.assertEqual(escala.name,e.name)

    def test_adiconar_escala_no_usuario(self):
        self.popular_bd()
        usuario = Usuario.query.all()[0]
        escala = Escala.query.all()[0]
        usuario.escalas.append(escala)
        db.session.commit()
        usuario_saved = Usuario.query.get_or_404(usuario.id)
        self.assertEqual(usuario_saved.escalas[0],escala)
        self.assertEqual(usuario.escalas[0].id,usuario_saved.escalas[0].id)
        self.assertEqual(usuario.escalas[0].name,usuario_saved.escalas[0].name)

class TestAfastamento(TestBD):

    def test_afastamento_to_json(self):
        self.popula_usuario()
        usuario = Usuario(id=1)
        afastamento = Afastamento(motivo='teste',data_inicio=date.today(),data_fim=date.today(),usuario_id=usuario.id)
        db.session.add(afastamento)
        db.session.commit()
        afastamento_saved = Afastamento.query.all()[0]
        self.assertEqual(afastamento.motivo,afastamento_saved.to_json()['motivo'])
        self.assertEqual(afastamento.data_inicio.strftime('%Y-%m-%d'),afastamento_saved.to_json()['data_inicio'])
        self.assertEqual(afastamento.data_fim.strftime('%Y-%m-%d'),afastamento_saved.to_json()['data_fim'])

    def test_afastamento_from_json(self):
        self.popula_usuario()
        usuario = Usuario.query.all()[0]
        afastamento_dict = {
            'usuario': usuario.get_url(),
            'motivo': 'teste',
            'data_inicio': '2015-10-10',
            'data_fim': '2015-11-11'
        }
        afastamento = Afastamento().from_json(afastamento_dict)
        db.session.add(afastamento)
        db.session.commit()
        afastamento_saved = Afastamento.query.all()[0]
        self.assertEqual(afastamento_dict['motivo'],afastamento_saved.motivo)
        self.assertEqual(afastamento_dict['data_inicio'],afastamento_saved.data_inicio.strftime('%Y-%m-%d'))
        self.assertEqual(afastamento_dict['data_fim'],afastamento_saved.data_fim.strftime('%Y-%m-%d'))


    def test_save_afastamento(self):
        a = Afastamento(motivo = 'teste',data_inicio=date.today(),data_fim=date.today())
        db.session.add(a)
        db.session.commit()
        afastamento = Afastamento.query.get_or_404(1)
        self.assertEqual(afastamento.motivo,a.motivo)
        self.assertEqual(afastamento.data_inicio,a.data_inicio)
        self.assertEqual(afastamento.data_fim,a.data_fim)

    def test_adiconar_afastamento_no_usuario(self):
        self.popular_bd()
        afastamento = Afastamento.query.all()[0]
        usuario = Usuario.query.all()[0]
        usuario.afastamentos.append(afastamento)
        db.session.commit()
        usuario_saved = Usuario.query.get_or_404(usuario.id)
        self.assertEqual(usuario_saved.afastamentos[0],afastamento)
        self.assertEqual(usuario.afastamentos[0].motivo,usuario_saved.afastamentos[0].motivo)
        self.assertEqual(usuario.afastamentos[0].data_inicio,usuario_saved.afastamentos[0].data_inicio)
        self.assertEqual(usuario.afastamentos[0].data_fim,usuario_saved.afastamentos[0].data_fim)

class TestServico(TestBD):      

    def test_servico_to_json(self):
        self.popula_usuario()
        self.popupla_escala()
        usuario = Usuario(id=1)
        escala = Escala(id=1)
        servico = Servico(data=date.today(),tipo=1,usuario_id=usuario.id,escala_id=escala.id)
        db.session.add(servico)
        db.session.commit()
        servico_saved = Servico.query.all()[0]
        self.assertEqual(servico.data.strftime('%Y-%m-%d'),servico_saved.to_json()['data'])
        self.assertEqual(servico.tipo,servico_saved.to_json()['tipo'])


    #Ignored
    def test_servico_from_json(self):
        self.popula_usuario()
        self.popupla_escala()
        escala = Escala.query.all()[0]
        usuario = Usuario.query.all()[0]
        servico_dict = {
            'usuario': usuario.get_url(),
            'escala': escala.get_url(),
            'tipo': 2,
            'data': '2015-11-11'
        }
        servico = Servico().from_json(servico_dict)
        db.session.add(servico)
        db.session.commit()
        servico_saved = Servico.query.all()[0]
        self.assertEqual(servico_dict['tipo'],servico_saved.tipo)
        self.assertEqual(servico_dict['data'],servico_saved.data.strftime('%Y-%m-%d'))

    def test_save_servico(self):
        s = Servico(data = date.today(),tipo=1)
        db.session.add(s)
        db.session.commit()
        servico = Servico.query.get_or_404(1)
        self.assertEqual(servico.data,s.data)
        self.assertEqual(servico.tipo,s.tipo)

    def test_adicionar_escala_usuario_no_servico(self):
        self.popular_bd()
        usuario = Usuario.query.all()[0]
        escala = Escala.query.all()[0]
        servico = Servico(usuario_id=usuario.id,escala_id=escala.id,data=date.today(),tipo=1)
        db.session.add(servico)
        db.session.commit()
        servico_saved = Servico.query.all()[0]
        self.assertEqual(servico_saved.escala,escala)
        self.assertEqual(servico_saved.usuario,usuario)