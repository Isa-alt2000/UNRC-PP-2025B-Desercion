from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import Group
from .models import User
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator
from django.db.models import Q


#Decorator que requiere que el usuario sea staff
def admin_required(function=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_staff,
        login_url='/acceso-denegado/'
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


@admin_required
def user_dashboard(request):
    # Obtener todos los usuarios
    users = User.objects.all().order_by('-date_joined')

    # Filtro de búsqueda
    query = request.GET.get('q')
    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(alias__icontains=query)
        )

    # Filtros adicionales
    filter_type = request.GET.get('filter')
    if filter_type == 'active':
        users = users.filter(is_active=True)
    elif filter_type == 'inactive':
        users = users.filter(is_active=False)
    elif filter_type == 'staff':
        users = users.filter(is_staff=True)
    elif filter_type == 'superusers':
        users = users.filter(is_superuser=True)

    # Estadísticas
    stats = {
        'active_users': User.objects.filter(is_active=True).count(),
        'inactive_users': User.objects.filter(is_active=False).count(),
        'staff_users': User.objects.filter(is_staff=True).count(),
        'superusers': User.objects.filter(is_superuser=True).count(),
    }

    # Paginación
    paginator = Paginator(users, 25)  # 25 usuarios por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'users': page_obj,
        'page_obj': page_obj,
        'is_paginated': paginator.num_pages > 1,
        **stats
    }

    return render(request, 'user_dashboard.html', context)
