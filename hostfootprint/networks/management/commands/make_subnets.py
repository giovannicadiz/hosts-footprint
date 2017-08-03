#encoding=utf8

## git
## sacar els
## add lock to check index
## sacar 2 consulta DB

import sys
#from __future__ import print_function
from django.core.management.base import BaseCommand, CommandError
from networks.models import *

import sys, time
from multiprocessing import Manager
from multiprocessing.pool import ThreadPool
from threading import Thread, Lock

import ipaddress, nmap

#from elasticsearch import Elasticsearch,helpers

index='nmap'

#es_lock = Lock()
es = ElsSaveMap(index)

## ELASTICSEARCH index

NMAPPROCS=4
# windows = 'windows'
# linux = 'linux'


def syncronic():
    return shared_info['sync']


def get_nets_and_clear():
    result = []
    while len(nets_shared_lists) > 0:
        result.append(nets_shared_lists.pop())
    return result


#def do_es():
#    if sincronico():
#        hosts_args = get_hosts_and_clear()
#        for host_args in hosts_args:
#            es.es_save( host_args[0], host_args[1], host_args[2] )
#    else:
#        pool = Pool(processes=QUAN_ANALISES_PROC)
#        while not shared_info['finalizar'] or len(hosts_shared_lists) > 0:
#            hosts_args = get_hosts_and_clear()
#            if len(hosts_args) > 0:
#                pool.map(analize_host, hosts_args )
#            time.sleep(1)



# nmap
def scan_net( subnet_object ):
    nm = nmap.PortScanner()
    nm.scan(
        hosts=subnet_object['net'],
        ports="445",
        arguments="-P0 -n --open"
    )

    hosts_map = {
        '445': [],
        '22': []
    }

    for host in nm.all_hosts():
        if nm[host].has_tcp(445) is True:
            hosts_map['445'].append(host)
        if nm[host].has_tcp(22) is True:
            hosts_map['22'].append(host)

    if len(hosts_map['445']) > 0:
        for host in hosts_map['445']:

            es_obj = ('windows', host, subnet_object['netobject'])

            #hosts_shared_lists.append( es_obj )
            #with es_lock:
            es_save('windows', host, subnet_object['netobject'])
            
    if len(hosts_map['22']) > 0:
        for host in hosts_map['22']:
            #with es_lock:
            es.es_save('linux', host, subnet_object['netobject'])
            
def main(options):

    shared_info['finalizar'] = False
    shared_info['sync'] = options['sync']
    #shared_info['force'] = options['force']

    if 'all' in options.keys():
        netobject = Network.objects.all()
    else:
        netobject = Network.objects.filter(network = options['net'])

    if len(netobject) == 0:
        print('net failed')
        sys.exit(2)
    else:
        sub_net = CreateSubNetworks()
        for i in netobject:
            list_sub_net = sub_net.make_subnetworks(i)
            for net in list_sub_net:
                nets_shared_lists.append( {
                    'net': str(net),
                    'netobject': i
                    }
                )

        if syncronic():
            for net in nets_shared_lists:
                scan_net( net )
        else:
            #t = Thread(target=do_es)
            #t.start()

            pool = ThreadPool(processes=NMAPPROCS)
            while len(nets_shared_lists) > 0:
                nets = get_nets_and_clear()
            if len(nets) > 0:
                pool.map(scan_net, nets)
            #pool.close()
        shared_info['finalizar'] = True
       #t.join()


class Command(BaseCommand):
    help = 'make subnets from networks'
    def add_arguments(self, parser):
        parser.add_argument('--sync',
            action='store_true',
            dest='sync',
            default=False,
            help='Dont generate threads.')
        parser.add_argument('-n', '--net', required=False, \
                            help=u'network address')
        parser.add_argument('-a', '--all', required=False, \
                            help=u'all networks')
        
    def handle(self, *args, **options):
        main(options)

manager = Manager()
hosts_shared_lists = manager.list([])
hosts_error_list = manager.list([])
nets_shared_lists = manager.list([])
shared_info = manager.dict()
