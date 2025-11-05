from django.urls import path
from . import views
from user import login, profiles, view_admin

app_name = 'dashboards'

urlpatterns = [
    path('cuentas/', views.lista_cuentas, name='lista_cuentas'),
    path('cuentas/nueva/', views.crear_cuenta, name='crear_cuenta'),
]
