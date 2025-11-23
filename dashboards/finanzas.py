from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Sum
from django.contrib import messages
from .models import Cuenta, Movimiento
from .forms import CuentaForm, MovimientoForm
from django.contrib.auth.decorators import login_required


@login_required
def lista_cuentas(request):
    cuentas = Cuenta.objects.filter(usuario=request.user)
    for cuenta in cuentas:
        ingresos_q = cuenta.movimientos.filter(tipo='INGRESO').aggregate(Sum('monto'))
        ingresos = ingresos_q.get('monto__sum') or 0
        egresos_q = cuenta.movimientos.filter(tipo='EGRESO').aggregate(Sum('monto'))
        egresos = egresos_q.get('monto__sum') or 0
        cuenta.balance = ingresos - egresos

    form = CuentaForm()
    form_action = reverse('dashboards:crear_cuenta')
    return render(request, 'cuentas_lista.html', {
        'cuentas': cuentas,
        'form': form,
        'form_action': form_action,
    })


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
            cuentas = Cuenta.objects.filter(usuario=request.user)
            for cuenta in cuentas:
                ingresos_q = cuenta.movimientos.filter(tipo='INGRESO').aggregate(Sum('monto'))
                ingresos = ingresos_q.get('monto__sum') or 0
                egresos_q = cuenta.movimientos.filter(tipo='EGRESO').aggregate(Sum('monto'))
                egresos = egresos_q.get('monto__sum') or 0
                cuenta.balance = ingresos - egresos

            return render(request, 'cuentas_lista.html', {
                'cuentas': cuentas,
                'form': form,
                'open_modal': True,
            })
    else:
        form = CuentaForm()

    return render(request, 'cuenta_form.html', {'form': form})


@login_required
def detalle_cuenta(request, cuenta_id):
    cuenta = get_object_or_404(Cuenta, id=cuenta_id, usuario=request.user)
    movimientos = cuenta.movimientos.all().order_by('-fecha')

    ingresos_q = cuenta.movimientos.filter(tipo='INGRESO').aggregate(Sum('monto'))
    ingresos = ingresos_q.get('monto__sum') or 0
    egresos_q = cuenta.movimientos.filter(tipo='EGRESO').aggregate(Sum('monto'))
    egresos = egresos_q.get('monto__sum') or 0
    balance = ingresos - egresos

    form = MovimientoForm()

    return render(request, 'cuenta_detalle.html', {
        'cuenta': cuenta,
        'movimientos': movimientos,
        'balance': balance,
        'form': form
    })


@login_required
def eliminar_cuenta(request, cuenta_id):
    cuenta = get_object_or_404(Cuenta, id=cuenta_id)

    if request.method == 'POST':
        cuenta.delete()
        messages.success(request, "Cuenta eliminada correctamente.")
        return redirect('dashboards:lista_cuentas')

    return render(request, 'dashboards/confirmar_eliminar_cuenta.html', {'cuenta': cuenta})


@login_required
def agregar_movimiento(request, cuenta_id):
    cuenta = get_object_or_404(Cuenta, id=cuenta_id, usuario=request.user)
    if request.method == 'POST':
        form = MovimientoForm(request.POST)
        if form.is_valid():
            movimiento = form.save(commit=False)
            movimiento.cuenta = cuenta
            movimiento.save()
            return redirect('dashboards:detalle_cuenta', cuenta_id=cuenta.id)
    else:
        form = MovimientoForm()
    return render(request, 'movimiento_form.html', {'form': form, 'cuenta': cuenta})


@login_required
def eliminar_movimiento(request, cuenta_id, movimiento_id):
    cuenta = get_object_or_404(Cuenta, id=cuenta_id, usuario=request.user)
    movimiento = get_object_or_404(Movimiento, id=movimiento_id, cuenta=cuenta)

    if request.method == 'POST':
        movimiento.delete()
        messages.success(request, "Movimiento eliminado correctamente.")
        return redirect('dashboards:detalle_cuenta', cuenta_id=cuenta.id)

    return redirect('dashboards:detalle_cuenta', cuenta_id=cuenta.id)


@login_required
def editar_movimiento(request, cuenta_id, movimiento_id):
    cuenta = get_object_or_404(Cuenta, id=cuenta_id, usuario=request.user)
    movimiento = get_object_or_404(Movimiento, id=movimiento_id, cuenta=cuenta)

    if request.method == 'POST':
        form = MovimientoForm(request.POST, instance=movimiento)
        if form.is_valid():
            form.save()
            messages.success(request, "Movimiento actualizado correctamente.")
            return redirect('dashboards:detalle_cuenta', cuenta_id=cuenta.id)
    else:
        form = MovimientoForm(instance=movimiento)

    return redirect('dashboards:detalle_cuenta', cuenta_id=cuenta.id)


@login_required
def editar_cuenta(request, cuenta_id):
    cuenta = get_object_or_404(Cuenta, id=cuenta_id, usuario=request.user)

    if request.method == 'POST':
        form = CuentaForm(request.POST, instance=cuenta)
        if form.is_valid():
            form.save()
            messages.success(request, "Cuenta actualizada correctamente.")
            return redirect('dashboards:lista_cuentas')
        else:
            # Si hay errores al editar, renderizamos la lista y abrimos el modal
            cuentas = Cuenta.objects.filter(usuario=request.user)
            for c in cuentas:
                ingresos_q = c.movimientos.filter(tipo='INGRESO').aggregate(Sum('monto'))
                ingresos = ingresos_q.get('monto__sum') or 0
                egresos_q = c.movimientos.filter(tipo='EGRESO').aggregate(Sum('monto'))
                egresos = egresos_q.get('monto__sum') or 0
                c.balance = ingresos - egresos

            form_action = reverse('dashboards:editar_cuenta', args=[cuenta.id])
            return render(request, 'cuentas_lista.html', {
                'cuentas': cuentas,
                'form': form,
                'form_action': form_action,
                'open_modal': True,
            })
    else:
        form = CuentaForm(instance=cuenta)

    return render(request, 'cuenta_form.html', {'form': form, 'cuenta': cuenta})
