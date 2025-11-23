from django import forms
from django.core.exceptions import ValidationError
from .models import Cuenta, Movimiento


# FINANZAS
class CuentaForm(forms.ModelForm):
    class Meta:
        model = Cuenta
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la cuenta',
                'id': 'id_nombre',
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Breve descripción (opcional)',
                'rows': '3',
                'id': 'id_descripcion',
            }),
        }


class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = ['tipo', 'monto', 'concepto', 'descripcion', 'fecha']
        widgets = {
            'tipo': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_tipo',
            }),
            'monto': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.01',
                'id': 'id_monto',
            }),
            'concepto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Concepto del movimiento',
                'id': 'id_concepto',
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción detallada (opcional)',
                'rows': '5',
                'id': 'id_descripcion',
            }),
            'fecha': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'id': 'id_fecha',
            }),
        }

    def clean_monto(self):
        monto = self.cleaned_data.get('monto')

        if monto is None:
            raise ValidationError("El monto es obligatorio.")
        if monto < 0:
            raise ValidationError("El monto no puede ser negativo.")
        return monto

