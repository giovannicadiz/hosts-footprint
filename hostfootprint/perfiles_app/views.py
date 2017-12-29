from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.views.generic import CreateView, TemplateView
from perfiles_app.models import Perfil
from perfiles_app.forms import SignUpForm
#
from django.contrib.auth.views import LoginView, LogoutView



# Create your views here.
class SignUpView(CreateView):

    model = Perfil
    form_class = SignUpForm

    def form_valid(self, form):

        form.save()
        usuario = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        usuario = authenticate(username=usuario, password=password)
        login(self.request, usuario)
        return redirect('/')

class BienvenidaView(TemplateView):
    template_name = 'perfiles/bienvenida.html' # OK


class SignInView(LoginView):
    template_name = 'perfiles/iniciar_sesion.html'


class  SignOutView(LogoutView):
    pass




