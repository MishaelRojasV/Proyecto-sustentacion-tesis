from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

# Modelo para las Jornadas
class Jornada(models.Model):
    idJornada = models.AutoField(primary_key=True, null = False)
    codigoJornada = models.CharField(max_length=10, null=True)
    descripJornada = models.CharField(max_length=200, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    eliminado = models.BooleanField(default=False)
    activo = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.descripJornada}'

DOCTORADO_MAESTRIA_CHOICES = [
        ('DOCTORADO', 'DOCTORADO'),
        ('MAESTRIA', 'MAESTRIA')
]

UNIDAD_CHOICES = [
        ('UNIDAD DE CIENCIAS ECONOMICAS', 'UNIDAD DE CIENCIAS ECONOMICAS'),
        ('UNIDAD DE DERECHO', 'UNIDAD DE DERECHO'),
        ('UNIDAD DE FARMACIA Y BIOQUIMICA', 'UNIDAD DE FARMACIA Y BIOQUIMICA'),
        ('UNIDAD DE CIENCIAS MEDICAS', 'UNIDAD DE CIENCIAS MEDICAS'),
        ('UNIDAD DE CIENCIAS SOCIALES', 'UNIDAD DE CIENCIAS SOCIALES'),
        ('UNIDAD DE INGENIERIA', 'UNIDAD DE INGENIERIA'),
        ('UNIDAD DE CIENCIAS BIOLOGICAS', 'UNIDAD DE CIENCIAS BIOLOGICAS'),
        ('UNIDAD DE CIENCIAS FISICAS Y MATEMATICAS', 'UNIDAD DE CIENCIAS FISICAS Y MATEMATICAS'),
        ('UNIDAD DE ENFERMERIA', 'UNIDAD DE ENFERMERIA'),
        ('UNIDAD DE ING. QUIMICA', 'UNIDAD DE ING. QUIMICA'),
        ('UNIDAD DE AGROPECUARIAS', 'UNIDAD DE AGROPECUARIAS'),
        ('UNIDAD DE EDUCACION', 'UNIDAD DE EDUCACION'),
    ]


# Modelo para el Ponente
class Alumno(models.Model):
    idAlumno = models.AutoField(primary_key=True, null=False)   
    codigoAlumno = models.CharField(max_length=10, null=True)    
    nombre_ponente = models.CharField(max_length=100, null=False)    
    email = models.EmailField(max_length=100, blank=True, null=True)
    dni = models.CharField(max_length=15, null=True) 
    ncelular =  models.CharField(max_length=10, null=True)   
    ponencia = models.CharField(max_length=200, blank=True, null=True)  
    doctorado_maestria = models.CharField(max_length=200, choices=DOCTORADO_MAESTRIA_CHOICES, blank=True, null=True)   
    unidad = models.CharField(max_length=200, choices=UNIDAD_CHOICES, blank=True, null=True)
    mencion = models.CharField(max_length=200, blank=True, null=True)
    sala = models.CharField(max_length=100, blank=True, null=True)
    fecha_sustentacion = models.DateField(blank=True, null=True)
    hora_inicio_sustentacion = models.TimeField(blank=True, null=True)
    hora_fin_sustentacion = models.TimeField(blank=True, null=True)
    asesor = models.CharField(max_length=200, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    eliminado = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    jornadas = models.ManyToManyField(Jornada, related_name='alumnos')


    def clean(self):
        # Verificar que ambas horas estén presentes
        if self.hora_inicio_sustentacion and self.hora_fin_sustentacion:
            # Validar que la hora de inicio no sea mayor a la hora de fin
            if self.hora_inicio_sustentacion >= self.hora_fin_sustentacion:
                raise ValidationError(
                    _('La hora de inicio no puede ser mayor o igual a la hora de fin.')
                )   

    def __str__(self):
        return f'{self.nombre_ponente}'
    
    
CARGO = (('Presidente','Presidente'),
        ('Secretario','Secretario'),
        ('Vocal','Vocal'))


# Modelo para el Jurado
class Jurado(models.Model):
    idJurado = models.AutoField(primary_key=True, null=False)   
    codigoJurado = models.CharField(max_length=10, null=True) 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre_jurado = models.CharField(max_length=200, null=False)  
    dni  = models.CharField(max_length=20, null=True, unique=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=10, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    eliminado = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    jornadas = models.ManyToManyField(Jornada, related_name='jurados')


    def __str__(self):
        return f'{self.nombre_jurado}'

# Modelo para el Evaluación    
class Evaluacion(models.Model):
    idEvaluacion = models.AutoField(primary_key=True, null = False)
    codigoEvaluacion = models.CharField(max_length=10, null=False, unique=True )
    alumno = models.ForeignKey(Alumno, on_delete = models.CASCADE, null = False, unique=True)    
    estadoFinal = models.IntegerField(default=0)
    jornada = models.ForeignKey(Jornada, on_delete = models.CASCADE, null = False)   
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    eliminado = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f'Puntaje: {self.codigo}'
    
# Modelo para el Detalle de  la Evaluación    
class DetalleEvaluacion(models.Model):
    ORIGINALIDAD_CHOICES = [(i, i) for i in range(1, 6)]
    IMPORTANCIA_CHOICES = [(i, i) for i in range(1, 6)]
    COHERENCIA_CHOICES = [(i, i) for i in range(1, 6)]
    METODOLOGIA_CHOICES = [(i, i) for i in range(1, 6)]
    VALIDEZ_CHOICES = [(i, i) for i in range(1, 6)]
    DOMINIO_TEMA_CHOICES = [(i, i) for i in range(1, 6)]

    idDetEvaluacion = models.AutoField(primary_key=True, null = False)
    evaluacion = models.ForeignKey(Evaluacion, on_delete = models.CASCADE, null = False)
    jornada = models.ForeignKey(Jornada, on_delete = models.CASCADE, null = False)   
    jurado = models.ForeignKey(Jurado, on_delete = models.CASCADE, null = False)
    cargo = models.CharField(max_length=20, null = False)
    alumno = models.ForeignKey(Alumno, on_delete = models.CASCADE, null = False)
    originalidad = models.IntegerField(choices=ORIGINALIDAD_CHOICES, default=1)
    importancia = models.IntegerField(choices=IMPORTANCIA_CHOICES, default=1)
    coherencia = models.IntegerField(choices=COHERENCIA_CHOICES, default=1)
    metodologia = models.IntegerField(choices=METODOLOGIA_CHOICES, default=1)
    validez = models.IntegerField(choices=VALIDEZ_CHOICES, default=1)
    dominio_tema = models.IntegerField(choices=DOMINIO_TEMA_CHOICES, default=1)
    puntajeFinal = models.IntegerField(null=False, default=0) 
    estado = models.IntegerField(default=0)
    sugerencias = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    eliminado = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)




