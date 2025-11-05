from django import forms
from django.core.exceptions import ValidationError
from .models import Cuenta, Movimiento


class CuentaForm(forms.ModelForm):
    class Meta:
        model = Cuenta
        fields = ['nombre', 'descripcion']


class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = ['tipo', 'monto', 'descripcion', 'fecha']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'monto': forms.NumberInput(attrs={'min': '0', 'step': '0.01'}),
        }

    def clean_monto(self):
        monto = self.cleaned_data.get('monto')

        if monto is None:
            raise ValidationError("El monto es obligatorio.")
        if monto < 0:
            raise ValidationError("El monto no puede ser negativo.")
        return monto
