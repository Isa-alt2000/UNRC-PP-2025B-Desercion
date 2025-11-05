from django import forms
from .models import Cuenta, Ingreso, Egreso

class CuentaForm(forms.ModelForm):
    class Meta:
        model = Cuenta
        fields = ['nombre', 'tipo', 'saldo_inicial', 'descripcion']


class IngresoForm(forms.ModelForm):
    class Meta:
        model = Ingreso
        fields = ['cuenta', 'categoria', 'monto', 'descripcion']


class EgresoForm(forms.ModelForm):
    class Meta:
        model = Egreso
        fields = ['cuenta', 'categoria', 'monto', 'descripcion']
