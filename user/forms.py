from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from .models import User
from django import forms
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column
from  crispy_forms.bootstrap import FormActions

# Obtener el modelo de usuario personalizado
User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'correo@ejemplo.com'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'alias', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de usuario'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar mensajes de ayuda y clases de los campos
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

        # Mensajes de ayuda más amigables
        self.fields['password1'].help_text = '''
            <small class="form-text text-muted">
                <ul class="mb-0 ps-3">
                    <li>Tu contraseña no puede ser demasiado similar a tu información personal.</li>
                    <li>Debe contener al menos 8 caracteres.</li>
                    <li>No puede ser una contraseña común.</li>
                    <li>No puede ser entirely numérica.</li>
                </ul>
            </small>
        '''
        self.fields['password2'].help_text = '''
            <small class="form-text text-muted">
                Introduce la misma contraseña para verificación.
            </small>
        '''


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre de usuario o email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = 'Usuario o Email'


class CustomPasswordChangeForm(PasswordChangeForm):
    """Formulario personalizado para cambiar contraseña"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agregar clases Bootstrap a todos los campos
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control'
            })

        # Personalizar etiquetas y placeholders
        self.fields['old_password'].label = 'Contraseña actual'
        self.fields['old_password'].widget.attrs['placeholder'] = 'Contraseña actual'

        self.fields['new_password1'].label = 'Nueva contraseña'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Nueva contraseña'
        self.fields['new_password1'].help_text = '''
            <small class="form-text text-muted">
                <ul class="mb-0 ps-3">
                    <li>Tu contraseña no puede ser demasiado similar a tu información personal.</li>
                    <li>Debe contener al menos 8 caracteres.</li>
                    <li>No puede ser una contraseña común.</li>
                    <li>No puede ser completamente numérica.</li>
                </ul>
            </small>
        '''

        self.fields['new_password2'].label = 'Confirmar nueva contraseña'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirmar nueva contraseña'


class ProfileImageForm(forms.ModelForm):
    """Formulario específico para la imagen de perfil"""

    class Meta:
        model = User
        fields = ('profile_image',)
        widgets = {
            'profile_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
        labels = {
            'profile_image': 'Imagen de perfil'
        }


class UserRegistrationForm(CustomUserCreationForm):
    """Formulario de registro extendido si necesitas más campos"""

    accept_terms = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Acepto los términos y condiciones',
        error_messages={'required': 'Debes aceptar los términos y condiciones'}
    )

    class Meta(CustomUserCreationForm.Meta):
        fields = CustomUserCreationForm.Meta.fields + ('accept_terms',)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "alias", "email", "bio"]

    alias = forms.CharField(
        required=False,
        label="Alias/Nickname",
        widget=forms.TextInput(attrs={
            'placeholder': 'Tu alias opcional',
            'class': 'form-control'
        })
    )

    bio = forms.CharField(
        required=False,
        label="Biografía",
        widget=forms.Textarea(attrs={
            'placeholder': 'Cuéntanos algo sobre ti...',
            'rows': 3,
            'class': 'form-control'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Configurar campos deshabilitados
        self.fields["username"].disabled = True
        self.fields["email"].disabled = True

        # Configurar widgets para mantener el diseño Bootstrap
        self.fields["username"].widget.attrs.update({
            'class': 'form-control',
            'disabled': 'disabled'
        })
        self.fields["email"].widget.attrs.update({
            'class': 'form-control',
            'disabled': 'disabled'
        })

        # Configurar labels
        self.fields["username"].label = "Nombre de usuario"
        self.fields["email"].label = "Correo electrónico"

        # Configurar helper de Crispy Forms
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'form-label fw-bold'
        self.helper.field_class = 'mb-3'

        self.helper.layout = Layout(
            Row(
                Column(
                    'username',
                    css_class='col-md-6 mb-3'
                ),
                Column(
                    'alias',
                    css_class='col-md-6 mb-3'
                ),
            ),
            'email',
            'bio',
            FormActions(
                Submit('submit', 'Guardar Cambios', 
                      css_class='btn btn-principal',
                      onclick="this.disabled=true; this.form.submit();")
            )
        )

    def clean_username(self):
        return self.instance.username

    def clean_email(self):
        return self.instance.email


def validate_username_unique(value):
    """Validador para asegurar que el username sea único"""
    if User.objects.filter(username=value).exists():
        raise forms.ValidationError('Este nombre de usuario ya está en uso.')
    return value
