from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.decorators import login_required
from appevaluacion.models import Alumno
from appevaluacion.forms import *
from django.contrib import messages

#---------------------------------------------Listar Jurado---------------------------------------------
@login_required(login_url='login')
def listar_jurados(request):
    return render(request, "jurado/listar.html")

@login_required(login_url='login')
def listar_jurado_json(_request):    
    jurado = list(Jurado.objects.filter(eliminado=False).values())
    data = {'jurado':jurado}
    return JsonResponse(data)

#---------------------------------------------Crear Jurado---------------------------------------------
@login_required(login_url='login')
def crear_jurado(request):
    if request.method == 'POST':
        form = JuradosForm(request.POST)
        if form.is_valid():       
            form.save()             
            messages.success(request, f'Jurado Creado Exitosamente')
            return redirect('listar_jurados')
        else:
            messages.error(request, "El formulario contiene errores. Por favor, corrija")
    else:
        form = JuradosForm()
    return render(request, 'jurado/agregar.html', {'form': form})


#---------------------------------------------Editar Jurado---------------------------------------------
@login_required(login_url='login')
def actualizar_jurado(request, id):
    jurado = get_object_or_404(Jurado, pk=id)
    if request.method == 'POST':
        form = JuradosForm(request.POST, instance=jurado)
        if form.is_valid():
           form.save()
           messages.success(request, f'Jurado actualizado exitosamente.')
           return redirect('listar_jurados')
        else:
           messages.error(request, "El formulario contiene errores. Por favor, corrija")
    else:
        form = JuradosForm(instance=jurado)
    return render(request, 'jurado/editar.html', {'form': form})

#------------------------------------------Eliminar USuario ------------------------------------------------
@login_required
def eliminar_jurado(request, id):
    jurado = get_object_or_404(Jurado, pk=id)   
    if request.user.is_superuser:  
        jurado.eliminado = True
        jurado.save()
        messages.success(request, 'Jurado eliminado exitosamente.')
    else:
        messages.error(request, 'No tienes permiso para eliminar usuarios.')
    return redirect('listar_jurados')