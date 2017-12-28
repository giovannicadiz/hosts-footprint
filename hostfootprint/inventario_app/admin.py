from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from inventario_app.models import Inventario
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter


# Register your models here.
class InventarioAdmin(ImportExportModelAdmin):
    # view total count in head
    show_full_result_count = False
    # list of visualization by field
    list_display = (
        # 'id',
        'HOSTNAME','IP','MAC','PAIS','KPI','En_Ope','AMBIENTE','UUNN','APLICACION','SERVICIO','FUNCIONAL','ROS',
        'LIDER_DATACENTER','OBS','NAGIOS','APM','SO','SO_VERSION','SO_PROVEEDOR','Es_Virtual','ROL','OIT','DOC',
        # 'IMAGEN',
    )
    # list display link
    list_display_links = ('HOSTNAME',)
    # search filters by field
    search_fields = [
        # 'id',
        'PAIS','NAGIOS','APM','HOSTNAME','IP','MAC','SO','SO_VERSION','SO_PROVEEDOR','UUNN','Es_Virtual','En_Ope',
        'AMBIENTE','ROL','SERVICIO','APLICACION','KPI','FUNCIONAL','ROS','LIDER_DATACENTER','OIT','DOC','OBS'
    ]
    # list_filter
    list_filter = (
        # for ordinary fields
        ('PAIS', DropdownFilter),
        ('UUNN', DropdownFilter),
        ('AMBIENTE', DropdownFilter),
        ('SERVICIO', DropdownFilter),
        #('KPI', DropdownFilter),
        # for related fields
        # ('field_foreignkey_field', RelatedDropdownFilter),
    )
    # list max 10 per page
    list_per_page = 10
    # ordering per field
    ordering = ('id',)
    
admin.site.register(Inventario, InventarioAdmin)

