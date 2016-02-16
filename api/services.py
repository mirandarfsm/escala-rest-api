from models import db,TipoServico,Servico,Usuario,TipoEscala
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

class ServicoDiarioService(object):
    
    def get_first_last_mounth_day(self,year=datetime.date.today().year,month=datetime.date.today().month):
        first_day,last_day = calendar.monthrange(year,month)
        return (datetime.date(year,month,1),datetime.date(year,month,last_day))

    def gerar_lista_servico(self,end_date,escala,start_date=datetime.date.today()):
        feriados = escala.feriados
        roxas = escala.roxas
        d = start_date
        delta = datetime.timedelta(days=1)
        weekend = set([5,6])
        servicos = []
        while d <= end_date:
            tipo = TipoServico.PRETO
            if d.weekday() in weekend or d in feriados:
                tipo =  TipoServico.VERMELHO
            if d in roxas:
                tipo = TipoServico.ROXA
            servicos.append(Servico(data=d,tipo=tipo,escala_id=escala.id))
            d += delta
        return servicos
    
    def is_descanso(self,milico,date):
        for servico in milico.servicos:
            descanso_start = servico.data - datetime.timedelta(days=2)
            descanso_end = servico.data + datetime.timedelta(days=2)
            if descanso_start <= date <= descanso_end:
                return True
        return False

    def is_afastado(self,milico,date):
        for afastamento in milico.afastamentos:
            if afastamento.data_inicio <= date <= afastamento.data_fim:
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
        milicos = escala.usuarios.all()
        hash = {}
        hash[TipoServico.VERMELHO] = sorted(milicos,key=Usuario.by_vermelha_key)
        hash[TipoServico.PRETO] = sorted(milicos,key=Usuario.by_preta_key)
        hash[TipoServico.ROXA] = sorted(milicos,key=Usuario.by_roxa_key)
        date = get_next_month(datetime.date.today())
        start_date,last_date = self.get_first_last_mounth_day(date.year,date.month)
        servicos = self.gerar_lista_servico(last_date,escala,start_date)
        for servico in servicos:
            milico = self.get_next_military(hash[servico.tipo],servico)
            milico.servicos.append(servico)
            db.session.commit()
        return milicos

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