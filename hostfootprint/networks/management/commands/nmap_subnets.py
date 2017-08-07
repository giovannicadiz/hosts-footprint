#encoding=utf8

## git - OK
## sacar els
## add lock to check index
## sacar 2 consulta DB

import sys
#from __future__ import print_function
from django.core.management.base import BaseCommand, CommandError
from networks.models import *
from django.db.utils import IntegrityError


from django import db

import sys, time
from multiprocessing import Manager
#from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
from threading import Thread, Lock

import ipaddress, nmap

#from elasticsearch import Elasticsearch,helpers

index='nmap'

#es_lock = Lock()
es = ElsSaveMap(index, index)

## ELASTICSEARCH index

NMAPPROCS=100
HOSTSPROCS=10
# windows = 'windows'
# linux = 'linux'


def syncronic():
    return shared_info['sync']

def get_hosts_and_clear():
    result = []
    while len(hosts_shared_lists) > 0:
        result.append(hosts_shared_lists.pop())
    return(result)

def get_nets_and_clear():
    result = []
    while len(nets_shared_lists) > 0:
        result.append(nets_shared_lists.pop())
    return(result)

def print_host(host_args):
    es.es_save(*host_args)


def do_print():
    if syncronic():
        hosts_args = get_hosts_and_clear()
        for host_args in hosts_args:
            print( host_args )
            #es.es_save( host_args[0], host_args[1], host_args[2] )
    else:
        pool = ThreadPool(processes=HOSTSPROCS)
        while not shared_info['finalizar'] or len(hosts_shared_lists) > 0:
            hosts_args = get_hosts_and_clear()
            if len(hosts_args) > 0:
                pool.map(print_host, hosts_args )
            time.sleep(1)

# nmap
def scan_net( subnet_object ):
    print( subnet_object['net'] )
    nm = nmap.PortScanner()
    nm.scan(
        hosts=subnet_object['net'],
        ports="445,22",
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
            es_windows = ('windows', host, subnet_object['netobject'])
            hosts_shared_lists.append( es_windows )
            #with es_lock:

            
    if len(hosts_map['22']) > 0:
        for host in hosts_map['22']:
            es_linux = ('linux', host, subnet_object['netobject'])
            hosts_shared_lists.append( es_linux )
            
def main(options):

    shared_info['finalizar'] = False
    shared_info['sync'] = options['sync']
    #shared_info['force'] = options['force']

    if 'all' in options.keys():
        netobject = Network.objects.all()
    else:
        netobject = Network.objects.filter(network = options['net'])

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
        t = Thread(target=do_print)
        t.start()

        pool = ThreadPool(processes=NMAPPROCS)
        while len(nets_shared_lists) > 0:
            nets = get_nets_and_clear()
        if len(nets) > 0:
            pool.map(scan_net, nets)
            #pool.close()
            #pool.join()
            
        shared_info['finalizar'] = True
        t.join()
        db.connections.close_all()

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
