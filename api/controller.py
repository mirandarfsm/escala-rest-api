from models import db,Usuario,Escala,UsuarioEscala
from datetime import datetime

class UsuarioEscalaController(object):
    
    def modificar_lista_usuario(self,escala,lista_id_usuario):
        lista_usuario_escala = escala.usuarios.filter(UsuarioEscala.data_fim != None).all()
        lista_remocao = []
        for usuario_escala in lista_usuario_escala:
            id_usuario = usuario_escala.id_usuario
            if id_usuario not in lista_id_usuario:
                lista_remocao.apend(usuario_escala)
            if id_usuario in lista_id_usuario:
                lista_id_usuario.remove(id_usuario)
        self.remover_usuarios(lista_remocao)
        self.adicionar_usuarios(escala.id,lista_id_usuario)
    
    def adicionar_usuarios(self,id_escala,lista_id_usuario):
        for id_usuario in lista_id_usuario:
            self.add_usuario(id_escala,id_usuario)

    def add_usuario(self,id_escala,id_usuario):
        usuario_escala = UsuarioEscala.query.filter_by(id_escala = id_escala, id_usuario = id_usuario, data_fim = None)
        if not usuario_escala:
            escala = Escala.query.find_or_404(id_escala)
            usuario = Usuario.query.find_or_404(id_usuario)
            data = datetime.now()
            usuario_escala = UsuarioEscala(escala = escala,usuario = usuario,data_cadastro = data)
            db.session.add(usuario_escala)
            db.session.commit()
                    
    def remover_usuarios(self,list_remocao):
        for obj in list_remocao:
            self.remover_usuario(obj)
    
    def remover_usuario(self,usuario_escala):
        usuario_escala.data_fim = datetime.now()
        db.session.commit()