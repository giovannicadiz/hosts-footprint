from rest_framework import viewsets
from inventario_app.models import Inventario
from inventario_app.serializers import InventarioSerializer
from django.views.generic.list import ListView


# Create your views here.
class InventarioViewSet(viewsets.ModelViewSet):
    model = Inventario
    http_method_names = ['get', 'head', 'post']
    queryset = Inventario.objects.all()
    serializer_class = InventarioSerializer


class InventarioListaView(ListView):
    model = Inventario

    def get_context_data(self, **kwargs):
        context = super(InventarioListaView, self).get_context_data(**kwargs)
        lista_inventario = Inventario.objects.all()
        context['lista_inventario'] = lista_inventario
        return context




