# forum/views.py
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count, Q
from django.contrib.auth import get_user_model

User = get_user_model()


def home(request):
    return render(request, "home.html")