from django.contrib import admin
from networks.models import Network

# Register your models here.
admin.site.site_header = 'Host Network - Admin Interface'

class NetworkAdmin(admin.ModelAdmin):
    list_display_links = [ 'network', 'good_networks' ]
    list_display = [
        'local',
        'network',
        'description',
        'good_networks',
        'country'
    ]

    list_filter = [ 'local__activo', 'local__city__country' ]
    # customer 
    
    search_fields = [ 'network', 'local__local_id' ]
    list_per_page = 40

    def country(self, network):
        return(network.local.city.country)

admin.site.register(Network, NetworkAdmin)



