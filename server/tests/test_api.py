import unittest
from werkzeug.exceptions import BadRequest
from .test_client import TestClient
from api.app import create_app
from api.models import db, Usuario
from api.errors import ValidationError


class TestAPI(unittest.TestCase):
    default_username = 'dave'
    default_password = 'cat'

    def setUp(self):
        self.app = create_app('test_config')
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.drop_all()
        db.create_all()
        u = Usuario(username=self.default_username,
                 password=self.default_password,admin=True)
        db.session.add(u)
        db.session.commit()
        self.client = TestClient(self.app, u.generate_auth_token(), '')

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_password_auth(self):
        self.app.config['USE_TOKEN_AUTH'] = False
        good_client = TestClient(self.app, self.default_username,
                                 self.default_password)
        rv, json = good_client.get('/api/v1.0/usuarios/')
        self.assertTrue(rv.status_code == 200)

        self.app.config['USE_TOKEN_AUTH'] = True
        u = Usuario.query.get(1)
        good_client = TestClient(self.app, u.generate_auth_token(), '')
        rv, json = good_client.get('/api/v1.0/usuarios/')
        self.assertTrue(rv.status_code == 200)

    def test_bad_auth(self):
        bad_client = TestClient(self.app, 'abc', 'def')
        rv, json = bad_client.get('/api/v1.0/usuarios/')
        self.assertTrue(rv.status_code == 401)

        self.app.config['USE_TOKEN_AUTH'] = True
        bad_client = TestClient(self.app, 'bad_token', '')
        rv, json = bad_client.get('/api/v1.0/usuarios/')
        self.assertTrue(rv.status_code == 401)

    def test_usuarios(self):
        # get collection
        rv, json = self.client.get('/api/v1.0/usuarios/')
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(len(json['objects']) == 1)

        # create new
        rv, json = self.client.post('/api/v1.0/usuarios/',
                                    data={
                                          'name': 'susan',
                                          'username':'susan',
                                          'nome_guerra':'susan',
                                          'especialidade':'3S',
                                          'posto':'SIN','email':'susan@',
                                          'saram':123,
                                          'data_promocao':"2016-03-28T00:00:00.0Z"
                                        }
                                    )
        self.assertTrue(rv.status_code == 201)
        susan_url = rv.headers['Location']

        # get
        rv, json = self.client.get(susan_url)
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['name'] == 'susan')
        self.assertTrue(json['url'] == susan_url)
        self.assertTrue(json['data_promocao'] == "2016-03-28T00:00:00")
        self.assertTrue(json['saram'] == 123)
        self.assertTrue(json['email'] == 'susan@')

        # create new
        rv, json = self.client.post('/api/v1.0/usuarios/',
                                    data={
                                          'name': 'david',
                                          'username':'david',
                                          'nome_guerra':'david',
                                          'especialidade':'1S',
                                          'posto':'SAD',
                                          'email':'david@',
                                          'saram':123,
                                          'data_promocao':"2016-03-28T11:08:12.144Z"
                                        }
                                    )
        self.assertTrue(rv.status_code == 201)
        david_url = rv.headers['Location']

        # get
        rv, json = self.client.get(david_url)
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['name'] == 'david')
        self.assertTrue(json['url'] == david_url)
        self.assertTrue(json['data_promocao'] == "2016-03-28T00:00:00")
        self.assertTrue(json['saram'] == 123)
        self.assertTrue(json['email'] == 'david@')


        # create bad request
        rv,json = self.client.post('/api/v1.0/usuarios/', data={})
        self.assertTrue(rv.status_code == 400)

        self.assertRaises(ValidationError, lambda:
            self.client.post('/api/v1.0/usuarios/',
                             data={'not-name': 'david'}))

        # modify
        rv, json = self.client.put(david_url, data={
                                          'name': 'david2',
                                          'username':'david',
                                          'nome_guerra':'david',
                                          'especialidade':'1S',
                                          'posto':'SAD',
                                          'email':'david@',
                                          'saram':123,
                                          'data_promocao':"2016-03-28T11:08:12.144Z"
                                        }
                                    )
        self.assertTrue(rv.status_code == 200)

        # get
        rv, json = self.client.get(david_url)
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['name'] == 'david2')

        # get collection
        rv, json = self.client.get('/api/v1.0/usuarios/')
        self.assertTrue(rv.status_code == 200)
        urls = [usuario['url'] for usuario in json['objects']]
        self.assertTrue(susan_url in urls)
        self.assertTrue(david_url in urls)
        self.assertTrue(len(urls) == 3)

        # delete
        rv, json = self.client.delete(susan_url)
        self.assertTrue(rv.status_code == 200)

        # get collection
        rv, json = self.client.get('/api/v1.0/usuarios/')
        self.assertTrue(rv.status_code == 200)
        urls = [usuario['url'] for usuario in json['objects']]
        self.assertFalse(susan_url in urls)
        self.assertTrue(david_url in urls)
        self.assertTrue(len(urls) == 2)

    def test_escalas(self):
        # get collection
        rv, json = self.client.get('/api/v1.0/escalas/')
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['objects'] == [])

        # create new
        rv, json = self.client.post('/api/v1.0/escalas/',
                                    data={
                                          'name': 'sobreaviso administrativo ccasj',
                                          'tipo':'0'
                                          }
                                    )
        self.assertTrue(rv.status_code == 201)
        administrativo_url = rv.headers['Location']

        # get
        rv, json = self.client.get(administrativo_url)
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['name'] == 'sobreaviso administrativo ccasj')
        self.assertTrue(json['url'] == administrativo_url)

        # create new
        rv, json = self.client.post('/api/v1.0/escalas/',
                                    data={
                                          'name': 'sobreaviso tecnico ccasj',
                                          'tipo': '1'
                                          }
                                    )
        self.assertTrue(rv.status_code == 201)
        tecnico_url = rv.headers['Location']

        # get
        rv, json = self.client.get(tecnico_url)
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['name'] == 'sobreaviso tecnico ccasj')
        self.assertTrue(json['url'] == tecnico_url)

        # create bad
        rv,json = self.client.post('/api/v1.0/escalas/', data={})
        self.assertTrue(rv.status_code == 400)

        self.assertRaises(ValidationError, lambda:
            self.client.post('/api/v1.0/escalas/', data={'not-name': 'tecnico'}))

        # modify
        rv, json = self.client.put(tecnico_url, data={
                                                      'name': 'tecnico2',
                                                      'tipo':'0'
                                                      }
                                   )
        self.assertTrue(rv.status_code == 200)

        # get
        rv, json = self.client.get(tecnico_url)
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['name'] == 'tecnico2')

        # get collection
        rv, json = self.client.get('/api/v1.0/escalas/')
        self.assertTrue(rv.status_code == 200)
        urls = [ escala['url'] for escala in json['objects'] ]
        self.assertTrue(administrativo_url in urls)
        self.assertTrue(tecnico_url in urls)
        self.assertTrue(len(urls) == 2)

        # delete
        rv, json = self.client.delete(tecnico_url)
        self.assertTrue(rv.status_code == 200)

        # get collection
        rv, json = self.client.get('/api/v1.0/escalas/')
        self.assertTrue(rv.status_code == 200)
        urls = [ escala['url'] for escala in json['objects'] ]
        self.assertTrue(administrativo_url in urls)
        self.assertFalse(tecnico_url in urls)
        self.assertTrue(len(urls) == 1)

    def test_servicos(self):
        # create new usuarios
        rv, json = self.client.post('/api/v1.0/usuarios/',
                                    data={
                                          'name': 'susan',
                                          'username':'susan',
                                          'nome_guerra':'susan',
                                          'especialidade':'3S',
                                          'posto':'SIN','email':'susan@',
                                          'saram':123,
                                          'data_promocao':"2016-03-28T00:00:00.0Z"
                                        }
                                    )
        self.assertTrue(rv.status_code == 201)
        susan_url = rv.headers['Location']

        rv, json = self.client.post('/api/v1.0/usuarios/',
                                   data={
                                          'name': 'david2',
                                          'username':'david',
                                          'nome_guerra':'david',
                                          'especialidade':'1S',
                                          'posto':'SAD',
                                          'email':'david@',
                                          'saram':123,
                                          'data_promocao':"2016-03-28T11:08:12.144Z"
                                        }
                                   )
        self.assertTrue(rv.status_code == 201)
        david_url = rv.headers['Location']

        # create new classes
        rv, json = self.client.post('/api/v1.0/escalas/',
                                    data={
                                          'name': 'sobreaviso administrativo ccasj',
                                          'tipo':'0'
                                          }
                                    )
        self.assertTrue(rv.status_code == 201)
        administrativo_url = rv.headers['Location']

        rv, json = self.client.post('/api/v1.0/escalas/',
                                    data={
                                          'name': 'sobreaviso tecnico ccasj',
                                          'tipo': '1'
                                          }
                                    )
        self.assertTrue(rv.status_code == 201)
        tecnico_url = rv.headers['Location']

        # register usuarios to classes
        rv, json = self.client.post('/api/v1.0/servicos/',
                                    data={'usuario': {'url': susan_url },
                                          'escala': {'url': administrativo_url },
                                          'data': "2012-01-11T11:08:12.144Z",
                                          'tipo': 1})
        self.assertTrue(rv.status_code == 201)
        susan_in_administrativo_url = rv.headers['Location']

        rv, json = self.client.post('/api/v1.0/servicos/',
                                    data={'usuario': {'url': david_url },
                                          'escala': {'url': administrativo_url },
                                          'data': "2012-01-13T11:08:12.144Z",
                                          'tipo': 0})
        self.assertTrue(rv.status_code == 201)
        david_in_administrativo_url = rv.headers['Location']

        # get registration
        rv, json = self.client.get(susan_in_administrativo_url)
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['usuario']['url'] == susan_url)
        self.assertTrue(json['escala']['url'] == administrativo_url)

        # get collection
        rv, json = self.client.get('/api/v1.0/servicos/')
        self.assertTrue(rv.status_code == 200)
        urls = [ servico['url'] for servico in json['objects'] ]
        self.assertTrue(susan_in_administrativo_url in urls)
        self.assertTrue(david_in_administrativo_url in urls)
        self.assertTrue(len(urls) == 2)

        # bad registrations
        rv,json = self.client.post('/api/v1.0/servicos/', data={})
        self.assertTrue(rv.status_code == 400)

        self.assertRaises(ValidationError, lambda:
            self.client.post('/api/v1.0/servicos/',
                             data={'usuario': {'url': david_url}}))

        self.assertRaises(ValidationError, lambda:
            self.client.post('/api/v1.0/servicos/',
                             data={'escala': {'url': administrativo_url}}))

        self.assertRaises(ValidationError, lambda:
            self.client.post('/api/v1.0/servicos/',
                                data={
                                    'usuario': {'url': david_url},
                                    'escala': {'url': 'bad-url'}
                                }
                            )
            )

        self.assertRaises(ValidationError, lambda:
            self.client.post('/api/v1.0/servicos/',
                             data={'usuario': {'url': david_url},
                                   'escala': {'url': administrativo_url + '1'}
                                    }
                             )
            )
        db.session.remove()

        # get classes from each student
        rv, json = self.client.get(susan_url)
        self.assertTrue(rv.status_code == 200)
        
        urls = [ servico['url'] for servico in json['servicos']]
        self.assertTrue(susan_in_administrativo_url in urls)
        self.assertTrue(len(urls) == 1)
        
        rv, json = self.client.get(david_url)
        self.assertTrue(rv.status_code == 200)
        
        urls = [servico['url'] for servico in json['servicos']]
        self.assertTrue(david_in_administrativo_url in urls)
        self.assertTrue(len(urls) == 1)
        
        # get usuarios for each class
        rv, json = self.client.get(administrativo_url)
        self.assertTrue(rv.status_code == 200)
        
        urls = [ servico['url'] for servico in json['servicos']]
        
        self.assertTrue(susan_in_administrativo_url in urls)
        self.assertTrue(david_in_administrativo_url in urls)
        self.assertTrue(len(urls) == 2)

        # unregister usuarios
        rv, json = self.client.delete(susan_in_administrativo_url)
        self.assertTrue(rv.status_code == 200)

        # get collection
        rv, json = self.client.get('/api/v1.0/servicos/')
        self.assertTrue(rv.status_code == 200)
        
        urls = [ servico['url'] for servico in json['objects']]
        
        self.assertFalse(susan_in_administrativo_url in urls)
        self.assertTrue(david_in_administrativo_url in urls)
        self.assertTrue(len(urls) == 1)

        # delete student
        rv, json = self.client.delete(david_url)
        self.assertTrue(rv.status_code == 200)

        # get collection
        rv, json = self.client.get('/api/v1.0/servicos/')
        
        urls = [ servico['url'] for servico in json['objects']]
        
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(len(urls) == 0)
    
    def afastamentos(self):
        # create new usuarios
        rv, json = self.client.post('/api/v1.0/usuarios/',
                                    data={
                                          'name': 'susan',
                                          'username':'susan',
                                          'nome_guerra':'susan',
                                          'especialidade':'3S',
                                          'posto':'SIN','email':'susan@',
                                          'saram':123,
                                          'data_promocao':"2016-03-28T00:00:00.0Z"
                                        }
                                   )
        self.assertTrue(rv.status_code == 201)
        susan_url = rv.headers['Location']

        rv, json = self.client.post('/api/v1.0/usuarios/',
                                    data={
                                          'name': 'david',
                                          'username':'david',
                                          'nome_guerra':'david',
                                          'especialidade':'1S',
                                          'posto':'SAD',
                                          'email':'david@',
                                          'saram':123,
                                          'data_promocao':"2016-03-28T00:00:00.0Z"
                                        }
                                   )
        self.assertTrue(rv.status_code == 201)
        david_url = rv.headers['Location']

        # register usuarios afastamentos
        rv, json = self.client.post('/api/v1.0/afastamentos/',
                                    data={'usuario': susan_url,
                                          'motivo': 'ferias',
                                          'data_inicio': '2012-01-11',
                                          'data_fim': '2012-01-15'})
        self.assertTrue(rv.status_code == 201)
        susan_ferias_url = rv.headers['Location']

        rv, json = self.client.post('/api/v1.0/afastamentos/',
                                    data={'usuario': david_url,
                                          'motivo': 'Junta Especial',
                                          'data_inicio': '2012-01-11',
                                          'data_fim': '2012-06-15'})
        self.assertTrue(rv.status_code == 201)
        david_junta_url = rv.headers['Location']

        # get afastamento
        rv, json = self.client.get(susan_ferias_url)
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['usuario'] == susan_url)
        self.assertTrue(json['motivo'] == 'ferias')
        self.assertTrue(json['data_inicio'] == '2012-01-11')
        self.assertTrue(json['data_fim'] == '2012-01-15')

        # get collection
        rv, json = self.client.get('/api/v1.0/afastamentos/')
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(susan_ferias_url in json['urls'])
        self.assertTrue(david_junta_url in json['urls'])
        self.assertTrue(len(json['urls']) == 2)

        # bad afastamento
        rv,json = self.client.post('/api/v1.0/afastamentos/', data={})
        self.assertTrue(rv.status_code == 400)

        self.assertRaises(ValidationError, lambda:
            self.client.post('/api/v1.0/afastamentos/',
                             data={'usuario': david_url}))

        self.assertRaises(ValidationError, lambda:
            self.client.post('/api/v1.0/afastamentos/',
                             data={'motivo': 'ferias'}))

        self.assertRaises(ValidationError, lambda:
            self.client.post('/api/v1.0/afastamentos/',
                             data={'data_inicio': '2011-10-14'}))

        self.assertRaises(ValidationError, lambda:
            self.client.post('/api/v1.0/afastamentos/',
                             data={'usuario': 'bad-url',
                                          'motivo': 'Junta Especial',
                                          'data_inicio': '2012-01-11',
                                          'data_fim': '2012-06-15'}))

        db.session.remove()

        # get afastamentos from each usuario
        rv, json = self.client.get(susan_url)
        self.assertTrue(rv.status_code == 200)
        susans_afastamento_url = json['afastamentos']
        rv, json = self.client.get(susans_afastamento_url)
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(susan_ferias_url in json['urls'])
        self.assertTrue(len(json['urls']) == 1)

        rv, json = self.client.get(david_url)
        self.assertTrue(rv.status_code == 200)
        davids_afastamento_url = json['afastamentos']
        rv, json = self.client.get(davids_afastamento_url)
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(david_junta_url in json['urls'])
        self.assertTrue(len(json['urls']) == 1)

        # unregister usuarios
        rv, json = self.client.delete(susan_ferias_url)
        self.assertTrue(rv.status_code == 200)

        # get collection
        rv, json = self.client.get('/api/v1.0/afastamentos/')
        self.assertTrue(rv.status_code == 200)
        self.assertFalse(susan_ferias_url in json['urls'])
        self.assertTrue(len(json['urls']) == 1)

        # delete student
        rv, json = self.client.delete(david_url)
        self.assertTrue(rv.status_code == 200)

        # get collection
        rv, json = self.client.get('/api/v1.0/afastamentos/')
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(len(json['urls']) == 0)
    
    #Ignored
    def test_rate_limits(self):
        self.app.config['USE_RATE_LIMITS'] = True

        rv, json = self.client.get('/api/v1.0/servicos/')
        self.assertTrue(rv.status_code == 200)
        self.assertTrue('X-RateLimit-Remaining' in rv.headers)
        self.assertTrue('X-RateLimit-Limit' in rv.headers)
        self.assertTrue('X-RateLimit-Reset' in rv.headers)
        self.assertTrue(int(rv.headers['X-RateLimit-Limit']) == int(rv.headers['X-RateLimit-Remaining']) + 1)
        while int(rv.headers['X-RateLimit-Remaining']) > 0:
            rv, json = self.client.get('/api/v1.0/servicos/')
        self.assertTrue(rv.status_code == 429)
    
    #Ignored
    def pagination(self):
        # create several usuarios
        rv, json = self.client.post('/api/v1.0/usuarios/',
                                    data={'name': 'one'})
        self.assertTrue(rv.status_code == 201)
        one_url = rv.headers['Location']
        rv, json = self.client.post('/api/v1.0/usuarios/',
                                    data={'name': 'two'})
        self.assertTrue(rv.status_code == 201)
        two_url = rv.headers['Location']
        rv, json = self.client.post('/api/v1.0/usuarios/',
                                    data={'name': 'three'})
        self.assertTrue(rv.status_code == 201)
        three_url = rv.headers['Location']
        rv, json = self.client.post('/api/v1.0/usuarios/',
                                    data={'name': 'four'})
        self.assertTrue(rv.status_code == 201)
        four_url = rv.headers['Location']
        rv, json = self.client.post('/api/v1.0/usuarios/',
                                    data={'name': 'five'})
        self.assertTrue(rv.status_code == 201)
        five_url = rv.headers['Location']

        # get collection in pages
        rv, json = self.client.get('/api/v1.0/usuarios/?page=1&per_page=2')
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(one_url in json['urls'])
        self.assertTrue(two_url in json['urls'])
        self.assertTrue(len(json['urls']) == 2)
        self.assertTrue('total' in json['meta'])
        self.assertTrue(json['meta']['total'] == 5)
        self.assertTrue('prev' in json['meta'])
        self.assertTrue(json['meta']['prev'] is None)
        first_url = json['meta']['first'].replace('http://localhost', '')
        last_url = json['meta']['last'].replace('http://localhost', '')
        next_url = json['meta']['next'].replace('http://localhost', '')

        rv, json = self.client.get(first_url)
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(one_url in json['urls'])
        self.assertTrue(two_url in json['urls'])
        self.assertTrue(len(json['urls']) == 2)

        rv, json = self.client.get(next_url)
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(three_url in json['urls'])
        self.assertTrue(four_url in json['urls'])
        self.assertTrue(len(json['urls']) == 2)
        next_url = json['meta']['next'].replace('http://localhost', '')

        rv, json = self.client.get(next_url)
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(five_url in json['urls'])
        self.assertTrue(len(json['urls']) == 1)

        rv, json = self.client.get(last_url)
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(five_url in json['urls'])
        self.assertTrue(len(json['urls']) == 1)

    #Ignored
    def cache_control(self):
        client = TestClient(self.app, self.default_username,
                            self.default_password)
        rv, json = client.get('/auth/request-token')
        self.assertTrue(rv.status_code == 200)
        self.assertTrue('Cache-Control' in rv.headers)
        cache = [c.strip() for c in rv.headers['Cache-Control'].sptecnico(',')]
        self.assertTrue('no-cache' in cache)
        self.assertTrue('no-store' in cache)
        self.assertTrue('max-age=0' in cache)
        self.assertTrue(len(cache) == 3)

    #Ignored
    def etag(self):
        # create two usuarios
        rv, json = self.client.post('/api/v1.0/usuarios/',
                                    data={'name': 'one'})
        self.assertTrue(rv.status_code == 201)
        one_url = rv.headers['Location']
        rv, json = self.client.post('/api/v1.0/usuarios/',
                                    data={'name': 'two'})
        self.assertTrue(rv.status_code == 201)
        two_url = rv.headers['Location']

        # get their etags
        rv, json = self.client.get(one_url)
        self.assertTrue(rv.status_code == 200)
        one_etag = rv.headers['ETag']
        rv, json = self.client.get(two_url)
        self.assertTrue(rv.status_code == 200)
        two_etag = rv.headers['ETag']

        # send If-None-Match header
        rv, json = self.client.get(one_url, headers={
            'If-None-Match': one_etag})
        self.assertTrue(rv.status_code == 304)
        rv, json = self.client.get(one_url, headers={
            'If-None-Match': one_etag + ', ' + two_etag})
        self.assertTrue(rv.status_code == 304)
        rv, json = self.client.get(one_url, headers={
            'If-None-Match': two_etag})
        self.assertTrue(rv.status_code == 200)
        rv, json = self.client.get(one_url, headers={
            'If-None-Match': two_etag + ', *'})
        self.assertTrue(rv.status_code == 304)

        # send If-Match header
        rv, json = self.client.get(one_url, headers={
            'If-Match': one_etag})
        self.assertTrue(rv.status_code == 200)
        rv, json = self.client.get(one_url, headers={
            'If-Match': one_etag + ', ' + two_etag})
        self.assertTrue(rv.status_code == 200)
        rv, json = self.client.get(one_url, headers={
            'If-Match': two_etag})
        self.assertTrue(rv.status_code == 412)
        rv, json = self.client.get(one_url, headers={
            'If-Match': '*'})
        self.assertTrue(rv.status_code == 200)

        # change a resource
        rv, json = self.client.put(one_url, data={'name': 'not-one'})
        self.assertTrue(rv.status_code == 200)

        # use stale etag
        rv, json = self.client.get(one_url, headers={
            'If-None-Match': one_etag})
        self.assertTrue(rv.status_code == 200)
