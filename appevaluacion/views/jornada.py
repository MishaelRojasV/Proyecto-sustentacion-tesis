from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from appevaluacion.models import Alumno
from appevaluacion.forms import *
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json


#---------------------------------------------Listar jornada---------------------------------------------
@login_required(login_url='login')
def listar_jornadas(request):
    return render(request, "jornada/listar.html")

@login_required(login_url='login')
def listar_jornadas_json(_request):    
    jornada = list(Jornada.objects.filter(eliminado=False).values())
    data = {'jornada':jornada}
    return JsonResponse(data)

#---------------------------------------------Añadir jornada---------------------------------------------
@csrf_exempt  # Si estás usando CSRF, esto no es recomendable, pero es útil para pruebas
def crear_jornada(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            codigo = data.get('codigoJornada')
            descripcion = data.get('descripJornada')
            activo = data.get('activo', True)  # Por defecto, activo es True

            # Crear una nueva jornada
            jornada = Jornada(codigoJornada=codigo, descripJornada=descripcion,eliminado=False, activo=activo)
            jornada.save()

            return JsonResponse({'status': 'success', 'message': 'Jornada creada correctamente!'}, status=201)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

# Actualiza estado del Usuario
@csrf_exempt
def update_jornada_status(request):
    jornada_id = request.POST.get('user_id')
    is_active = request.POST.get('is_active') == 'true'  
    try:
        jornada = Jornada.objects.get(idJornada=jornada_id)
        jornada.activo = is_active
        jornada.save()
        return JsonResponse({'status': 'success'})
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)