from django import forms 
from django.forms import fields 
from appevaluacion.models import *
from django.contrib.auth.models import User
import datetime

#-------------------------------------- Formulario para Crear Uusario-------------------------------------
class CrearUserForm(forms.ModelForm):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    first_name = forms.CharField(label='Nombres (opcional)', required=False)
    last_name = forms.CharField(label='Apellidos (opcional)', required=False)
    email = forms.EmailField(label='Correo Electrónico (opcional)', required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'is_superuser', 'is_active']
        help_texts = {
            'is_active': ('Indica si este usuario debe ser tratado como activo. Desactive esto en lugar de eliminar cuentas.'),
            'is_superuser': ('Designa que este usuario tiene todos los permisos sin asignarlos explícitamente.'),
        }

    def __init__(self, *args, **kwargs):
        super(CrearUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['password'].required = True

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

#-------------------------------Formulario para Editar Uusario----------------------------------
class EditarUserForm(forms.ModelForm):    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_superuser', 'is_active']
        help_texts = {
            'is_active': ('Indica si este usuario debe ser tratado como activo. Desactive esto en lugar de eliminar cuentas.'),
            'is_superuser': ('Designa que este usuario tiene todos los permisos sin asignarlos explícitamente.'),
        }



#-------------------------------------- Formulario para Crear y Editar Alumno-------------------------------------
class AlumnosForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = [
            'codigo',
            'nombre_ponente',            
            'dni',
            'email',
            'ncelular',
            'ponencia',
            'doctorado_maestria',
            'unidad',            
            'mencion',
            'sala',            
            'fecha_sustentacion',            
            'hora_inicio_sustentacion',
            'hora_fin_sustentacion',
            'asesor',            
        ]
        widgets = {                            
            'codigo': forms.TextInput(attrs={'placeholder': 'Ingrese codigo'}),
            'nombre_ponente': forms.TextInput(attrs={'placeholder': 'Ingrese nombres y apellidos'}),           
            'dni': forms.TextInput(attrs={'placeholder': 'Ingrese dni'}),
            'email': forms.TextInput(attrs={'placeholder': 'Ingrese correo electronico'}),
            'ncelular': forms.TextInput(attrs={'placeholder': 'Ingrese celular'}),
            'ponencia': forms.TextInput(attrs={'placeholder': 'Ingrese titulo de la ponencia'}),
            'doctorado_maestria': forms.TextInput(attrs={'placeholder': 'Ingrese el programa'}),            
            'unidad': forms.TextInput(attrs={'placeholder': 'Ingrese unidad'}),
            'mencion': forms.TextInput(attrs={'placeholder': 'Ingrese mención'}),
            'sala': forms.TextInput(attrs={'placeholder': 'Ingrese sala'}),
            'fecha_sustentacion': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control',
                'placeholder': 'Seleccione una fecha'
            }),
            'hora_inicio_sustentacion': forms.TimeInput(attrs={
                'type': 'time', 
                'class': 'form-control',
                'placeholder': 'Seleccione una hora inicio'
            }),
            'hora_fin_sustentacion': forms.TimeInput(attrs={
                'type': 'time', 
                'class': 'form-control',
                'placeholder': 'Seleccione una hora final'
            }),
        }
        labels = {
            'codigo': 'Codigo',
            'nombre_ponente': 'Nombre ponente',
            'dni': 'Dni',
            'email': 'Email',
            'ncelular': 'Ncelular',
            'ponencia': 'Ponencia',
            'doctorado_maestria': 'Doctorado maestria',
            'unidad': 'Unidad',
            'mencion': 'Mencion',
            'sala': 'Sala',
            'fecha_sustentacion': 'Fecha sustentacion',
            'hora_inicio_sustentacion': 'Hora Inicio',
            'hora_fin_sustentacion': 'Hora Fin',
            'asesor': 'Asesor',
        }

#-------------------------------------- Formulario para Jurado-------------------------------------
class JuradosForm(forms.ModelForm):
    class Meta:
        model = Jurado
        fields = [
            'user',
            'nombre_jurado',            
            'dni',
            'email',
            'telefono',           
        ]
        widgets = {                                  
            'nombre_jurado': forms.TextInput(attrs={'placeholder': 'Ingrese nombres y apellidos'}),           
            'dni': forms.TextInput(attrs={'placeholder': 'Ingrese dni'}),
            'email': forms.TextInput(attrs={'placeholder': 'Ingrese correo electronico'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Ingrese celular'}),            
        }
        labels = {
            'user': 'Nombre de Usuario',
            'nombre_jurado': 'Nombre del jurado',
            'dni': 'Dni',
            'email': 'Email',
            'telefono': 'Telefono/Celular',   
        }

#-------------------------------------- Formulario para Evaluacion-------------------------------------
class EvaluacionForm(forms.ModelForm):
    class Meta:
        model = Evaluacion
        fields = [
            'codigo',
            'alumno',            
            'eliminado',                     
        ]     
        labels = {
            'codigo': 'Codigo de Evaluación',
            'alumno': 'Datos del Ponente',
            'eliminado': 'Eliminado',  
        }

    def __init__(self, *args, **kwargs):
        super(EvaluacionForm, self).__init__(*args, **kwargs)        
        alumno_sinevaluacion = Alumno.objects.filter(eliminado=False).exclude(evaluacion__isnull=False)
        self.fields['alumno'].queryset = alumno_sinevaluacion



class DetalleEvaluacionForm(forms.ModelForm):
    class Meta:
        model = DetalleEvaluacion
        fields = ['originalidad', 'importancia', 'coherencia', 'metodologia', 'validez', 'dominio_tema', 'sugerencias']
        widgets = {
            'originalidad': forms.RadioSelect,
            'importancia': forms.RadioSelect,
            'coherencia': forms.RadioSelect,
            'metodologia': forms.RadioSelect,
            'validez': forms.RadioSelect,
            'dominio_tema': forms.RadioSelect,
            'sugerencias': forms.Textarea(attrs={'rows': 4, 'cols': 40}),

        }
        labels = {
            'originalidad': 'Originalidad',
            'importancia': 'Importancia',
            'coherencia': 'Coherencia',
            'metodologia': 'Metodología',
            'validez': 'Validez',
            'dominio_tema': 'Dominio del tema',
            'sugerencias': 'Sugerencias',
        }