from models import db,TipoServico,Servico,Usuario,TipoEscala,Afastamento,UsuarioEscala,Escala
import datetime
import calendar

#dateutil
def get_next_month(date):
    month = date.month+1
    year = date.year
    day = date.day
    if month > 12:
        month = month%12
        year += 1
    return datetime.date(year, month, day)

def fazer_trocar_servico(troca_servico,substituto):
    servico = troca_servico.servico
    hash = {}
    hash[TipoEscala.DIARIA] = ServicoDiarioService()
    hash[TipoEscala.SEMANAL] = ServicoDiarioService()
    if hash[servico.escala.tipo].is_descanso(substituto,servico.data) or hash[servico.escala.tipo].is_afastado(substituto,servico.data):
        raise Exception("Militar %s nao pode assumir servico por estar de descanco ou afastado"%(substituto.nome_guerra))
    troca_servico.substituto = substituto
    troca_servico.data = datetime.datetime.now()
    servico = Servico.query.get(troca_servico.servico.id)
    servico.usuario = troca_servico.substituto
    db.session.commit()
    
def is_servico_exists(servico,escala):
    exist = Servico.query.join(UsuarioEscala).join(Escala) \
                .filter(Escala.id == escala.id) \
                .filter(Servico.data == servico.data).first()
    if exist:
        raise Exception("Servico existe no banco de dados")
    return False

class ServicoDiarioService(object):
    
    def get_first_last_mounth_day(self,year=datetime.date.today().year,month=datetime.date.today().month):
        first_day,last_day = calendar.monthrange(year,month)
        return (datetime.date(year,month,1),datetime.date(year,month,last_day))

    def gerar_lista_servico(self,end_date,escala,start_date=datetime.date.today()):
        datas_vermelhas = escala.get_datas_vermelhas()
        datas_roxas = escala.get_datas_roxas()
        d = start_date
        delta = datetime.timedelta(days=1)
        weekend = set([4,5,6])
        servicos = []
        jump = False
        while d <= end_date:
            if d in datas_roxas:
                tipo = TipoServico.ROXA
                jump = True
            elif d.weekday() in weekend or d in datas_vermelhas:
                if jump:
                    d += delta
                    continue
                tipo =  TipoServico.VERMELHO
                jump = True
            else:
                tipo = TipoServico.PRETO    
            servico = Servico(data=d,tipo=tipo)
            print servico
            is_servico_exists(servico,escala)
            servicos.append(servico)
            if servico.tipo == TipoServico.PRETO:
                jump = False
            d += delta
        return servicos
    
    def is_descanso(self,usuario_escala,data):
        data_inicio = data - datetime.timedelta(days=2)
        data_fim = data + datetime.timedelta(days=2)
        servico = usuario_escala.servicos.filter(Servico.data.between(data_inicio,data_fim)).first()
        if servico:
                return True
        return False

    def is_afastado(self,usuario,date):
        afastamento = usuario.afastamentos.filter(Afastamento.ativo == True) \
                            .filter(Afastamento.data_revisao is not None) \
                            .filter(Afastamento.data_inicio <= date, Afastamento.data_fim >= date).first()
        if afastamento:
            return True     
        return False

    def get_next_military(self,lista_usuario_escala,servico):
        for i in range(len(lista_usuario_escala)):
            usuario_escala = lista_usuario_escala[0]
            if not self.is_afastado(usuario_escala.usuario,servico.data):
                if not self.is_descanso(usuario_escala,servico.data):
                    lista_usuario_escala.pop(0)
                    lista_usuario_escala.append(usuario_escala)
                    return usuario_escala
            lista_usuario_escala[0] = lista_usuario_escala[i+1]
            lista_usuario_escala[i+1] = usuario_escala
        raise Exception("Nao existem militares para serem escalados na data: "+ str(servico.data))

    
    def gerar_lista_militares_escalados(self,escala):
        lista_usuario_escala = escala.usuarios.all()
        if not lista_usuario_escala:
            raise Exception("Nao existem militares cadastrado na escala")
        hash = {}
        hash[TipoServico.VERMELHO] = sorted(lista_usuario_escala,key=UsuarioEscala.by_vermelha_key)
        hash[TipoServico.PRETO] = sorted(lista_usuario_escala,key=UsuarioEscala.by_preta_key)
        hash[TipoServico.ROXA] = sorted(lista_usuario_escala,key=UsuarioEscala.by_roxa_key)
        date = get_next_month(datetime.date.today())
        start_date,last_date = self.get_first_last_mounth_day(date.year,date.month)
        servicos = self.gerar_lista_servico(last_date,escala,start_date)
        for servico in servicos:
            usuario_escala = self.get_next_military(hash[servico.tipo],servico)
            servico.id_usuario_escala = usuario_escala.id
            db.session.add(servico)
            db.session.commit()
        return lista_usuario_escala

class ServicoSemanalService(object):
    
    def gerar_lista_servico(self,year,month,escala):
        roxas = [roxa.isocalendar()[1] for roxa in escala.roxas]
        servicos = []
        dates = calendar.monthcalendar(year, month)
        for d in dates:
            tipo = TipoServico.PRETO
            day = d[calendar.MONDAY]
            if day != 0:
                date = datetime.date(year,month,day)
                if date.isocalendar()[1] in roxas:
                    tipo = TipoServico.ROXA
                servicos.append(Servico(data=date,tipo=tipo,escala_id=escala.id))
        return servicos

    def is_descanso(self,militar,date):
        for servico in militar.servicos:
            descanso_start = servico.data.isocalendar()[1]-1
            descanso_end = servico.data.isocalendar()[1]+1
            if descanso_start <= date.isocalendar()[1] <= descanso_end:
                return True
        return False

    def is_afastado(self,militar,date):
        for afastamento in militar.afastamentos:
            if afastamento.data_inicio.isocalendar()[1] <= date.isocalendar()[1] <= afastamento.data_fim.isocalendar()[1]:
                return True     
        return False
    
    def get_next_military(self,militares,servico):
        for i in range(len(militares)):
            militar = militares[0]
            if not self.is_afastado(militar,servico.data):
                if not self.is_descanso(militar,servico.data):
                    militares.pop(0)
                    militares.append(militar)
                    return militar
            militares[0] = militares[i+1]
            militares[i+1] = militar
        raise Exception("Nao existe militares para serem escalados na data: "+ str(servico.data))

    def gerar_lista_militares_escalados(self,escala):
        militares = escala.usuarios.all()
        hash = {}
        hash[TipoServico.PRETO] = sorted(militares,key=Usuario.by_preta_key)
        hash[TipoServico.ROXA] = sorted(militares,key=Usuario.by_roxa_key)
        date = get_next_month(datetime.date.today())
        servicos = self.gerar_lista_servico(date.year,date.month,escala)
        for servico in servicos:
            militar = self.get_next_military(hash[servico.tipo],servico)
            militar.servicos.append(servico)
            db.session.commit()
        return militares


def get_next_military_old(milicos,servico):
    if servico.tipo == TipoServico.VERMELHO:
        key = Usuario.by_vermelha_key
    if servico.tipo == TipoServico.PRETO:
        key = Usuario.by_preta_key
    if servico.tipo == TipoServico.ROXA:
        key = Usuario.by_roxa_key
    print key
    milicos_sorted = sorted(milicos,key=key)
    for milico in milicos_sorted:
        if not is_afastado(milico,servico.data):
            if not is_descanso(milico,servico.data):
                return milico
    raise Exception("Nao existe militares para serem escalados na data: "+ str(servico.data))