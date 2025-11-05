from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cuenta
from .forms import CuentaForm


@login_required
def lista_cuentas(request):
    cuentas = Cuenta.objects.filter(usuario=request.user)
    return render(request, 'cuentas_lista.html', {'cuentas': cuentas})


@login_required
def crear_cuenta(request):
    if request.method == 'POST':
        form = CuentaForm(request.POST)
        if form.is_valid():
            cuenta = form.save(commit=False)
            cuenta.usuario = request.user
            cuenta.save()
            return redirect('dashboards:lista_cuentas')
    else:
        form = CuentaForm()
    return render(request, 'cuenta_form.html', {'form': form})
