from datetime import date
from typing import List

from django.db.models import Sum, Q
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Movimiento


def _first_of_month(d: date) -> date:
    return date(d.year, d.month, 1)


def _add_months(d: date, months: int) -> date:
    year = d.year + (d.month - 1 + months) // 12
    month = (d.month - 1 + months) % 12 + 1
    return date(year, month, 1)


def _months_range(start: date, end: date) -> List[date]:
    start = _first_of_month(start)
    end = _first_of_month(end)
    months = []
    cur = start
    while cur <= end:
        months.append(cur)
        cur = _add_months(cur, 1)
    return months


def aggregate_movimientos_por_mes(movimientos_qs):
    """
    Devuelve un diccionario con claves month (date) y valores (ingresos, egresos).
    Usa una consulta con `TruncMonth` y agregaciones condicionales para aprovechar
    las capacidades de la base de datos.
    """
    raw = (
        movimientos_qs
        .annotate(month=TruncMonth('fecha'))
        .values('month')
        .annotate(
            ingresos=Sum('monto', filter=Q(tipo='INGRESO')),
            egresos=Sum('monto', filter=Q(tipo='EGRESO')),
        )
        .order_by('month')
    )

    month_map = {}
    for r in raw:
        m = r['month']
        if hasattr(m, 'date'):
            m = m.date()
        m = _first_of_month(m)
        ingresos = r['ingresos'] or 0
        egresos = r['egresos'] or 0
        month_map[m] = (ingresos, egresos)

    return month_map


def compute_savings_series(month_map, start: date, end: date):
    """
    Dado un mapa month -> (ingresos, egresos) y un rango temporal, devuelve listas
    ordenadas: months, ahorro_mensual, ahorro_acumulado
    """
    months = _months_range(start, end)
    ahorro_mensual = []
    ahorro_acumulado = []
    acumulado = 0
    for m in months:
        ingresos, egresos = month_map.get(m, (0, 0))
        ahorro = ingresos - egresos
        acumulado += ahorro
        ahorro_mensual.append(float(ahorro))
        ahorro_acumulado.append(float(acumulado))

    return months, ahorro_mensual, ahorro_acumulado


def project_savings(last_month: date, last_accumulated: float, last_month_saving: float,
                    mode: str = 'constante', n: int = 3, months_ahead: int = 12):
    """
    Proyecta ahorro mensual hacia el futuro.
    - modo 'constante': usa `last_month_saving` repetido.
    - modo 'variable': usa el promedio de los últimos `n` meses (ya pasado por parámetro)

    Devuelve: projected_months, projected_savings_monthly, projected_savings_cumulative
    """
    if mode not in ('constante', 'variable'):
        mode = 'constante'

    projected_months = [_add_months(last_month, i) for i in range(1, months_ahead + 1)]

    if mode == 'constante':
        monthly_vals = [float(last_month_saving)] * months_ahead
    else:
        monthly_vals = [float(last_month_saving)] * months_ahead

    cum = []
    acc = float(last_accumulated)
    for v in monthly_vals:
        acc += v
        cum.append(float(acc))

    return projected_months, monthly_vals, cum


@login_required
def plan_ahorro_view(request, cuenta_id):
    """
    Vista que calcula el ahorro mensual, acumulado y una proyección.

    Parámetros URL:
    - `cuenta_id`: id de la cuenta para filtrar movimientos (obligatorio).

    Parámetros GET opcionales:
    - `mode`: 'constante' o 'variable' (por defecto 'constante').
    - `n`: número de meses para promedio cuando `mode='variable'` (por defecto 3).
    - `months_ahead`: horizonte de proyección en meses (por defecto 12).
    """
    mode = request.GET.get('mode', 'constante')
    try:
        n = int(request.GET.get('n', 3))
    except (TypeError, ValueError):
        n = 3
    try:
        monto_constante = float(request.GET.get('monto_constante', 0))
    except (TypeError, ValueError):
        monto_constante = 0.0
    try:
        months_ahead = int(request.GET.get('months_ahead', 12))
    except (TypeError, ValueError):
        months_ahead = 12

    # Filtrar movimientos de la cuenta del usuario
    movimientos = Movimiento.objects.filter(
        cuenta_id=cuenta_id,
        cuenta__usuario=request.user
    )

    if not movimientos.exists():
        # No hay movimientos: generar últimos 6 meses con 0 para continuidad
        today = date.today()
        end = _first_of_month(today)
        start = _add_months(end, -5)
        month_map = {}
    else:
        month_map = aggregate_movimientos_por_mes(movimientos)
        months_present = sorted(month_map.keys())
        start = months_present[0]
        end = months_present[-1]

    months, ahorro_mensual, ahorro_acumulado = compute_savings_series(month_map, start, end)

    if len(ahorro_mensual) > 0:
        last_month_saving = ahorro_mensual[-1]
        last_accumulated = ahorro_acumulado[-1]
    else:
        last_month_saving = 0.0
        last_accumulated = 0.0

    if mode == 'constante':
        # Modo constante: usar el monto ingresado por el usuario
        last_month_saving_for_projection = monto_constante
    else:
        # Modo variable: usar promedio de últimos N meses
        recent = ahorro_mensual[-n:] if n > 0 else ahorro_mensual
        if recent:
            avg = sum(recent) / len(recent)
        else:
            avg = last_month_saving
        last_month_saving_for_projection = avg

    projected_months, projected_savings_monthly, projected_savings_cumulative = project_savings(
        end if movimientos.exists() else _first_of_month(date.today()),
        last_accumulated,
        last_month_saving_for_projection,
        mode=mode,
        n=n,
        months_ahead=months_ahead,
    )

    months_str = [m.strftime('%Y-%m') for m in months]
    projected_months_str = [m.strftime('%Y-%m') for m in projected_months]

    historical = list(zip(months_str, ahorro_mensual, ahorro_acumulado))
    projected = list(zip(projected_months_str, projected_savings_monthly,
                         projected_savings_cumulative))

    months_str = [m.strftime('%Y-%m') for m in months]
    projected_months_str = [m.strftime('%Y-%m') for m in projected_months]

    historical = list(zip(months_str, ahorro_mensual, ahorro_acumulado))
    projected = list(zip(projected_months_str, projected_savings_monthly,
                         projected_savings_cumulative))

    context = {
        'months': months_str,
        'ahorro_mensual': ahorro_mensual,
        'ahorro_acumulado': ahorro_acumulado,
        'projected_months': projected_months_str,
        'ahorro_proyectado_mensual': projected_savings_monthly,
        'ahorro_proyectado_acumulado': projected_savings_cumulative,
        'projection_mode': mode,
        'projection_n': n,
        'monto_constante': monto_constante,
        'historical': historical,
        'projected': projected,
        'months_ahead': months_ahead,
    }

    return render(request, 'prediccion.html', context)
