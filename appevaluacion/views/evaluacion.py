from appevaluacion.models import Alumno, Evaluacion, Jurado, DetalleEvaluacion
from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from appevaluacion.forms import *
from django.contrib import messages

#---------------------------------------------Listar Evaluaciones---------------------------------------------
@login_required(login_url='login')
def listar_evaluaciones(request): 
    jurados_presidente = Jurado.objects.filter(cargo='Presidente').filter(eliminado=False)
    jurados_secretario = Jurado.objects.filter(cargo='Secretario').filter(eliminado=False)
    jurados_vocal = Jurado.objects.filter(cargo='Vocal').filter(eliminado=False)
    return render(request, "evaluacion/listar.html", {'jurados_presidente':jurados_presidente,'jurados_secretario':jurados_secretario,'jurados_vocal':jurados_vocal})

@login_required(login_url='login')
def listar_evaluacion_json(_request):    
    evaluacion = list(Evaluacion.objects.values())
    alumnos = {alumno['idAlumno']: alumno for alumno in Alumno.objects.values()}
    data = {'evaluacion':evaluacion, 'alumnos':alumnos}
    return JsonResponse(data)

#---------------------------------------------Crear Evaluaciones---------------------------------------------
@login_required(login_url='login')
def crear_evaluacion(request):
    if request.method == 'POST':
        form = EvaluacionForm(request.POST)
        if form.is_valid():       
            form.save()             
            messages.success(request, f'Evaluacion Creada Exitosamente')
            return redirect('listar_evaluaciones')
        else:
            messages.error(request, "El formulario contiene errores. Por favor, corrija")
    else:
        form = EvaluacionForm()
    return render(request, 'evaluacion/agregar.html', {'form': form})


#---------------------------------------------Editar Evaluacion---------------------------------------------
@login_required(login_url='login')
def actualizar_evaluacion(request, id):
    evaluacion = get_object_or_404(Evaluacion, pk=id)
    if request.method == 'POST':
        form = EvaluacionForm(request.POST, instance=evaluacion)
        if form.is_valid():
           form.save()
           messages.success(request, f'Evaluación actualizada exitosamente.')
           return redirect('listar_evaluaciones')
        else:
           messages.error(request, "El formulario contiene errores. Por favor, corrija")
    else:
        form = EvaluacionForm(instance=evaluacion)
    return render(request, 'evaluacion/editar.html', {'form': form})

#------------------------------------------Eliminar Evaluacion ------------------------------------------------
@login_required
def eliminar_evaluacion(request, id):
    evaluacion = get_object_or_404(Evaluacion, pk=id)   
    if request.user.is_superuser:  
        evaluacion.delete()
        messages.success(request, 'Evaluación eliminado exitosamente.')
    else:
        messages.error(request, 'No tienes permiso para eliminar usuarios.')
    return redirect('listar_evaluaciones') 

#------------------------------------------ Asignar Jurado ------------------------------------------------
@csrf_exempt
def crear_detalle_evaluacion(request):

    if request.method == 'POST':         
        idEvaluacion = request.POST.get('id_evaluacion')
        print(idEvaluacion)
        juradoid = request.POST.get('id_jurado')
        print(juradoid)
        alumnoid = request.POST.get('id_alumno')
        print(alumnoid)
        
        try:
            detalle_evaluacion = DetalleEvaluacion.objects.create(
               eliminado=False,
               jurado_id=juradoid,
               evaluacion_id=idEvaluacion,
               alumno_id=alumnoid
            ) 
            return JsonResponse({'mensaje': f'Jurado Asignado'})
        except Jurado.DoesNotExist:
            return JsonResponse({'error': 'Jurado no encontrado'}, status=404)
        except ValueError:
            return JsonResponse({'error': 'ID no válido'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return render(request, 'evaluador/listar.html')


def evaluar(request):
    return render(request, "evaluacion/evaluacion.html")

