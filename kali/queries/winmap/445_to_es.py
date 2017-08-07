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

def smbclient(user, host, timeout=20):

    smbclient_command = ['./smbclient.sh', \
                         user, host, timeout]

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

    return(end)
def update_es_ip(_id, status):
    _id = _id
    parse = int(status[0]),
    exit_code = int(status[1]),
    smb_copy = str(status[2])
    
    # :-)
    body = {
        "doc":{
            "parsed": parse,
            "exit_code": parse,
            "smbclient": smb_copy
        }
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

ips = get_ip(country)
              
for host in ips:
    parsed = (smbclient(user, host['_source']['ip']))
    update_es_ip(host['_id'], parsed)
