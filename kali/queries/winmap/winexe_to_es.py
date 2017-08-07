#!/usr/bin/env python3

from elasticsearch import Elasticsearch

from subprocess import STDOUT, CalledProcessError, check_output as qx
import subprocess, sys, json, re
from datetime import datetime

if len(sys.argv) <= 1:
    print('need country')
else:
    country = sys.argv[1]

class EstadoNaoDeterminado(Exception):
    pass

settings = open('settings.txt').readlines()
user = settings[0].replace('\n', '')
es_server = settings[1].replace('\n', '')

es = Elasticsearch( hosts=[ es_server ])
INDEX = 'nmap'
MAP_TYPE = 'windows'

def time_execution(user, host, command, timeout=30):

    winexe_command = ['winexe', '-U', user, str('//' + host), command, timeout]

    try:
        print (winexe_command[0:-1])
        output = qx(winexe_command[0:-1], timeout=winexe_command[-1])
        result = (output.decode("utf-8",errors='ignore'))
        result = result.split('\n')
        return(result)

    except CalledProcessError as time_err:
        winexe_err = ( time_err.returncode, str(time_err.output) )
        return(winexe_err)
    except subprocess.TimeoutExpired as timeout:
        winexe_err = ( 1, str(timeout.output), str(timeout.timeout), str(timeout.stderr) )
        return(winexe_err)

def update_es_winexe(_id, winexe):

    _id = _id
    
    winmap_dict = {
        'parsed': 1,
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
            print('value fail on %s: %s' % ( _id, i ) )
        
    # :-)
    body = {
        "doc": winmap_dict
    }

    try:
        response = es.update(
            index=INDEX,
            doc_type=INDEX,
            id=_id,
            body=body
        )
        return(response)
    except:
        return("fail: %s" % _id)

def get_parsed(country):
    PAIS = country
    body = {
        "query": {
            "bool": {
                "must": [
                    { "term": { "country": PAIS } },
                    { "term": { "map_type": MAP_TYPE } },
                    { "term": { "parsed": "0" } },
                    { "term": { "exit_code": "0" } }
                ]
            },
        }
    }

    res = es.search(
        index=INDEX,
        doc_type=INDEX,
        body=body,
        size=1000,
    )

    parsed = []
    for doc in res['hits']['hits']:
        parsed.append(doc)
    return(parsed)

parsed = get_parsed(country)
              
for host in parsed:
    winexe = (
        time_execution(
            user,
            host['_source']['ip'],
            "c:\Temp\winmap.bat"
        )
    )
    #print(winexe)
    print(update_es_winexe(host['_id'], winexe))
