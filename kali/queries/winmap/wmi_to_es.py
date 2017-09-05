#!/usr/bin/env python3

import sys, time, os
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

user = os.getenv('MAPUSER')
es_server = os.getenv('ELASTICSEARCH')

es = Elasticsearch( hosts=[ es_server ])
INDEX = 'nmap'
MAP_TYPE = 'nmap'
PROCS=20
WINEXEPROCS=12

###### MP
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


####

class WinCheck(object):
    """
    wmick = WinCheck(ip)

    # Win32_OperatingSystem
    # Win32_ComputerSystem
    # Win32_QuickFixEngineering
    # Win32_ComputerSystemProduct
    """

    """
get_user() {
    USERID_WIN=`wmic  -U "$LUSER" //$LHOST "SELECT LogonId FROM Win32_LogonSession WHERE LogonType = 2 or LogonType = 10" | tail -n1`
    if [ "$?" = "0" ]; then
	USERCAPTION=`wmic  -U "$LUSER" //$LHOST "Associators Of {Win32_LogonSession.LogonId=$USERID_WIN} WHERE AssocClass=Win32_LoggedOnUser Role=Dependent"| awk -F "|" '{ print $2}' | tail -n1`
	if echo "$USERCAPTION" | grep -q "$LDOMAIN" ; then 
	    header_user=$(printf '%s\n' "UserName")            
	    value_user=$(printf '%s\n' "$USERCAPTION")
	fi
    fi
}
    """


    """

    1a - construir um modulo que receba um IP como parametro e monte o objeto:
    data de inicializacao - OK
    sistema operativo - OK
    architetura - OK
    service pack - OK

    lista de patches instalados - OK
    
    ip - OK
    hostname- OK
    id = ip-dia-mes-ano - OK
    """
    def __init__(self, ip):
        """
        master object
        'winuserpass': 'cencosud\_lego%p0o9i8u7y6'
            'winuserpass': base64.b64decode('Y2VuY29zdWRcX2NsdXN0ZXJzZXJ2aWNlMSV2Nnk4YXlyNmN4MWwxN3dqcQo=').replace("\n")


            'Win32_ComputerSystem': 'wmic  -U "%s" //%s "SELECT Model,Manufacturer,CurrentTimeZone,DaylightInEffect,EnableDaylightSavingsTime,NumberOfLogicalProcessors,NumberOfProcessors,Status,SystemType,ThermalState,TotalPhysicalMemory from Win32_ComputerSystem"' % (self.winobject['winuserpass'], self.winobject['ip']),

        """
        self.commands = {
            # Win32_OperatingSystem
            'Win32_OperatingSystem': 'SELECT Caption,CSDVersion,CSName,ServicePackMajorVersion,LastBootUpTime from Win32_OperatingSystem',
            # Win32_ComputerSystem:
            'Win32_ComputerSystem': 'SELECT Model,Manufacturer,CurrentTimeZone,DaylightInEffect,EnableDaylightSavingsTime,NumberOfLogicalProcessors,NumberOfProcessors,Status,SystemType,ThermalState,TotalPhysicalMemory from Win32_ComputerSystem',
            # 

            ########### Architecture #################### CRASH SOME OLDS S.O.s Queries (make result in blank)
            #'Win32_OperatingSystem': 'SELECT OSArchitecture from Win32_OperatingSystem'
            ########### HotfixID
            'Win32_QuickFixEngineering': 'SELECT HotfixID from win32_QuickFixEngineering',
            #
            ########### CHECK_MK
            #'check_mk': 'nmap --open -p 6556 %s 2>/dev/null | grep "6556/tcp"' % (self.winobject['ip']),
        }
        
    def subproc_exec(self):
        """
        in action
        """

        result = {}
        for k,v in self.commands.items():
            time.sleep(0.5)
            result[k] = {}

            try:
                l_subproc = subprocess.check_output(v, shell=True)
                line = l_subproc.decode().split('\n')

                if k in [ 'Win32_OperatingSystem', 'Win32_ComputerSystem' ]:

                    header = line[1].split('|')
                    info = line[2].split('|')

                    pointer = 0
                    while pointer < len(header):
                        result[header[pointer]] = info[pointer]
                        pointer = pointer + 1
                
                if k == 'Win32_QuickFixEngineering':
                    header = 'HotFixID'
                    result[header] = []

                    for fix in line[2:-1]:
                        fix = fix.replace('|', '')
                        result[header].append(fix)

                if k == 'check_mk':
                    if 'open' in line:
                        result[k] = 1
                    else:
                        result[k] = 0
            except:
                result[k] = False

        self.winobject['result'] = result
        return(self.winobject)

    def console(self):
        print(self.winobject['ip'], self.winobject['result'])

### END MP        
def winmap_xp(user, host, timeout=120):

    winmap_xp_command = ['./winmap_xp.sh', \
                         user, host, DOMAIN, timeout]

    result = []

    try:
        output = qx(winmap_xp_command[0:-1], timeout=winmap_xp_command[-1])
        err = [3]
    except CalledProcessError as time_err:
        output = (2, time_err.output, time_err.returncode,  )

    except subprocess.TimeoutExpired as timeout:
        output = ( 1, timeout.output, timeout.timeout, timeout.stderr )

    try:
        output = output.decode()
        if DOMAIN in output:
            output = output.replace('Caption', 'hostname')
            xp_list = output.split('\n')
            xp_header = xp_list[0]
            xp_value = xp_list[1]

            xp_header_list = xp_header.split('|')
            xp_value_list = xp_value.split('|')
            result = []
            count = 0
            for i in xp_header_list:
                i_value = ("%s=%s" % (xp_header_list[count], xp_value_list[count]) )
                result.append(i_value)
                count = count + 1
                #output = output.replace('\n', '')
                #output = output.split('|')
            result.append('Caption=Windows XP')
            result = [ 0 ] + result
            print(result)
    except:
        print("fail: %s" ,  output)
        result = [-2, output]

    return(result)

def wmi_execution(host, timeout=120):
    
    # antivirus problem!
    #command = 'cmd /c c:\Temp\winmap.bat'
    #winexe_command = ['winexe', '-U', user, str('//' + host['_source']['ip']), command, timeout]

    try:
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

    if 'Caption' not in str(winexe):
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


def smbclient(host, timeout=30):

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
        "sort" : [
            { "created_at" : {"order" : "desc"}},
        ],
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
