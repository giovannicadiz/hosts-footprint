#encoding=utf8

from __future__ import print_function
from django.core.management.base import BaseCommand, CommandError
from default.models import *
from django.db.utils import IntegrityError

import sys
import subprocess
from multiprocessing import Pool
import time

from multiprocessing import Manager
from threading import Thread, Lock
from datetime import date, datetime

from winmap_to_dict import analise_and_get_es_body, EstadoNaoDeterminado

# multiprocessing
# multithread

# make subnets
# sopport a nmap templates

# send result to elasticsearch


QUAN_NMAP_PROC = 4
QUAN_ANALISES_PROC = 8

nmapCommandTemplate = "nmap %s -P0 --open -p445 | grep ^'Nmap scan report'"

if '--debug' in sys.argv:
    winmapCommandTemplate = "./winmap2.sh '%s' '%s' '%s' '%s' '%s' '%s' '%s' '%s' '%s' | tail -n 2"
else:
    winmapCommandTemplate = "./winmap2.sh '%s' '%s' '%s' '%s' '%s' '%s' '%s' '%s' '%s' &> /dev/null"

es = Elasticsearch('http://localhost:9200')

INDEX = 'windows_clients_v2'

es_lock = Lock()

def sincronico():
    return shared_info['sync']

class Host:

    def __init__(self, host, ip, net):
        self.host = host
        self.ip = ip
        self.net = net

    def get_data(self):
        data = date.today()
        return datetime(data.year, data.month, data.day, 12)

    def get_id(self):
        return '%s-%s' % (self.host, str(date.today()))

    def analised(self):

        if shared_info['force']:
            return False
        with es_lock:
            exist = es.search( index=INDEX, q="""_id: "%s" """ % self.get_id())
        try:
            return ( exist['hits']['hits'][0]['_source']['status'] in [0, -1] )
        except:
            pass
        return False

    def index(self, body):

        body['descricao'] = self.net.description
        body['local'] = self.net.local.split('/')
        body['data'] = str(self.get_data())
        body['hostname'] = self.host
        body['ip'] = self.ip
        body['bandeira'] = self.net.bandeira
        #body['regional'] = self.net.regional
        body['lat_lon'] = { 'lat': self.net.lat, 'lon': self.net.lon }
        body['loja_critica'] = self.net.critica
        body['tipo_loja'] = self.net.tipo
        body['critica'] = self.net.critica

        with es_lock:
            es.index( index=INDEX, doc_type='status', id=self.get_id(),
                body=body )

    def analise(self):
        
        if self.analised():
            return

        try:

            body = analise_and_get_es_body(self.host)

            self.index(body)

        except EstadoNaoDeterminado as e:
            hosts_error_list.append(self.host)
            print(e)
        except:
            hosts_error_list.append(self.host)
            print(u'ERRO: Error não reconhecido ao processar o host %s.' % self.host)

    def __str__(self):
        return '%s [%s]' % (self.ip, self.host)

def analize_host(host_args):
    host, ip, net = host_args
    host_instance = Host(host, ip, net)
    print('analises: %s' % host_instance )
    host_instance.analise()

def get_nets_and_clear():
    result = []
    while len(nets_shared_lists) > 0:
        result.append(nets_shared_lists.pop())
    return result


def get_hosts_and_clear():
    result = []
    while len(hosts_shared_lists) > 0:
        result.append(hosts_shared_lists.pop())
    return result

def do_winmap():
    if sincronico():
        hosts_args = get_hosts_and_clear()
        for host_args in hosts_args:
            analize_host(host_args)
    else:
        pool = Pool(processes=QUAN_ANALISES_PROC)
        while not shared_info['finalizar'] or len(hosts_shared_lists) > 0:
            hosts_args = get_hosts_and_clear()
            if len(hosts_args) > 0:
                pool.map(analize_host, hosts_args )
            time.sleep(1)


def do_nmap(net):
    print('nmap: %s' % net)
    nmapCommand = nmapCommandTemplate % net.net
    try:
        lines = subprocess.check_output(nmapCommand, shell=True)  
    except:
        nets_error_list.append(net)
        print('ERRO: %s.' % nmapCommand)
        return

    for line in lines.decode().split('\n'):
        register = line.split(' ');
        if len(register) < 6:
            continue
        host = register[4]
        
        if not register[5]:
            continue

        ip = register[5].replace('(','').replace(')','');

        host_args = (host, ip, net)
        hosts_shared_lists.append( host_args )


def main(options):

    shared_info['finalizar'] = False
    shared_info['sync'] = options['sync']
    shared_info['force'] = options['force']
    #shared_info['command'] = self

    if len(options['net']) == 0:
        nets = Net.objects.all()
    else:
        nets = Net.objects.filter(net__in=options['net'])

    if options['err']:
        nets = nets.filter(processado_com_sucesso=False)

    base_nets = nets

    for net in nets:
        nets_shared_lists.append( net )

    if sincronico():
        for net in nets_shared_lists:
            do_nmap(net)
        do_winmap()
    else:
        t = Thread(target=do_winmap)
        t.start()

        pool = Pool(processes=QUAN_NMAP_PROC)
        while len(nets_shared_lists) > 0:
            nets = get_nets_and_clear()
            if len(nets) > 0:
                pool.map(do_nmap, nets)

        self.MP.shared_info['finalizar'] = True
        t.join()

    print('Listado de redes com erro:')
    nets_ids_error = []
    for x in nets_error_list:
        x.processado_com_sucesso = False
        x.quan_erros = x.quan_erros + 1
        x.save()
        nets_ids_error.append(x.id)
        print(x)
    for x in base_nets.exclude(id__in=nets_ids_error):
        x.processado_com_sucesso = True
        x.quan_sucessos = x.quan_sucessos + 1
        x.save()
    print('Listado de hosts com erro:')
    for x in hosts_error_list:
        print(x)


class Command(BaseCommand):
    help = 'Carrega redes desde arquivo separado por tabuladores.'

    def add_arguments(self, parser):
        parser.add_argument('net', nargs='*')
        parser.add_argument('--sync',
            action='store_true',
            dest='sync',
            default=False,
            help='Não cria threads.')
        parser.add_argument('--err',
            action='store_true',
            dest='err',
            default=False,
            help='Só processa redes que apresentaram erro.')
        parser.add_argument('--force',
            action='store_true',
            dest='force',
            default=False,
            help='Grava sempre em elastic search.')

    def handle(self, *args, **options):

        main(options)

manager = Manager()
hosts_shared_lists = manager.list([])
hosts_error_list = manager.list([])
nets_shared_lists = manager.list([])
nets_error_list = manager.list([])
shared_info = manager.dict()
