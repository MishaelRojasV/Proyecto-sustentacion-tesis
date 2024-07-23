from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from appevaluacion.forms import *


#---------------------------------------------Listar usuarios---------------------------------------------
@login_required(login_url='login')
def listar_usuarios(request):
    return render(request, 'usuario/listar.html')

@login_required(login_url='login')
def listar_usuarios_json(request):       
    usuarios = list(User.objects.values())
    data = {'usuarios':usuarios}
    return JsonResponse(data)

#---------------------------------------------Crear usuarios---------------------------------------------
@login_required(login_url='login')
def creacion_usuario(request):
    if request.method == 'POST':
        form = CrearUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']         
            form.save() 
            messages.success(request, f'Usuario {username} creado exitosamente.')
            return redirect('listar_usuarios')
        else:
            messages.error(request, "El formulario contiene errores. Por favor, corrija")
    else:
        form = CrearUserForm()
    return render(request, 'usuario/agregar.html', {'form': form})

#---------------------------------------------Editar usuarios---------------------------------------------
@login_required(login_url='login')
def actualizar_usuario(request, id):
    usuario = get_object_or_404(User, pk=id)
    if request.method == 'POST':
        form = EditarUserForm(request.POST, instance=usuario)
        if form.is_valid():
           form.save()
           username = form.cleaned_data.get('username')
           messages.success(request, f'Usuario {username} actualizado exitosamente.')
           return redirect('listar_usuarios')
        else:
           messages.error(request, "El formulario contiene errores. Por favor, corrija")
    else:
        form = EditarUserForm(instance=usuario)
    return render(request, 'usuario/editar.html', {'form': form})

#------------------------------------------Eliminar USuario ------------------------------------------------
@login_required
def eliminar_usuario(request, id):
    usuario = get_object_or_404(User, pk=id)   
    if request.user.is_superuser:  
        usuario.delete()
        messages.success(request, 'Usuario eliminado exitosamente.')
    else:
        messages.error(request, 'No tienes permiso para eliminar usuarios.')
    return redirect('listar_usuarios')