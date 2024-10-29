
from django.urls import path
from appevaluacion.views import jornada

urlpatterns = [   
    path('',jornada.listar_jornadas ,name="listar_jornadas"),
    path('listar_jornadas_json', jornada.listar_jornadas_json,name="listar_jornadas_json"), 
    path('crear-jornada/',jornada.crear_jornada ,name="crear_jornada"),
    path('update-status-jornada/',jornada.update_jornada_status,name="update_jornada_status"),

    #path('edit/<int:id>/',jurado.actualizar_jurado ,name="actualizar_jurado"),
    #path('delete/<int:id>/',jurado.eliminar_jurado ,name="eliminar_jurado"),
    #path('enviar_credenciales/<int:pk>/', jurado.enviar_credenciales, name='enviar_credenciales'),
]