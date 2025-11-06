from django.db import models
from django.utils import timezone
from django.conf import settings

# FORMULARIOS


class DatosPersonales(models.Model):
    EDO_CIVIL_CHIOCES = [
        ('SOLTERO', 'Soltero'),
        ('CASADO', 'Casado'),
        ('DIVORCIADO', 'Divorciado'),
        ('VIUDO', 'Viudo'),
        ('UNION_LIBRE', 'Union libre'),
        ('OTRO', 'Otro'),
    ]

    ALCALDIA_CHIOCES = [
        ('ALVARO_OBREGON', 'Alvaro Obregon'),
        ('AZCAPOTZALCO', 'Azcapotzalco'),
        ('BENITO_JUAREZ', 'Benito Juárez'),
        ('COYOACAN', 'Coyoacan'),
        ('CUAJIMALPA', 'Cuajimalpa de Morelos'),
        ('CUAUHTEMOC', 'Cuauhtémoc'),
        ('GUSTAVO_A_MADERO', 'Gustavo A. Madero '),
        ('IZTACALCO', 'Iztacalco'),
        ('IZTAPALAPA', 'Iztapalapa'),
        ('LA_MAGDALENA_CONTRERAS', 'La Magdalena Contreras'),
        ('MIGUEL_HIDALGO', 'Miguel Hidalgo'),
        ('MILPA_ALTA', 'Milpa Alta'),
        ('TLAHUAC', 'Tlahuac'),
        ('TLALPAN', 'Tlalpan'),
        ('VENUSTIANO_CARRANZA', 'Venustiano Carranza'),
        ('XOCHIMILCO', 'Xochimilco'),
        ('OTRO', 'Otro'),
    ]

    GENERO_CHOICES = [
        ('MASCULINO', 'Masculino'),
        ('FEMENINO', 'Femenino'),
        ('NO_BINARIO', 'No binario'),
        ('NO_ESPECIFICAR', 'Prefiero no especificar'),
        ('OTRO', 'Otro'),
    ]

    nombre = models.CharField(max_length=100, null=True, blank=True)
    edad = models.IntegerField(null=False, blank=False,)
    genero = models.CharField(max_length=20, choices=GENERO_CHOICES, blank=False)
    estado_civil = models.CharField(max_length=30, choices=EDO_CIVIL_CHIOCES, blank=False)
    alcaldia = models.CharField(max_length=50, choices=ALCALDIA_CHIOCES, blank=True)
    fecha_registro = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if self.edad < 0:
            raise ValueError("La edad no puede ser negativa.")
        super().save(*args, **kwargs)


class EstadoActual(models.Model):
    SEMESTRES_CHOICES = [(i, str(i)) for i in range(1, 7)]  # 6 tuplas usandp for en linea

    OCUP_ACT_CHOICES = [
        ('ESTUDIANDO', 'Estudiando'),
        ('TRABAJANDO', 'Trabajando'), 
        ('AMBOS', 'Estudiando y Trabajando'),
        ('EMPRENDIENDO', 'Emprendiendo'),
        ('BUSCANDO_TRABAJO', 'Buscando Trabajo'),
        ('OTRO', 'Otro'),
    ]

    persona = models.OneToOneField(
        DatosPersonales,
        on_delete=models.CASCADE,
        related_name='estado_actual'
    )
    ultimo_sem_cursado = models.IntegerField(null=False, choices=SEMESTRES_CHOICES, blank=False)
    sem_posible_abandono = models.IntegerField(null=False, choices=SEMESTRES_CHOICES, blank=False)
    ocupacion_actual = models.CharField(max_length=100, choices=OCUP_ACT_CHOICES, blank=True)
    trabajo_actual = models.CharField(max_length=100, blank=True)
    apoyo_actual = models.CharField(max_length=100, blank=True)
    expectativas_carrera = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Estado de {self.persona.nombre}"


class FactoresDesercion(models.Model):
    IMPORTANCIA_CHOICES = [
        ('MUY_IMPORTANTE', 'Muy importante'),
        ('IMPORTANTE', 'Importante'),
        ('INTERMEDIO', 'Intermedio'),
        ('POCO_IMPORTANTE', 'Poco importante'),
        ('NO_IMPORTANTE', 'No importante'),
    ]

    persona = models.OneToOneField(
        DatosPersonales,
        on_delete=models.CASCADE,
        related_name='factores_desercion'
    )

    rendimiento = models.TextField(blank=False, null=False, choices=IMPORTANCIA_CHOICES)
    financieros = models.TextField(blank=False, null=False, choices=IMPORTANCIA_CHOICES)
    personales = models.TextField(blank=False, null=False, choices=IMPORTANCIA_CHOICES)
    costos = models.TextField(blank=False, null=False, choices=IMPORTANCIA_CHOICES)
    salud_mental = models.TextField(blank=False, null=False, choices=IMPORTANCIA_CHOICES)
    falta_apoyo = models.TextField(blank=False, null=False, choices=IMPORTANCIA_CHOICES)
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
    concepto = models.CharField(max_length=100, blank=True)
    descripcion = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.monto < 0:
            raise ValueError("El monto no puede ser negativo.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tipo} - {self.monto} ({self.cuenta.nombre})"
