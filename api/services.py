
from models import db,TipoServico,Servico,Usuario
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
    return (datetime.date(year,month,first_day),datetime.date(year,month,last_day))

def gerar_lista_servico(end_date,escala,start_date=datetime.date.today()):
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

def get_next_military(milicos,servico):
    if servico.tipo == TipoServico.VERMELHO:
        key = Usuario.by_vermelha_key
    if servico.tipo == TipoServico.PRETO:
        key = Usuario.by_preta_key
    if servico.tipo == TipoServico.ROXA:
        key = Usuario.by_roxa_key
    print key
    milicos_sorted = sorted(milicos,key=key)
    print milicos_sorted
    for milico in milicos_sorted:
        if not is_afastado(milico,servico.data):
            if not is_descanso(milico,servico.data):
                return milico
    raise Exception("Nao existe militares para serem escalados na data: "+ str(servico.data))

def gerar_lista_militares_escalados(escala):
    milicos = escala.usuarios
    today = get_next_month(datetime.date.today())
    start_date,last_date = get_first_last_mounth_day(today.year,today.month)
    servicos = gerar_lista_servico(last_date,escala,start_date)
    for servico in servicos:
        milico = get_next_military(milicos,servico)
        milico.servicos.append(servico)
        db.session.add(milico)
        db.session.commit()
    return milico

'''
def milicos_to_string(milicos):
    text = "--------------------------------------------------------------\n"
    soma = 0
    vermelhas = 0
    pretas = 0
    roxas = 0
    for milico in milicos:
        soma += len(milico.pretas())+len(milico.vermelhas())+len(milico.roxas())
        pretas += len(milico.pretas())
        vermelhas += len(milico.vermelhas())
        roxas += len(milico.roxas())
        text += "nome: %s\n" % milico.nome
        text += "escalas: %s\n" % milico.escalas
        text += "servicos preta: %s\n" % len(milico.pretas())
        text += "servicos vermelha: %s\n" % len(milico.vermelhas())
        text += "servicos roxa: %s\n" % len(milico.roxas())
        text += "dias servicos preta: %s\n" %milico.pretas() 
        text += "dias servicos vermelha: %s\n" %milico.vermelhas()
        text += "dias servicos roxa: %s\n" %milico.roxas()
        text += "----------------------------------------------------------\n"
    text += "Soma total %s\n" %soma
    text += "Soma total pretas %s\n" %pretas
    text += "Soma total vermelhas %s\n" %vermelhas
    text += "Soma total roxas %s\n" %roxas
    return text

ccasj = Escala("admin")
brejau = Escala("brejau")

renato = Milico('renato',1,[],[],[ccasj,brejau])
robson = Milico('robson',2,[],[],[ccasj,brejau])
souza = Milico('souza',3,[],[],[ccasj,brejau])
fernando = Milico('fernando',4,[],[],[ccasj,brejau])
augusto = Milico('augusto',5,[],[],[ccasj,brejau])
miranda = Milico('miranda',6,[],[],[ccasj,brejau]) 
santos = Milico('santos',7,[],[],[ccasj,brejau])
lopes = Milico('lopes',8,[],[],[ccasj,brejau]) 
silva = Milico('silva',9,[],[],[ccasj,brejau]) 
paula = Milico('paula',10,[],[],[ccasj,brejau]) 
ornelas = Milico('ornelas',11,[],[],[ccasj,brejau]) 
oliveira = Milico('oliveira',12,[],[],[ccasj,brejau]) 
sardela = Milico('sardela',13,[],[],[ccasj,brejau])
duda = Milico('duda',14,[],[],[ccasj,brejau])
pai = Milico('pai',15,[],[Afastamento("junta",datetime.date.today(),datetime.date.today() + datetime.timedelta(days=10))],[ccasj,brejau])
milicos = [ 
            renato,
            robson,
            souza,
            fernando,
            augusto,
            miranda,
            santos,
            lopes,
            silva,
            paula,
            ornelas,
            oliveira, 
            sardela,
            duda,
            pai
        ]
milicos2 = [ 
            renato,
            robson,
            souza,
            fernando,
            augusto,
            paula,
            ornelas,
            oliveira, 
            sardela,
            duda,
            pai
        ]


gerar_lista_militares_escalados(milicos,ccasj)
gerar_lista_militares_escalados(milicos2,brejau)
print milicos_to_string(milicos)
'''