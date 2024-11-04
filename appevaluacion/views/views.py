from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

def acceder(request):
    if request.method=="POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            nombre_usuario=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            usuario=authenticate(username=nombre_usuario, password=password)
            if usuario is not None:
                login(request, usuario)              
                request.session['userName_logged'] = usuario.first_name + ' '+ usuario.last_name
                request.session['user_logged'] = usuario.username                             
                return redirect('home')                                
            else:
                messages.error(request, "Credenciales incorrectas.")
        else:
            nombre_usuario=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            user_exits = (User.objects.filter(username=nombre_usuario).count()>0)
            if user_exits:
                messages.error(request, "Contraseña incorrecta.")
            else:
                messages.error(request, "Usuario incorrecto.")
    form=AuthenticationForm()
    return render(request, "login.html", {"form": form})


@login_required(login_url='login')
def home(request):
    return render(request, "home.html", {'user_logged':request.session['user_logged']})


@login_required(login_url='login')
def salir(request):    
    del request.session['user_logged']
    del request.session['userName_logged']
    logout(request)
    messages.info(request,"Sesión cerrada")
    return redirect("login")


""" def home(request):
    return render(request, "index.html") """