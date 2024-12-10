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
    jornadas = forms.ModelMultipleChoiceField(
        queryset=Jornada.objects.filter(activo=True),  # Muestra solo las jornadas activas
        widget=forms.CheckboxSelectMultiple,  # O puedes usar un widget de selección múltiple
        required=False,
        label='Jornadas'
    )

    class Meta:
        model = Alumno
        fields = [
            'codigoAlumno',  
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
            'jornadas',  # Se añade el campo jornadas al formulario
        ]
        widgets = {
            'codigoAlumno': forms.TextInput(attrs={'placeholder': 'Ingrese código'}),
            'nombre_ponente': forms.TextInput(attrs={'placeholder': 'Ingrese nombres y apellidos'}),
            'dni': forms.TextInput(attrs={'placeholder': 'Ingrese DNI'}),
            'email': forms.TextInput(attrs={'placeholder': 'Ingrese correo electrónico'}),
            'ncelular': forms.TextInput(attrs={'placeholder': 'Ingrese celular'}),
            'ponencia': forms.TextInput(attrs={'placeholder': 'Ingrese título de la ponencia'}),
            'doctorado_maestria': forms.Select(attrs={'placeholder': 'Seleccione el programa'}),
            'unidad': forms.Select(attrs={'placeholder': 'Seleccione la unidad'}),
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
                'placeholder': 'Seleccione una hora de inicio'
            }),
            'hora_fin_sustentacion': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control',
                'placeholder': 'Seleccione una hora de fin'
            }),
        }
        labels = {
            'codigoAlumno': 'Código del Alumno',
            'nombre_ponente': 'Nombre del Ponente',
            'dni': 'DNI',
            'email': 'Correo Electrónico',
            'ncelular': 'Celular',
            'ponencia': 'Ponencia',
            'doctorado_maestria': 'Doctorado o Maestría',
            'unidad': 'Unidad',
            'mencion': 'Mención',
            'sala': 'Sala',
            'fecha_sustentacion': 'Fecha de Sustentación',
            'hora_inicio_sustentacion': 'Hora de Inicio',
            'hora_fin_sustentacion': 'Hora de Fin',
            'asesor': 'Asesor',
            'jornadas': 'Jornadas',
        }
    
    def save(self, commit=True):
        # Primero guardamos el alumno
        alumno = super().save(commit=False)
        
        if commit:
            alumno.save()  # Guardamos la instancia del Alumno

        # Asignamos las jornadas seleccionadas
        if self.cleaned_data['jornadas']:
            alumno.jornadas.set(self.cleaned_data['jornadas'])  # Establecemos la relación ManyToMany
        else:
            alumno.jornadas.clear()  # Limpiamos si no hay jornadas seleccionadas
        
        # Guardamos la instancia con las relaciones ManyToMany si `commit` es True
        self.save_m2m()
        return alumno


#-------------------------------------- Formulario para Jurado-------------------------------------
class JuradosForm(forms.ModelForm):
    jornadas = forms.ModelMultipleChoiceField(
        queryset=Jornada.objects.filter(activo=True),  # Muestra solo las jornadas activas
        widget=forms.CheckboxSelectMultiple,  # O puedes usar un widget de selección múltiple
        required=False,
        label='Jornadas'
    )

    class Meta:
        model = Jurado
        fields = [
            'codigoJurado', 
            'user',
            'nombre_jurado',            
            'dni',
            'email',
            'telefono',     
            'jornadas',  # Se añade el campo jornadas al formulario      
        ]
        widgets = {  
            'codigoJurado': forms.TextInput(attrs={}),                                
            'nombre_jurado': forms.TextInput(attrs={}),           
            'dni': forms.TextInput(attrs={}),
            'email': forms.TextInput(attrs={}),
            'telefono': forms.TextInput(attrs={}),            
        }
        labels = {
            'user': '',
            'nombre_jurado': 'Nombre del jurado',
            'dni': 'Dni',
            'email': 'Email',
            'telefono': 'Celular',  
            'jornadas': 'Jornadas', 
        }
        

    def __init__(self, *args, **kwargs):
        super(JuradosForm, self).__init__(*args, **kwargs)        
        usuario_sinasignacion = User.objects.exclude(jurado__isnull=False)
        self.fields['user'].queryset = usuario_sinasignacion

    def save(self, commit=True):
        # Guardar primero la instancia del jurado sin confirmar la relación ManyToMany
        jurado = super().save(commit=False)
        
        if commit:
            jurado.save()  # Guardamos la instancia del Jurado

        # Asignar las jornadas seleccionadas al jurado
        if self.cleaned_data['jornadas']:
            jurado.jornadas.set(self.cleaned_data['jornadas'])  # Establecemos la relación ManyToMany
        else:
            jurado.jornadas.clear()  # Limpiamos si no hay jornadas seleccionadas
        
        # Guardamos la instancia con las relaciones ManyToMany
        self.save_m2m()
        return jurado

#-------------------------------------- Formulario para Evaluacion-------------------------------------
class EvaluacionForm(forms.ModelForm):
    class Meta:
        model = Evaluacion
        fields = [
            'codigoEvaluacion',
            'alumno', 
            'jornada',            
        ]     
        labels = {
            'codigoEvaluacion': 'Codigo de Evaluación',
            'alumno': 'Datos del Ponente',
            'jornada': 'Jornada',
        }

    def __init__(self, *args, **kwargs):
        super(EvaluacionForm, self).__init__(*args, **kwargs)
        
        # Filtrar alumnos sin evaluación
        alumno_sinevaluacion = Alumno.objects.filter(eliminado=False).exclude(evaluacion__isnull=False)
        self.fields['alumno'].queryset = alumno_sinevaluacion
        
        # Filtrar jornadas activas
        jornadas_activas = Jornada.objects.filter(activo=True)
        self.fields['jornada'].queryset = jornadas_activas

class EditarEvaluacionForm(forms.ModelForm):
    class Meta:
        model = Evaluacion
        fields = [
            'codigoEvaluacion',
            'alumno', 
            'jornada',            
        ]     
        labels = {
            'codigoEvaluacion': 'Codigo de Evaluación',
            'alumno': 'Datos del Ponente',
            'jornada': 'Jornada',
        }


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

    # Validación del campo sugerencias
    def clean_sugerencias(self):
        sugerencias = self.cleaned_data.get('sugerencias')
        if not sugerencias or sugerencias.strip() == "":
            raise forms.ValidationError("El campo 'Sugerencias' es obligatorio.")
        return sugerencias