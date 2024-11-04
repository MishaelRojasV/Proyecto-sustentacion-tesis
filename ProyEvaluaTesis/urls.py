from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from appevaluacion.views import evaluacion, views, usuario,dashboard

urlpatterns = [
    path('admin/', admin.site.urls),

    #Accesos
    path('', views.acceder, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.salir ,name="logout"),

    #Usuarios
    path('usuarios/',include('appevaluacion.routes.usuario'),name="usuarios"),
    path('create_user/', usuario.create_user, name='create_user'),

    #Jornada
    path('jornada/',include('appevaluacion.routes.jornada')),

    #Ponente
    path('ponente/',include('appevaluacion.routes.ponente')),

    #Jurados
    path('jurado/',include('appevaluacion.routes.jurado')),

    #Evaluaciones
    path('evaluacion/',include('appevaluacion.routes.evaluacion')),

    path('detalle/',include('appevaluacion.routes.detalle_evaluacion')),

    #Reportes
    path('dashboard/', dashboard.dashboard, name='dashboard'),
    path('datos-polar-area/', dashboard.obtener_datos_polar_area, name='obtener_datos_polar_area'),
    path('obtener_datos_grafico/', dashboard.obtener_datos_grafico, name='obtener_datos_grafico'),



    path('create-detalle/',evaluacion.crear_detalle_evaluacion ,name="crear_detalle_evaluacion"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)