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

def get_first_last_mounth_day(year=datetime.date.today().year,month=datetime.date.today().month):
    first_day,last_day = calendar.monthrange(year,month)
    return (datetime.date(year,month,1),datetime.date(year,month,last_day))

def gerar_lista_servico_diario(end_date,escala,start_date=datetime.date.today()):
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

def gerar_lista_servico_semanal(year,month,escala):
    roxas = escala.roxas
    servicos = []
    dates = calendar.monthcalendar(year, month)
    for d in dates:
        day = d[calendar.MONDAY]
        if day != 0:
            date = datetime.date(year,month,day)
            servicos.append(Servico(data=date,tipo=TipoServico.PRETO,escala_id=escala.id))
    return servicos

def is_descanso_semanal(milico,date):
    for servico in milico.servicos:
        descanso_start = servico.data.isocalendar()[1]-1
        descanso_end = servico.data.isocalendar()[1]+1
        if descanso_start <= date.isocalendar()[1] <= descanso_end:
            return True
    return False

def is_afastado_semanal(milico,date):
    for afastamento in milico.afastamentos:
        if afastamento.data_inicio.isocalendar()[1] <= date.isocalendar()[1] <= afastamento.data_fim.isocalendar()[1]:
            return True     
    return False

def is_descanso(milico,date):
    for servico in milico.servicos:
        descanso_start = servico.data - datetime.timedelta(days=2)
        descanso_end = servico.data + datetime.timedelta(days=2)
        if descanso_start <= date <= descanso_end:
            return True
    return False

def is_afastado(milico,date):
    for afastamento in milico.afastamentos:
        if afastamento.data_inicio <= date <= afastamento.data_fim:
            return True     
    return False

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

def get_next_military(militares,servico):
    for i in range(len(militares)):
        militar = militares[0]
        if not is_afastado(militar,servico.data):
            if not is_descanso(militar,servico.data):
                militares.pop(0)
                militares.append(militar)
                return militar
        militares[0] = militares[i+1]
        militares[i+1] = militar
    raise Exception("Nao existe militares para serem escalados na data: "+ str(servico.data))


def get_next_military_semanal(militares,servico):
    for i in range(len(militares)):
        militar = militares[0]
        if not is_afastado_semanal(militar,servico.data):
            if not is_descanso_semanal(militar,servico.data):
                militares.pop(0)
                militares.append(militar)
                return militar
        militares[0] = militares[i+1]
        militares[i+1] = militar
    raise Exception("Nao existe militares para serem escalados na data: "+ str(servico.data))

def gerar_lista_militares_escalados(escala):
    milicos = escala.usuarios.all()
    lista_militares_vermelhas = sorted(milicos,key=Usuario.by_vermelha_key)
    lista_militares_pretas = sorted(milicos,key=Usuario.by_preta_key)
    lista_militares_roxas = sorted(milicos,key=Usuario.by_preta_key)
    date = get_next_month(datetime.date.today())
    if escala.tipo == TipoEscala.DIARIA:
        start_date,last_date = get_first_last_mounth_day(date.year,date.month)
        servicos = gerar_lista_servico_diario(last_date,escala,start_date)
        get_militar = get_next_military
    else:
        servicos = gerar_lista_servico_semanal(date.year,date.month,escala)
        get_militar = get_next_military_semanal
    for servico in servicos:
        if servico.tipo == TipoServico.PRETO:
            milico = get_militar(lista_militares_pretas,servico)
            milico.servicos.append(servico)
        elif servico.tipo == TipoServico.VERMELHO:
            milico = get_militar(lista_militares_vermelhas,servico)
            milico.servicos.append(servico)
        else:
            milico = get_militar(lista_militares_roxas,servico)
            milico.servicos.append(servico)
        db.session.commit()
    return milicos