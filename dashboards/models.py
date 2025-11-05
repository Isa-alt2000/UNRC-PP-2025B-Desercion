from django.db import models
from django.utils import timezone
from django.conf import settings

# FORMULARIOS


class DatosPersonales(models.Model):
    nombre = models.CharField(max_length=100)
    edad = models.IntegerField(null=True, blank=True)
    genero = models.CharField(max_length=20, blank=True)
    estado_civil = models.CharField(max_length=30, blank=True)
    alcaldia = models.CharField(max_length=100, blank=True)
    fecha_registro = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre


class EstadoActual(models.Model):
    persona = models.OneToOneField(
        DatosPersonales,
        on_delete=models.CASCADE,
        related_name='estado_actual'
    )
    ultimo_sem_cursado = models.IntegerField(null=True, blank=True)
    sem_posible_abandono = models.IntegerField(null=True, blank=True)
    ocupacion_actual = models.CharField(max_length=100, blank=True)
    trabajo_actual = models.CharField(max_length=100, blank=True)
    apoyo_actual = models.CharField(max_length=100, blank=True)
    expectativas_carrera = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Estado de {self.persona.nombre}"


class FactoresDesercion(models.Model):
    persona = models.OneToOneField(
        DatosPersonales,
        on_delete=models.CASCADE,
        related_name='factores_desercion'
    )
    rendimiento = models.TextField(blank=True)
    financieros = models.TextField(blank=True)
    personales = models.TextField(blank=True)
    costos = models.TextField(blank=True)
    salud_mental = models.TextField(blank=True)
    falta_apoyo = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Factores de importancia de {self.persona.nombre}"


class PreguntasAbiertas(models.Model):
    persona = models.OneToOneField(
        DatosPersonales,
        on_delete=models.CASCADE,
        related_name='preguntas_abiertas'
    )
    continuar_estudios = models.TextField(blank=True)
    mensaje_ayuda = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Preguntas de {self.persona.nombre}"

# FINANZAS


class Cuenta(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cuentas'
    )
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Movimiento(models.Model):
    TIPO_CHOICES = [
        ('INGRESO', 'Ingreso'),
        ('EGRESO', 'Egreso'),
    ]

    cuenta = models.ForeignKey(
        Cuenta,
        on_delete=models.CASCADE,
        related_name='movimientos'
    )
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField(default=timezone.now)
    descripcion = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.monto < 0:
            raise ValueError("El monto no puede ser negativo.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tipo} - {self.monto} ({self.cuenta.nombre})"
