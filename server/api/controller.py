from .models import db,Usuario,Escala,UsuarioEscala,Servico
from datetime import datetime

class AfastamentoController(object):
    
    def verificar_usuario_tem_servico(self,afastamento):
        usuario = afastamento.usuario
        servico = Servico.query.join(UsuarioEscala).join(Usuario) \
                .filter(Servico.data.between(afastamento.data_inicio,afastamento.data_fim)) \
                .filter(Usuario.id == usuario.id).first()
        if servico:
            raise Exception("Usuario ja esta de servico. ")


class UsuarioEscalaController(object):
    
    def modificar_lista_usuario(self,escala,lista_id_usuario):
        lista_usuario_escala_ativas = escala.usuarios.filter(UsuarioEscala.data_fim == None).all()
        lista_remocao = []
        for usuario_escala in lista_usuario_escala_ativas:
            id_usuario = usuario_escala.id_usuario
            if id_usuario not in lista_id_usuario:
                lista_remocao.append(usuario_escala)
            if id_usuario in lista_id_usuario:
                lista_id_usuario.remove(id_usuario)
        self.remover_usuarios_de_escala(lista_remocao)
        self.adicionar_usuarios_in_escala(escala.id,lista_id_usuario)
    
    def adicionar_usuarios_in_escala(self,id_escala,lista_id_usuario):
        for id_usuario in lista_id_usuario:
            self.adicioar_usuario_escala(id_escala,id_usuario)

    def adicioar_usuario_escala(self,id_escala,id_usuario):
        usuario_escala = UsuarioEscala.query.filter_by(id_escala = id_escala, id_usuario = id_usuario, data_fim = None).first()
        if not usuario_escala:
            escala = Escala.query.get_or_404(id_escala)
            usuario = Usuario.query.get_or_404(id_usuario)
            data = datetime.now()
            usuario_escala = UsuarioEscala(escala = escala,usuario = usuario,data_cadastro = data)
            db.session.add(usuario_escala)
            db.session.commit()
                    
    def remover_usuarios_de_escala(self,list_remocao):
        for obj in list_remocao:
            self.remover_usuario_escala(obj)
    
    def remover_usuario_escala(self,usuario_escala):
        usuario_escala.data_fim = datetime.now()
        db.session.commit()
    
    def remover_usuario_de_escalas(self,usuario):
        lista_usuario_escala_ativas = usuario.escalas.filter(UsuarioEscala.data_fim == None).all()
        for usuario_escala in lista_usuario_escala_ativas:
            self.remover_usuario_escala(usuario_escala)
    
    def remover_escala_de_usuarios(self,escala):
        lista_usuario_escala_ativas = escala.usuarios.filter(UsuarioEscala.data_fim == None).all()
        for usuario_escala in lista_usuario_escala_ativas:
            self.remover_usuario_escala(usuario_escala)
        