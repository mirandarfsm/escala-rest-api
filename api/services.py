
#from models import TipoServico
import datetime
import calendar

class TipoServico:
    PRETO = 1
    VERMELHO = 2
    ROXA = 3

class Afastamento(object):

    def __init__(self,motivo,start_date,end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.motivo = motivo

    def __repr__(self):
        return repr((self.motivo,str(self.start_date),str(self.end_date)))

class Milico(object):

    def __init__(self,nome,antiguidade,servicos,afastamentos):
        self.nome = nome
        self.antiguidade = antiguidade
        self.servicos = servicos
        self.afastamentos = afastamentos

    def __repr__(self):
        return repr((self.nome,self.antiguidade,len(self.servicos)))

    def vermelhas(self):
        return [servico for servico in self.servicos if servico.tipo == TipoServico.VERMELHO]

    def pretas(self):
        return [servico for servico in self.servicos if servico.tipo == TipoServico.PRETO]
    
    def roxas(self):
        return [servico for servico in self.servicos if servico.tipo == TipoServico.ROXA]

    def by_vermelha_key(milico):
        servicos = milico.vermelhas()
        total = 0
        if len(servicos) > 0:
            total += reduce(lambda x,y: x*y*3,map(lambda x: x.date.year * x.date.month * x.date.day*3,servicos))
        total += milico.antiguidade
        return total
        
    def by_preta_key(milico):
        servicos = milico.pretas()
        total = 0
        if len(servicos) > 0:
            total += reduce(lambda x,y: x*y*3,map(lambda x: x.date.year * x.date.month * x.date.day*3,servicos))
        total += milico.antiguidade
        return total
     
    def by_roxa_key(milico):
        servicos = milico.roxas()
        total = 0
        if len(servicos) > 0:
            total += reduce(lambda x,y: x*y*3,map(lambda x: x.date.year * x.date.month * x.date.day*3,servicos))
        total += milico.antiguidade
        return total

class Servico(object):
    def __init__(self,date,tipo):
        self.date = date
        self.tipo = tipo

    def __repr__(self):
        return repr((self.tipo,str(self.date)))

    def __cmp__(self,other):
        return self.date.__cmp__(other.date)

def get_last_mounth_day(year=datetime.date.today().year,month=datetime.date.today().month):
    last_day = calendar.monthrange(year,month)[1]
    return datetime.date(year,month,last_day)

def gerar_lista_servico(end_date,feriados,roxas,start_date=datetime.date.today()):
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
        servicos.append(Servico(d,tipo))
        d += delta
    return servicos

def is_descanso(milico,date):
    if len(milico.servicos) == 0:
        return False
    last_service = milico.servicos[-1].date
    descanso = last_service + datetime.timedelta(days=2)
    if last_service <= date <= descanso:
        return True
    return False

def is_afastado(milico,date):
    for afastamento in milico.afastamentos:
        if afastamento.start_date <= date <= afastamento.end_date:
            return True     
    return False

def get_next_military(milicos,servico,escala=None):
    if servico.tipo == TipoServico.VERMELHO:
        key = Milico.by_vermelha_key
    if servico.tipo == TipoServico.PRETO:
        key = Milico.by_preta_key
    if servico.tipo == TipoServico.ROXA:
        key = Milico.by_roxa_key

    milicos_sorted = sorted(milicos,key=key)
    for milico in milicos_sorted:
        if not is_afastado(milico,servico.date):
            if not is_descanso(milico,servico.date):
                return milico
    raise Exception("Nao existe militares para serem escalados na data: "+ str(servico.date))

def gerar_lista_militares_escalados(milicos):
    start_date = datetime.date(2015,12,01)
    last_date = get_last_mounth_day(2015,12)
    servicos = gerar_lista_servico(last_date,[],[],start_date)

    for servico in servicos:
        milico = get_next_military(milicos,servico)
        milico.servicos.append(servico)
    return milicos

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

milicos = [
            Milico('renato',1,[],[]),
            Milico('robson',2,[],[]),
            Milico('souza',3,[],[]),
            Milico('fernando',4,[],[]), 
            Milico('augusto',5,[],[]), 
            Milico('miranda',6,[],[]), 
            Milico('santos',7,[],[]),
            Milico('lopes',8,[],[]), 
            Milico('silva',9,[],[]), 
            Milico('paula',10,[],[]), 
            Milico('ornelas',11,[],[]), 
            Milico('oliveira',12,[],[]), 
            Milico('sardela',13,[],[]),
            Milico('duda',14,[],[]),
            Milico('pai',15,[],[Afastamento("junta",datetime.date.today(),datetime.date.today() + datetime.timedelta(days=10))])
        ]

escalados = gerar_lista_militares_escalados(milicos)

print milicos_to_string(escalados)
