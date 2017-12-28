from django.db import models
# Create your models here.


class Inventario(models.Model):

    id = models.AutoField(primary_key=True)

    Argentina = 'ARGENTINA'
    Brasil = 'BRASIL'
    Chile = 'CHILE'
    Colombia = 'COLOMBIA'
    Peru = 'PERU'
    Regional = 'REGIONAL'
    sin_asignar = 'SIN ASIGNAR'

    PAIS_CHOICES = (
        (Argentina, 'ARGENTINA'),
        (Brasil, 'BRASIL'),
        (Chile, 'CHILE'),
        (Colombia, 'COLOMBIA'),
        (Peru, 'PERU'),
        (Regional, 'REGIONAL'),
        (sin_asignar, 'SIN ASIGNAR'),
    )
    PAIS = models.CharField(max_length=11, blank=True, null=False,  choices=PAIS_CHOICES)
    NAGIOS = models.CharField(null=True, max_length=18)
    APM = models.CharField(null=True, max_length=6)
    HOSTNAME = models.CharField(null=True, max_length=29)
    IP = models.CharField(null=True, max_length=15)
    MAC = models.CharField(null=True, max_length=17)
    SO = models.CharField(null=True, max_length=19)
    SO_VERSION = models.CharField(null=True, max_length=26)
    SO_PROVEEDOR = models.CharField(null=True, max_length=22)

    aventura = 'AVENTURA'
    bi = 'BI'
    central = 'CENTRAL'
    fidelidad = 'FIDELIDAD'
    mejoramiento_del_hogar = 'MEJORAMIENTO DEL HOGAR'
    N_D = 'N/D'
    operaciones = 'OPERACIONES'
    portal = 'PORTAL'
    retail_financiero = 'RETAIL FINANCIERO'
    rrhh = 'RRHH'
    shopping = 'SHOPPING'
    sin_asignar = 'SIN ASIGNAR'
    supermercado = 'SUPERMERCADO'
    teleticket = 'TELETICKET'
    tiendas_por_departamento = 'TIENDAS POR DEPARTAMENTO'

    UUNN_CHOICES = (
        (aventura, 'AVENTURA'),
        (bi, 'BI'),
        (central, 'CENTRAL'),
        (fidelidad, 'FIDELIDAD'),
        (mejoramiento_del_hogar,'MEJORAMIENTO DEL HOGAR'),
        (N_D, 'N/D'),
        (operaciones,'OPERACIONES'),
        (portal,'PORTAL'),
        (retail_financiero, 'RETAIL FINANCIERO'),
        (rrhh, 'RRHH'),
        (shopping, 'SHOPPING'),
        (sin_asignar, 'SIN ASIGNAR'),
        (supermercado, 'SUPERMERCADO'),
        (teleticket, 'TELETICKET'),
        (tiendas_por_departamento, 'TIENDAS POR DEPARTAMENTO'),
    )
    UUNN =models.CharField( max_length=24, blank=False, null=True, choices=UUNN_CHOICES)
    Es_Virtual = models.CharField(null=True, max_length=7)

    no = 'NO'
    si = 'SI'

    EN_OPE_CHOICE = (
        (no, 'NO'),
        (si, 'SI'),
    )
    En_Ope = models.CharField(null=True, max_length=2, choices=EN_OPE_CHOICE)

    no_hay = '#N/A'
    capacitacion = 'CAPACITACION'
    certificacion = 'CERTIFICACION'
    contingencia = 'CONTINGENCIA'
    desarrollo = 'DESARROLLO'
    historico = 'HISTORICO'
    homologacion = 'HOMOLOGACION'
    integracion = 'INTEGRACION'
    laboratorio = 'LABORATORIO'
    pivote = 'PIVOTE'
    pre_produccion = 'PRE PRODUCCION'
    producccion = 'PRODUCCION'
    proyecto = 'PROYECTO'
    qa = 'QA'
    sin_asignar = 'SIN ASIGNAR'
    stage = 'STAGE'
    stand_by = 'STAND BY'
    test = 'TEST'
    training = 'TRAINING'

    AMBIENTE_CHOICE = (

        (no_hay, '#N/A'),
        (capacitacion, 'CAPACITACION'),
        (certificacion, 'CERTIFICACION'),
        (contingencia, 'CONTINGENCIA'),
        (desarrollo, 'DESARROLLO'),
        (historico, 'HISTORICO'),
        (homologacion, 'HOMOLOGACION'),
        (integracion, 'INTEGRACION'),
        (laboratorio, 'LABORATORIO'),
        (pivote, 'PIVOTE'),
        (pre_produccion, 'PRE PRODUCCION'),
        (producccion, 'PRODUCCION'),
        (proyecto, 'PROYECTO'),
        (qa, 'QA'),
        (sin_asignar, 'SIN ASIGNAR'),
        (stage, 'STAGE'),
        (stand_by, 'STAND BY'),
        (test, 'TEST'),
        (training, 'TRAINING'),
    )
    AMBIENTE = models.CharField( max_length=14, blank=True, null=False, choices=AMBIENTE_CHOICE)

    ROL = models.CharField(null=True, max_length=25)
    SERVICIO = models.CharField(null=True,max_length=17)
    APLICACION = models.CharField(null=True,max_length=45)
    KPI = models.CharField(null=True, max_length=7)
    FUNCIONAL = models.CharField(null=True, max_length=44)
    ROS = models.CharField(null=True, max_length=97)
    LIDER_DATACENTER = models.CharField(null=True, max_length=23)
    OIT = models.CharField(null=True, max_length=7)
    DOC = models.CharField(null=True, max_length=189)
    OBS = models.CharField(null=True, max_length=10)
    IMAGEN = models.CharField(null=True, max_length=10)

    def __str__(self):
        return(u'%s' % self.HOSTNAME)






