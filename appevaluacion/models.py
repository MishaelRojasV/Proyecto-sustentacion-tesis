from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Alumno(models.Model):
    idAlumno = models.AutoField(primary_key=True, null=False)   
    codigo = models.CharField(max_length=10, null=True)    
    nombre_ponente = models.CharField(max_length=100, null=False)    
    email = models.EmailField(max_length=100, blank=True, null=True)
    dni = models.CharField(max_length=15, null=True) 
    ncelular =  models.CharField(max_length=10, null=True)   
    ponencia = models.CharField(max_length=200, blank=True, null=True)  
    doctorado_maestria = models.CharField(max_length=200, blank=True, null=True)   
    unidad = models.CharField(max_length=200, blank=True, null=True)
    mencion = models.CharField(max_length=200, blank=True, null=True)
    sala = models.CharField(max_length=100, blank=True, null=True)
    fecha_sustentacion = models.DateField(blank=True, null=True)
    hora_inicio_sustentacion = models.TimeField(blank=True, null=True)
    hora_fin_sustentacion = models.TimeField(blank=True, null=True)
    asesor = models.CharField(max_length=200, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    eliminado = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.nombre_ponente}'
    
CARGO = (('Presidente','Presidente'),
         ('Secretario','Secretario'),
         ('Vocal','Vocal'))


class Jurado(models.Model):
    idJurado = models.AutoField(primary_key=True, null=False)   
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre_jurado = models.CharField(max_length=200, null=False)  
    dni  = models.CharField(max_length=20, null=True, unique=True)
    cargo = models.CharField(max_length=20, choices=CARGO)
    email = models.EmailField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=10, null=True)
    fecha_creacion = models.DateTimeField(auto_now=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    eliminado = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.nombre_jurado}'


    
class Evaluacion(models.Model):
    idEvaluacion = models.AutoField(primary_key=True, null = False)
    codigo = models.CharField(max_length=10, null=False, unique=True )
    alumno = models.ForeignKey(Alumno, on_delete = models.CASCADE, null = False, unique=True)       
    fecha_creacion = models.DateTimeField(auto_now=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    eliminado = models.BooleanField(default=False)

    def __str__(self):
        return f'Puntaje: {self.codigo}'
    

""" class DetalleEvaluacion(models.Model):
    idDetEvaluacion = models.AutoField(primary_key=True, null = False)
    evaluacion = models.ForeignKey(Evaluacion, on_delete = models.CASCADE, null = False)
    jurado = models.ForeignKey(Jurado, on_delete = models.CASCADE, null = False)
    alumno = models.ForeignKey(Alumno, on_delete = models.CASCADE, null = False)
    Originalidad = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=False, default=1)
    Importancia = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=False, default=1)
    Coherencia = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=False, default=1)
    Metodologia = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=False, default=1)
    Validez = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=False, default=1)
    Dominio_tema = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=False, default=1)   
    puntajeFinal = models.IntegerField(null=False, default=0) 
    sugerencias = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    eliminado = models.BooleanField(default=False)

    def __str__(self):
        return f'Puntaje: {self.idDetEvaluacion}' """

class DetalleEvaluacion(models.Model):
    ORIGINALIDAD_CHOICES = [(i, i) for i in range(1, 6)]
    IMPORTANCIA_CHOICES = [(i, i) for i in range(1, 6)]
    COHERENCIA_CHOICES = [(i, i) for i in range(1, 6)]
    METODOLOGIA_CHOICES = [(i, i) for i in range(1, 6)]
    VALIDEZ_CHOICES = [(i, i) for i in range(1, 6)]
    DOMINIO_TEMA_CHOICES = [(i, i) for i in range(1, 6)]

    idDetEvaluacion = models.AutoField(primary_key=True, null = False)
    evaluacion = models.ForeignKey(Evaluacion, on_delete = models.CASCADE, null = False)
    jurado = models.ForeignKey(Jurado, on_delete = models.CASCADE, null = False)
    alumno = models.ForeignKey(Alumno, on_delete = models.CASCADE, null = False)
    originalidad = models.IntegerField(choices=ORIGINALIDAD_CHOICES, default=1)
    importancia = models.IntegerField(choices=IMPORTANCIA_CHOICES, default=1)
    coherencia = models.IntegerField(choices=COHERENCIA_CHOICES, default=1)
    metodologia = models.IntegerField(choices=METODOLOGIA_CHOICES, default=1)
    validez = models.IntegerField(choices=VALIDEZ_CHOICES, default=1)
    dominio_tema = models.IntegerField(choices=DOMINIO_TEMA_CHOICES, default=1)
    puntajeFinal = models.IntegerField(null=False, default=0) 
    sugerencias = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    eliminado = models.BooleanField(default=False)
