from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.contrib import messages
from .models import Cuenta, Movimiento
from .forms import CuentaForm, MovimientoForm
from django.contrib.auth.decorators import login_required

