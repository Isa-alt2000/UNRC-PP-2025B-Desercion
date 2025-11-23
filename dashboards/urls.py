from django.urls import path
from . import finanzas

app_name = 'dashboards'

urlpatterns = [
    path('cuentas/', finanzas.lista_cuentas, name='lista_cuentas'),
    path('cuentas/nueva/', finanzas.crear_cuenta, name='crear_cuenta'),
    path('cuentas/<int:cuenta_id>/', finanzas.detalle_cuenta, name='detalle_cuenta'),
    path('cuentas/<int:cuenta_id>/eliminar/', finanzas.eliminar_cuenta, name='eliminar_cuenta'),
    path('cuentas/<int:cuenta_id>/nuevo-movimiento/', finanzas.agregar_movimiento, name='agregar_movimiento'),
    path('cuentas/<int:cuenta_id>/movimiento/<int:movimiento_id>/eliminar/', finanzas.eliminar_movimiento, name='eliminar_movimiento'),
    path('cuentas/<int:cuenta_id>/editar-movimiento/<int:movimiento_id>/', finanzas.editar_movimiento, name='editar_movimiento'),
    path('cuentas/<int:cuenta_id>/editar/', finanzas.editar_cuenta, name='editar_cuenta'),
]
