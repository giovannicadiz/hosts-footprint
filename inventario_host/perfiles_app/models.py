from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    area =models.CharField(max_length=255, blank=True)
    cargo = models.CharField(max_length=255, blank=True)
    # PAIS_CHOICES
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
    pais = models.CharField(max_length=11, blank=True, null=False,  choices=PAIS_CHOICES)


    def __str__(self):
        return(u'%s' % self.usuario)

@receiver(post_save, sender=User)
def crear_usuario_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(usuario=instance)

@receiver(post_save, sender=User)
def guardar_usuario_perfil(sender, instance, **kwargs):
    instance.perfil.save()
