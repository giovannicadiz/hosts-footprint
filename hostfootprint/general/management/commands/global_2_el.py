#encoding=utf8
import sys
#from __future__ import print_function
from django.core.management.base import BaseCommand, CommandError
from general.models import *

def main(options):

    # total tiendas
    all_locals = Local.objects.filter(activo == True)
    print(len(all_locals))

    for x in all_locals:

        if options['action'] == 'save':
            x_obj = {
                'country': x.city.country.name,
                'city': x.city.city,
                'businessunit': x.flag.businessunit.businessunit,
                'flag': x.flag.flag,
                'local_id': x.local_id,
                'local_address': x.local_address,
                'local_desc': x.local_desc,
                'geo_point': {
                    'lat': x.lat,
                    'lon': x.lon
                }
            }
            el = ElsSave('locals')
            el.els_save(x_obj)
            
        else:
            print("""
            country: %s \n
            city: %s \n
            businessunit: %s \n
            flag: %s \n
            local_id: %s \n
            local_address: %s \n
            local_desc: %s \n
            lat: %s \n
            lon: %s \n
            """ % ( x.city.country,
                    x.city.city,
                    x.flag.businessunit.businessunit,
                    x.flag,
                    x.local_id,
                    x.local_address,
                    x.local_desc,
                    x.lat,
                    x.lon)
            )
        

class Command(BaseCommand):
    help = 'create global object and save on elasticsearch'
    def add_arguments(self, parser):
        parser.add_argument('-a', '--action', required=False, \
                            help=u'save or console')

    def handle(self, *args, **options):
        main(options)
