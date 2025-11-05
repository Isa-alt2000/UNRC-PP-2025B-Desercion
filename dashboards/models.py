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
    """Cuenta o fuente/tipd de dinero"""
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(
        max_length=50,
        choices=[
            ('AHORRO', 'Ahorro'),
            ('CREDITO', 'Crédito'),
            ('EFECTIVO', 'Efectivo'),
            ('OTRO', 'Otro')
        ],
        default='OTRO'
    )
    saldo_inicial = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"

    @property
    def saldo_actual(self):
        ingresos = sum(i.monto for i in self.ingreso_set.all())
        egresos = sum(e.monto for e in self.egreso_set.all())
        return self.saldo_inicial + ingresos - egresos


class CategoriaIngreso(models.TextChoices):
    BECA = 'BECA', 'Beca'
    TRABAJO = 'TRABAJO', 'Trabajo'
    APOYO_FAMILIAR = 'APOYO_FAMILIAR', 'Apoyo familiar'
    OTRO = 'OTRO', 'Otro'


class CategoriaEgreso(models.TextChoices):
    COLEGIATURA = 'COLEGIATURA', 'Colegiatura'
    TRANSPORTE = 'TRANSPORTE', 'Transporte'
    ALIMENTACION = 'ALIMENTACION', 'Alimentación'
    RENTA = 'RENTA', 'Renta'
    OCIO = 'OCIO', 'Ocio'
    OTRO = 'OTRO', 'Otro'


class Ingreso(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE, null=True, blank=True)
    categoria = models.CharField(
        max_length=20,
        choices=CategoriaIngreso.choices,
        default=CategoriaIngreso.OTRO
    )
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.categoria} - ${self.monto}"


class Egreso(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE, null=True, blank=True)
    categoria = models.CharField(
        max_length=20,
        choices=CategoriaEgreso.choices,
        default=CategoriaEgreso.OTRO
    )
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.categoria} - ${self.monto}"


class ResumenMensual(models.Model):
    """Modelo auxiliar para calcular balance mensual"""
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mes = models.IntegerField()  # 1 a 12
    anio = models.IntegerField()
    total_ingresos = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_egresos = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @property
    def balance(self):
        return self.total_ingresos - self.total_egresos

    @property
    def riesgo(self):
        if self.balance < 0:
            return "Alto"
        elif self.balance < 500:
            return "Moderado"
        return "Bajo"

    def __str__(self):
        return f"{self.usuario.username} - {self.mes}/{self.anio}"
