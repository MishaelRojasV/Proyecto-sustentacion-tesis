from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from appevaluacion.models import Alumno, Evaluacion, Jurado, DetalleEvaluacion, Jornada, UNIDAD_CHOICES
from django.http import JsonResponse
from django.db.models import Count


@login_required(login_url='login')
def dashboard(request):

    jornada_id = request.GET.get('jornada', '')  
    #print(jornada_id)
    # Filtro de jornada si se seleccionó una
    if jornada_id:
        # Filtrar las evaluaciones por jornada seleccionada
        total_ponentes = Alumno.objects.filter(jornadas__idJornada=jornada_id).count()
        total_jurados = Jurado.objects.filter(jornadas__idJornada=jornada_id).count()
        total_sustentaciones = Evaluacion.objects.filter(jornada__idJornada=jornada_id).count()
        total_ponentes_evaluados = Evaluacion.objects.filter(jornada__idJornada=jornada_id, estadoFinal=True).count()
        total_ponentes_sinevaluar = Evaluacion.objects.filter(jornada__idJornada=jornada_id, estadoFinal=False).count()
    else:
        # Contadores generales si no se seleccionó ninguna jornada
        total_ponentes = Alumno.objects.count()
        total_jurados = Jurado.objects.count()
        total_sustentaciones = Evaluacion.objects.count()
        total_ponentes_evaluados = Evaluacion.objects.filter(estadoFinal=True).count()
        total_ponentes_sinevaluar = Evaluacion.objects.filter(estadoFinal=False).count()

    total_usuarios = User.objects.count()
    total_ponentes_sinsusten = total_ponentes - total_sustentaciones
    jornadas = Jornada.objects.all()  # Obtener todas las jornadas para el filtro

    contexto={
        'total_ponentes': total_ponentes,
        'total_jurados': total_jurados,
        'total_sustentaciones': total_sustentaciones,
        'total_ponentes_evaluados': total_ponentes_evaluados,
        'total_ponentes_sinevaluar': total_ponentes_sinevaluar,
        'total_ponentes_sinsusten': total_ponentes_sinsusten,
        'total_usuarios': total_usuarios,
        'jornadas': jornadas,
        'jornada_id': jornada_id,
        
    }

    return render(request, "dashboard/dashboard.html", contexto)

def obtener_datos_polar_area(request):
    
    jornada_id = request.GET.get('jornada', '')
    #print(jornada_id)
    # Aplica el filtro de jornada si se proporciona un ID de jornada
    if jornada_id:
        datos = (
            DetalleEvaluacion.objects.filter(estado=1, jornada_id=jornada_id)
            .values('cargo')
            .annotate(cantidad=Count('idDetEvaluacion'))
        )
    else:
        datos = (
            DetalleEvaluacion.objects.filter(estado=1)
            .values('cargo')
            .annotate(cantidad=Count('idDetEvaluacion'))
        )

    datos_list = list(datos)
    return JsonResponse(datos_list, safe=False)



def obtener_datos_grafico(request):
    # Obtener el ID de la jornada desde los parámetros de la solicitud
    jornada_id = request.GET.get('jornada','')  # Suponiendo que se pasa como parámetro GET
    print(jornada_id)

    # 1. Obtener las categorías de unidades
    unidades = [unidad[0] for unidad in UNIDAD_CHOICES]

    # 2. Contar alumnos por unidad con estadoFinal = True en Evaluacion
    if jornada_id:  # Verifica si jornada_id no está vacío
        alumnos_por_unidad = (
            Alumno.objects
            .filter(evaluacion__estadoFinal=1)  # Filtramos alumnos con evaluaciones donde estadoFinal es True (1)
            .filter(jornadas__idJornada=jornada_id)  # Filtramos por jornada seleccionada
            .values('unidad')  # Agrupamos por la unidad
            .annotate(total_alumnos=Count('idAlumno'))  # Contamos los alumnos por unidad
        )

        # 3. Contar el total de evaluaciones por unidad
        evaluaciones_por_unidad = (
            Evaluacion.objects
            .filter(jornada__idJornada=jornada_id)  # Filtramos por jornada seleccionada
            .values('alumno__unidad')  # Agrupamos por la unidad del alumno asociado
            .annotate(total_evaluaciones=Count('idEvaluacion'))  # Contamos evaluaciones por unidad
        )
    else:
        # Si jornada_id está vacío, no filtramos por jornada
        alumnos_por_unidad = (
            Alumno.objects
            .filter(evaluacion__estadoFinal=1)  # Filtramos alumnos con evaluaciones donde estadoFinal es True (1)
            .values('unidad')  # Agrupamos por la unidad
            .annotate(total_alumnos=Count('idAlumno'))  # Contamos los alumnos por unidad
        )

        evaluaciones_por_unidad = (
            Evaluacion.objects
            .values('alumno__unidad')  # Agrupamos por la unidad del alumno asociado
            .annotate(total_evaluaciones=Count('idEvaluacion'))  # Contamos evaluaciones por unidad
        )

    # 4. Formatear los datos para enviarlos al frontend
    datos_unidades = []
    for unidad in unidades:
        # Filtrar datos específicos para cada unidad
        total_alumnos = next((item['total_alumnos'] for item in alumnos_por_unidad if item['unidad'] == unidad), 0)
        total_evaluaciones = next((item['total_evaluaciones'] for item in evaluaciones_por_unidad if item['alumno__unidad'] == unidad), 0)
        
        # Agregar los datos de la unidad a la lista
        datos_unidades.append({
            'unidad': unidad,
            'total_alumnos': total_alumnos,
            'total_evaluaciones': total_evaluaciones
        })

        print(datos_unidades)

    # Devolver los datos en formato JSON
    return JsonResponse({'datos_unidades': datos_unidades})