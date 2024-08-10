from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from appevaluacion.views import evaluacion, views, usuario

urlpatterns = [
    path('admin/', admin.site.urls),

    #Accesos
    path('', views.acceder, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.salir ,name="logout"),

    #Usuarios
    path('usuarios/',include('appevaluacion.routes.usuario'),name="usuarios"),
    path('create_user/', usuario.create_user, name='create_user'),


    #Ponente
    path('ponente/',include('appevaluacion.routes.ponente')),

    #Jurados
    path('jurado/',include('appevaluacion.routes.jurado')),

    #Evaluaciones
    path('evaluacion/',include('appevaluacion.routes.evaluacion')),

    path('detalle/',include('appevaluacion.routes.detalle_evaluacion')),


    path('create-detalle/',evaluacion.crear_detalle_evaluacion ,name="crear_detalle_evaluacion"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)