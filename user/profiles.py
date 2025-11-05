from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ProfileForm, CustomPasswordChangeForm, ProfileImageForm, CustomAuthenticationForm, CustomUserCreationForm
from .models import User
from django.contrib import messages


@login_required
def profile_view(request):
    user = request.user
    profile_form = ProfileForm(instance=user)
    password_form = CustomPasswordChangeForm(user)
    image_form = ProfileImageForm(instance=user)

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'profile':
            profile_form = ProfileForm(request.POST, instance=user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Perfil actualizado correctamente.')
                return redirect('users:perfil')
            else:
                messages.error(request, 'Por favor corrige los errores en el formulario.')

        elif form_type == 'image':
            image_form = ProfileImageForm(request.POST, request.FILES, instance=user)
            if image_form.is_valid():
                image_form.save()
                messages.success(request, 'Imagen de perfil actualizada.')
                return redirect('users:perfil')
            else:
                messages.error(request, 'Error al subir la imagen.')

        elif form_type == 'delete_image':
            if user.profile_image:
                user.profile_image.delete()
                user.profile_image = None
                user.save()
                messages.success(request, 'Imagen de perfil eliminada.')
            return redirect('users:perfil')

        elif form_type == 'password':
            password_form = CustomPasswordChangeForm(user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Contraseña cambiada correctamente.')
                return redirect('users:perfil')
            else:
                messages.error(request, 'Error al cambiar la contraseña.')

    context = {
        'profile_form': profile_form,
        'password_form': password_form,
        'image_form': image_form,
    }

    return render(request, 'perfil.html', context)


def user_profile(request, profile_slug):
    """Vista pública del perfil de cualquier usuario"""
    user = get_object_or_404(User, profile_slug=profile_slug)

    # Verificar si es el perfil propio para mostrar opciones de edición
    is_own_profile = request.user.is_authenticated and request.user == user

    context = {
        'profile_user': user,
        'is_own_profile': is_own_profile,
    }
    return render(request, 'profile_public.html', context)


@login_required
def my_profile(request):
    """Redirige al usuario a su propio perfil"""
    return redirect('public_profile', profile_slug=request.user.profile_slug)
