"""hostfootprint URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from inventario_app.views import InventarioViewSet,InventarioListaView
from perfiles_app.views import SignUpView, BienvenidaView, SignInView, SignOutView
from django.contrib.auth.decorators import login_required

router = routers.DefaultRouter()
router.register(r'',InventarioViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls), # admin
    url(r'^api/', include(router.urls)), # api
    url(r'^inventario/$', login_required(InventarioListaView.as_view(template_name="index.html")),name='inventario'), # view inventario, login required
    url(r'^$', BienvenidaView.as_view(), name='bienvenida'), # page home
    url (r'^registrate/$', SignUpView.as_view (), name='sign_up'), # registrar user
    url (r'^inicia-sesion/$', SignInView.as_view (), name='sign_in'), # login
    url (r'^cerrar-sesion/$', SignOutView.as_view (), name='sign_out'), # logout
]

