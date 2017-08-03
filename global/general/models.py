from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django_countries.fields import CountryField

from elasticsearch import Elasticsearch,helpers

from geopy.geocoders import Nominatim
from geopy.exc import GeopyError

from datetime import datetime

# Create your models here.
class DateUTC(object):

    def __init__(self, time_zone):
        self.pytimezone = pytz.timezone(time_zone)
        self.utc = pytz.utc
        
    def utc_to_timezone(self, date_time):
        date_utc = self.pytimezone.normalize(date_time)
        date_tz = date.astimezone(self.pytimezone)
        date_tz_stamp = ( int(date_tz.timestamp()) )
        date_tz_els = ( int(date_tz_stamp) * 1000 )
        return({
            'date': date_tz,
            'date_stamp': date_tz_stamp,
            'date_els': date_tz_els,
        })
    
    def timezone_to_utc(self, date_time):
        date_tz = self.pytimezone.localize(date_time)
        date_utc = tz_date.astimezone(self.utc)
        date_utc_stamp = ( int(date_utc.timestamp()) )
        date_utc_els = ( int(date_utc_stamp) * 1000 )
        return({
            'date': date_utc,
            'date_stamp': date_utc_stamp,
            'date_els': date_utc_els,
        })

class ElsSave(object):
    def __init__(self, object_type):
        '''
        init global variables
        pass host to elasticsearch connect
        '''
        # elasticsearch
        self.client = Elasticsearch(hosts=[ settings.ELASTICSEARCH ])
        self.object_type = object_type
                
    def els_save(self, attribute):
        if self.object_type == 'locals':

            normalize = ''.join(c.lower() for c in attribute['local_id'] if not c.isspace())
            today = datetime.today().strftime("%m%d%Y")
            _id=(normalize + '-' + today)

            data = datetime.now()
            date_els = int( data.timestamp() * 1000 )
            
            attribute['created_at'] = date_els

            response = self.client.index(
                index=self.object_type,
                id=_id,
                doc_type=self.object_type,
                body=attribute)
            print(response)

    def els_update(self, attribute, script):
        if self.object_type == 'locals':

            normalize = ''.join(c.lower() for c in attribute['local_id'] if not c.isspace())
            today = datetime.today().strftime("%m%d%Y")
            _id=(normalize + '-' + today)

            try:
                response = self.client.update(
                    index=self.object_type,
                    id=_id,
                    doc_type=self.object_type,
                    body=script)
                #print(response)
            except:
                print("fail: %s" % _id)

class GeoPoint(object):

    def __init__(self):
        self.geolocator = Nominatim()

    def make_geopoint(self, attribute):
        try:
            location = self.geolocator.geocode(u'%s, %s' % (
                attribute.city.city,
                attribute.city.country.name)
            )

            if location is None:
                raise GeopyError(_(u'Latitude e longitude not found'))
            else:
                attribute.lat = location.latitude
                attribute.lon = location.longitude
        
        except GeopyError as e:
            attribute.lat = 0
            attribute.lon = 0
            #raise e

        return(attribute)

# global django models
class City(models.Model):
    
    '''
    network City
    '''
    country = CountryField(blank_label='(select country)')
    city = models.CharField(max_length=40,
                            verbose_name=(u'City'),
                            unique=True)

    def __str__(self):
        return(u'%s' % self.city)

class BusinessUnit(models.Model):
    
    '''
    BussinessUnit
    '''
    businessunit = models.CharField(verbose_name=(u'Business Unit'),
                                    max_length=100,
                                    unique=True)

    def __str__(self):
        return(u'%s' % self.businessunit)

class Flag(models.Model):
    '''
    Flag
    '''
    businessunit = models.ForeignKey(BusinessUnit)
    flag = models.CharField(verbose_name=(u'Flag'),
                            max_length=100,
                            unique=True)

    def __str__(self):
        return(u'%s' % self.flag)

class Local(models.Model):
    '''
    Company owner of Data Center
    '''
    city = models.ForeignKey(City)
    flag = models.ForeignKey(Flag)
    local_id = models.CharField(max_length=200,
                                verbose_name=(u'Local ID'),
                                default='BB200',
                                unique=True)
    local_address = models.CharField(max_length=200, default='Street xxx, 2020')

    local_desc = models.CharField(max_length=100,
                                  verbose_name=(u'Description'),
                                  blank=True,
                                  unique=False)
    
    lat = models.FloatField(verbose_name=(u'Latitud'), blank=True, null=True)
    lon = models.FloatField(verbose_name=(u'Longitud'), blank=True, null=True)
                                
    def __str__(self):
        return(u'%s' % self.local_id)


