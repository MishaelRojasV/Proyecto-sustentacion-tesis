
from django.urls import path
from appevaluacion.views import jurado

urlpatterns = [   
    path('',jurado.listar_jurados ,name="listar_jurados"),
    path('listar_jurado_json', jurado.listar_jurado_json,name="listar_jurado_json"), 
    path('create/',jurado.crear_jurado ,name="crear_jurado"),
    path('edit/<int:id>/',jurado.actualizar_jurado ,name="actualizar_jurado"),
    path('delete/<int:id>/',jurado.eliminar_jurado ,name="eliminar_jurado"),
    path('enviar_credenciales/<int:pk>/', jurado.enviar_credenciales, name='enviar_credenciales'),
]