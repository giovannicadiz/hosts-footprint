from inventario_app.models import Inventario
from rest_framework import serializers


class InventarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventario
        fields = (

            'id',
            'PAIS',
            'NAGIOS',
            'APM',
            'HOSTNAME',
            'IP',
            'MAC',
            'SO',
            'SO_VERSION',
            'SO_PROVEEDOR',
            'UUNN',
            'Es_Virtual',
            'En_Ope',
            'AMBIENTE',
            'ROL',
            'SERVICIO',
            'APLICACION',
            'KPI',
            'FUNCIONAL',
            'ROS',
            'LIDER_DATACENTER',
            'OIT',
            'DOC',
            'OBS',
            # 'IMAGEN',
        )


