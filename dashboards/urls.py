from django.urls import path
from . import views

app_name = 'dashboards'

urlpatterns = [
    path('cuentas/', views.lista_cuentas, name='lista_cuentas'),
    path('cuentas/nueva/', views.crear_cuenta, name='crear_cuenta'),
    path('cuentas/<int:cuenta_id>/', views.detalle_cuenta, name='detalle_cuenta'),
    path('cuentas/<int:cuenta_id>/eliminar/', views.eliminar_cuenta, name='eliminar_cuenta'),
    path('cuentas/<int:cuenta_id>/nuevo-movimiento/', views.agregar_movimiento, name='agregar_movimiento'),
    path('cuentas/<int:cuenta_id>/movimiento/<int:movimiento_id>/eliminar/', views.eliminar_movimiento, name='eliminar_movimiento'),
]
