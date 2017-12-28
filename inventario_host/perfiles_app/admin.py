from django.contrib import admin
from perfiles_app.models import Perfil
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter


# Register your models here.
@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    # view total count in head
#   show_full_result_count = False
    # list of visualization by field
    list_display = ('usuario','pais', 'area', 'cargo',)
#   list_display = ('usuario','pais','cargo',)
    # search filters by field
   # search_fields = ['pais', 'area', 'cargo']
#   search_fields = ['pais','cargo']
    # list_filter
#   list_filter = (
        # for ordinary fields
#        ('pais', DropdownFilter),
        # for field_foreignkey_field
#        ('usuario', RelatedDropdownFilter),
#   )
    # ordering per field
#   ordering = ('usuario',)

