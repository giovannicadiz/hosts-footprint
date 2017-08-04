from __future__ import unicode_literals
from django.db import models
from general.models import *
from django.utils.translation import ugettext_lazy as _
#import elasticsearch_opentracing

from elasticsearch import Elasticsearch,helpers

import ipaddress

# Create your models here.
class Network(models.Model):
    '''
    network model used to search devices
    '''
    local = models.ForeignKey(Local)
    network =  models.CharField(max_length=26,
                                default='172.18.148.0/24',
                                unique=True)
    description = models.CharField(max_length=150,
                                   default="VLAN VoIP",
                                   verbose_name=(u'vlan description'),
                                   blank=True, null=True)
    
    total_subnetworks = models.IntegerField(default=0)
    
    good_networks = models.BooleanField(default=True)

    def __str__(self):
        return(u'%s' % self.network)
    
class CreateSubNetworks(object):

    def __init__(self):
        pass
        #self.network_object = network_object

    def make_subnetworks(self, network_object):

        try:
            ip_net = ipaddress.ip_network(network_object.network)
            #self.network_object.good_networks = True
        except:
            #self.network_object.good_networks = False
            #self.network_object.save()
            return(False)
        try:
            sub_net = ip_net.subnets(new_prefix=24)
            sub_net = list(sub_net)
            if len(sub_net) > 1:
                network_object.total_subnetworks = len(sub_net)
            return(sub_net)
        except:
            sub_net = [ ip_net ]

        #self.network_object.save()
        return( [ ip_net ]) 

class ElsSaveMap(object):
    def __init__(self, object_type, doc_type):
        '''
        init global variables
        pass host to elasticsearch connect
        '''
        # elasticsearch
        #self.client = Elasticsearch(
        #    transport_class=elasticsearch_opentracing.TracingTransport,
        #                            hosts=[ settings.ELASTICSEARCH ]
        #)
        self.client = Elasticsearch(
            hosts=[ settings.ELASTICSEARCH ]
        )
        self.object_type = object_type
        self.doc_type = doc_type

    def es_save(self, map_type, host, netobject):

        normalize = ''.join(c.lower() for c in host if not c.isspace())
        today = datetime.today().strftime("%m%d%Y")
        _id=(normalize + '-' + today)

        attribute = {
            'map_type': map_type,
            'ip': host,
            'network': netobject.network,
            'country': netobject.local.city.country.name,
            'city': netobject.local.city.city,
            'businessunit': netobject.local.flag.businessunit.businessunit,
            'flag': netobject.local.flag.flag,
            'local_id': netobject.local.local_id,
            'local_address': netobject.local.local_address,
            'local_desc': netobject.local.local_desc,
            'geo_point': {
                'lat': netobject.local.lat,
                'lon': netobject.local.lon
            }
        }

        data = datetime.now()
        date_els = int( data.timestamp() * 1000 )

        attribute['created_at'] = date_els

        response = self.client.index(
            index=self.object_type,
            id=_id,
            doc_type=self.doc_type,
            body=attribute
        )
        #print(response)
