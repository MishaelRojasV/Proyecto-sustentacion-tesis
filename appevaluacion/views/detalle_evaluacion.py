from django.shortcuts import render, redirect,  get_object_or_404
from appevaluacion.models import Alumno, Evaluacion, Jurado, DetalleEvaluacion
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from appevaluacion.forms import  DetalleEvaluacionForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings


#---------------------------------------------Listar Evaluaciones---------------------------------------------
@login_required(login_url='login')
def listar_detalleevaluaciones(request): 
    # Obtener los filtros de la solicitud GET
    ponente_filtro = request.GET.get('ponente', '')
    jurado_filtro = request.GET.get('jurado', '')
    cargo_filtro = request.GET.get('cargo', '')

    # Verificar si el usuario es administrador
    if request.user.is_superuser:
        # Si el usuario es administrador, obtener todas las evaluaciones
        datos = DetalleEvaluacion.objects.all()
    else:
        try:
            # Obtener el evaluador asociado al usuario
            jurado = request.user.jurado
            # Filtrar las evaluaciones por el evaluador
            datos = DetalleEvaluacion.objects.filter(jurado=jurado)
        except ObjectDoesNotExist:
            # Redirigir a una página de error o mostrar un mensaje en la plantilla
            return render(request, 'home.html')

    # Aplicar filtros adicionales
    if ponente_filtro:
        datos = datos.filter(alumno__nombre_ponente__icontains=ponente_filtro)
    if jurado_filtro:
        datos = datos.filter(jurado__nombre_jurado__icontains=jurado_filtro)
    if cargo_filtro:
        datos = datos.filter(cargo=cargo_filtro)

    # Paginar los resultados
    paginator = Paginator(datos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "DetalleEvaluacion/listar.html",  {'page_obj': page_obj})



#--------------------------------------------- Proceso de Evaluar---------------------------------------------
@login_required(login_url='login')
def evaluar_sustentacion(request, pk):
    # Obtener la instancia de la evaluación correspondiente
    detalle_evaluacion = get_object_or_404(DetalleEvaluacion, pk=pk)
    #detalle_evaluacion = get_object_or_404(Evaluacion, pk=pk)
    # Obtener la instancia de Postulante asociada a la evaluación
    alumno = detalle_evaluacion.alumno
    jurado = detalle_evaluacion.jurado    
    evaluacion = detalle_evaluacion.evaluacion
    # Crear un diccionario con los datos del postulante
    alumnodata = {
        'nombre_ponente': alumno.nombre_ponente,
        'dni': alumno.dni,
        'doctorado_maestria': alumno.doctorado_maestria,
        'unidad' : alumno.unidad,
        'mencion' : alumno.mencion,        
        'ponencia' : alumno.ponencia,
        'sala' : alumno.sala,
        'fecha_sustentacion' : alumno.fecha_sustentacion,
        'hora_inicio_sustentacion' : alumno.hora_inicio_sustentacion,
        'hora_fin_sustentacion' : alumno.hora_fin_sustentacion,
        'asesor' : alumno.asesor,
    }

    
    if request.method == 'POST':
        # Si la solicitud es POST, crea el formulario con los datos enviados
        form = DetalleEvaluacionForm(request.POST, instance=detalle_evaluacion)       
        if form.is_valid():          
            # Si el formulario es válido, guarda los datos en la base de datos
            detalle_evaluacion = form.save(commit=False)
            detalle_evaluacion.evaluacion = evaluacion
            detalle_evaluacion.jurado = jurado
            detalle_evaluacion.alumno = alumno
            detalle_evaluacion.save()

            # Enviar correo electrónico al alumno
            subject = 'SUSTENTACIÓN DE TESIS | Sugerencias'
            message = f'Hola {alumno.nombre_ponente},\n\nHemos recibido las siguientes sugerencias para tu evaluación:\n\n{detalle_evaluacion.sugerencias}'
            html_message = f"""
                <html>
                <body>
                    <h2>SUGERENCIAS DEL JURADO</h2>
                    <p>Buenas noches <strong>{alumno.nombre_ponente}</strong>, nos comunicamos para informarle las sugerencias con respecto a su sustentación realizada</p>
                    <br>
                    <p>Ponencia: <strong>{alumno.ponencia}</strong></p>
                    <p>Fecha de Sustentación: <strong>{alumno.fecha_sustentacion}</strong></p>
                    <p>Hora: <strong>{alumno.hora_inicio_sustentacion}- {alumno.hora_fin_sustentacion}</strong></p>
                    <br>
                    <p>Jurado: <strong>{jurado.nombre_jurado}</strong>| Cargo: <strong>{detalle_evaluacion.cargo}</strong></p>                    
                    <p>Hemos recibido las siguientes sugerencias para tu evaluación:</p>
                    <pre>{detalle_evaluacion.sugerencias}</pre>
                    <br>
                    <p>Saludos,<br>UTIC</p>
                </body>
                </html>
            """
            from_email = 'UTIC| POSGRADO'
            recipient_list = [alumno.email]

            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=recipient_list,
                fail_silently=False,
                html_message=html_message,  # Añadir el mensaje HTML aquí
            )

 
            # Redirige a alguna página de éxito o muestra un mensaje de éxito
            #messages.success(request, "Evaluación completada")
            return redirect('listar_detalleevaluaciones')  # Reemplaza 'pagina_de_exito' con la URL adecuada
    else:
        # Si la solicitud no es POST, crea un nuevo formulario vacío
        form = DetalleEvaluacionForm()
        print('form no valido') 
    # Renderiza el formulario en la plantilla
    return render(request, "DetalleEvaluacion/evaluacion.html", {'form': form,'detalle_evaluacion': detalle_evaluacion, 'alumnodata': alumnodata})