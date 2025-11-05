from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import Group
from .forms import CustomAuthenticationForm, CustomUserCreationForm
from .models import User
from django.contrib import messages
from django.urls import reverse_lazy


#Registro
def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            group, created = Group.objects.get_or_create(name="Usuario")
            user.groups.add(group)
            messages.success(request, "¡Registro exitoso! Serás redirigido al inicio de sesión.")
            return render(request, "registro.html", {"form": form, "show_modal": True})
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = CustomUserCreationForm()

    return render(request, "registro.html", {"form": form})


# Login
class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = "login.html"

    def get_success_url(self):
        return reverse_lazy('home')


# Logout
class CustomLogoutView(LogoutView):
    next_page = "home"