#!/usr/bin/env python3

import sys, time
from multiprocessing import Manager
#from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
from threading import Thread, Lock

from elasticsearch import Elasticsearch

from subprocess import STDOUT, CalledProcessError, check_output as qx
import subprocess, sys, json, re
from datetime import datetime

class EstadoNaoDeterminado(Exception):
    pass

settings = open('settings.txt').readlines()
user = settings[0].replace('\n', '')
es_server = settings[1].replace('\n', '')

es = Elasticsearch( hosts=[ es_server ])
INDEX = 'nmap'
MAP_TYPE = 'windows'
PROCS=12
WINEXEPROCS=6

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

def do_winexe():

    pool = ThreadPool(processes=WINEXEPROCS)
    while not shared_info['finalizar'] or len(hosts_shared_lists) > 0:
        hosts_args = get_hosts_and_clear()
        if len(hosts_args) > 0:
            pool.map(time_execution, hosts_args )
        time.sleep(1)

def winmap_xp(user, host, timeout=30):

    winmap_xp_command = ['./winmap_xp.sh', \
                         user, host, DOMAIN, timeout]
    try:
        #print (smbclient_command[0:-1])
        output = qx(winmap_xp_command[0:-1], timeout=winmap_xp_command[-1])
        err = [3]

        if DOMAIN in str(output):
            output = output.decode()
            output = output.replace('\n', '')
            output = output.split('|')
            result = [ 0 ] + output

    except CalledProcessError as time_err:
        result = (2, time_err.output, time_err.returncode,  )
        #print(err)

    except subprocess.TimeoutExpired as timeout:
        result = ( 1, timeout.output, timeout.timeout, timeout.stderr )

    return(result)


def time_execution(host, timeout=30):

    command = 'cmd /c c:\Temp\winmap.bat'
    
    winexe_command = ['winexe', '-U', user, str('//' + host['_source']['ip']), command, timeout]

    try:
        print (winexe_command[0:-1])
        output = qx(winexe_command[0:-1], timeout=winexe_command[-1])
        result = (output.decode("utf-8",errors='ignore'))
        result = result.split('\n')

    except CalledProcessError as time_err:
        result = ( time_err.returncode, str(time_err.output), str(time_err.stderr) )

    except subprocess.TimeoutExpired as timeout:
        result = ( 1, str(timeout.output), str(timeout.timeout), str(timeout.stderr) )

        
    if result[0] == 241:
        result = winmap_xp(user, host['_source']['ip'])

    update_es_winexe(host['_id'], result)
        
def update_es_winexe(_id, winexe):

    if 'Caption' not in winexe:
        parsed = -1
    else:
        parsed = 1

    _id = _id
    winmap_dict = {
        'parsed': parsed
    }

    for i in winexe:
        try:
            i = str(i).replace('\r', '')
        except AttributeError:
            continue
        try:
            kv = i.split('=')
            winmap_dict[kv[0]] = kv[1]
        except:
            pass
            #print('value fail on %s: %s' % ( _id, i ) )
        
    # :-)
    body = {
        "doc": winmap_dict
    }

    print(body)
    try:
        response = es.update(
            index=INDEX,
            doc_type=INDEX,
            id=_id,
            body=body
        )
        print(response)
    except:
        print("fail: %s" % _id)


def smbclient(host, timeout=20):

    smbclient_command = ['./smbclient.sh', \
                         user, host['_source']['ip'], timeout]

    try:
        output = qx(smbclient_command[0:-1], timeout=smbclient_command[-1])
        end = [0 , 0, 'NV' ]
        if 'Windows 5.1' in str(output):
            end = [ 0, 0, 'Windows XP' ]
            
    except CalledProcessError as time_err:
        end = [ 0, 2, time_err.output, time_err.returncode ]
        if "TIMEOUT" in str(end[2]):
            end[2] == 'NT_STATUS_IO_TIMEOUT'
    
    except subprocess.TimeoutExpired as timeout:
        end = [ 0, 1, timeout.output, timeout.timeout, timeout.stderr ]
        if "TIMEOUT" in str(end[2]):
            end[2] == 'NT_STATUS_IO_TIMEOUT'


    hosts_shared_lists.append( host )
    #return(end)


def get_ip(country):
    PAIS = country
    body = {
        "query": {
            "bool": {
                "must_not": {
                    "exists": {
                        "field": "parsed"
                    }
                },
                "must": [
                    { "exists": { "field": "ip" } },
                    { "term": { "country": PAIS } },
                    { "term": { "map_type": MAP_TYPE } },
                ],
            }
        }
    }

    res = es.search(
        index=INDEX,
        doc_type=INDEX,
        body=body,
        size=1000,
    )

    ips = []
    for doc in res['hits']['hits']:
        ips.append(doc)
    return(ips)


def main():
    
    shared_info['finalizar'] = False

    # query elasticsearch
    ips = get_ip(country)
    print(len(ips))

    for host in ips:
        nets_shared_lists.append(host)

    t = Thread(target=do_winexe)
    t.start()

    pool = ThreadPool(processes=PROCS)
    while len(nets_shared_lists) > 0:
        nets = get_nets_and_clear()
        if len(nets) > 0:
            pool.map(smbclient, nets)
        time.sleep(1)
            
    shared_info['finalizar'] = True
    t.join()

if len(sys.argv) <= 2:
    print('need country and DOMAIN')
    sys.exit(0)
else:
    country = sys.argv[1]
    DOMAIN = sys.argv[2]

manager = Manager()
hosts_shared_lists = manager.list([])
hosts_error_list = manager.list([])
nets_shared_lists = manager.list([])
shared_info = manager.dict()
        
if __name__ == "__main__":
    main()
