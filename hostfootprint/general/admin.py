from django.contrib import admin

from general.models import *

# Register your models here.

admin.site.site_header = 'LEGO - Admin Interface'

class CityAdmin(admin.ModelAdmin):
    list_display_links = ['city']
    list_display = [ 'country', 'city' ]
    list_filter = [ 'country' ]
    search_fields = ['city']
    list_per_page=40

class BusinessUnitAdmin(admin.ModelAdmin):
    list_display_links = ['businessunit']
    list_display = ['businessunit']
    search_fields = ['businessunit']
    list_per_page=40
    
class FlagAdmin(admin.ModelAdmin):
    list_display_links = ['flag', 'businessunit' ]
    list_display = ['flag', 'businessunit']
    list_filter = ['businessunit']
    search_fields = ['flag'] 
    list_per_page=40
    
class LocalAdmin(admin.ModelAdmin):
    list_display = [
        'local_id',
        'flag',
        'businessunit',
        'city',
        'activo'
    ]
    list_display_links = [
        'flag__flag',
        'local_id',
        'city',
    ]

    search_fields = [ 'local_id', 'flag__flag', ]

    list_per_page = [
        'local_id',
        'local_address',
        'city__city',
        'city__country',
        'flag__flag',
        'local_type',
    ]

    list_filter = [
        'flag__businessunit__businessunit',
        'flag__flag',
        'activo',
        'city__country',
    ]
    list_per_page=40

    def businessunit(self, obj):
        return(obj.flag.businessunit)

# lego
admin.site.register(City, CityAdmin)
admin.site.register(BusinessUnit, BusinessUnitAdmin)
admin.site.register(Flag, FlagAdmin)
admin.site.register(Local, LocalAdmin)
