from django.contrib import admin
from networks.models import Network

# Register your models here.
admin.site.site_header = 'Host Network - Admin Interface'

class NetworkAdmin(admin.ModelAdmin):
    list_display_links = [ 'local', 'network', 'description', 'good_networks' ]
    list_display = [
        'local',
        'network',
        'description',
        'good_networks',
        'total_subnetworks'
    ]
    search_fields = [ 'local']
    list_per_page = 40

admin.site.register(Network, NetworkAdmin)



