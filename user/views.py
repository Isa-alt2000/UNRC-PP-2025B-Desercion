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
