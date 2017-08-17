from django.contrib import admin
from networks.models import Network

# Register your models here.
admin.site.site_header = 'Host Network - Admin Interface'

class NetworkAdmin(admin.ModelAdmin):
    list_display_links = [ 'network', 'local' ]
    list_display = [
        'local',
        'network',
        'description',
        'country',
        'activo'
    ]

    list_filter = [
        'local__activo',
        'local__city__country',
        'local__flag__flag'
    ]
    # customer 
    search_fields = [ 'network', 'local__local_id' ]
    list_per_page = 40

    def country(self, network):
        return(network.local.city.country)
    
    def activo(self, network):
        return(network.local.activo)

admin.site.register(Network, NetworkAdmin)



