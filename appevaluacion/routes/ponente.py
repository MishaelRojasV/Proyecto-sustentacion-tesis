
from django.urls import path
from appevaluacion.views import ponente

urlpatterns = [   
    path('',ponente.listar_ponentes ,name="listar_ponentes"),
    path('listar_ponentes_json', ponente.listar_ponentes_json,name="listar_ponentes_json"), 
    path('create/',ponente.crear_ponente ,name="crear_ponente"),
    path('edit/<int:id>/',ponente.actualizar_ponente ,name="actualizar_ponente"),
    path('delete/<int:id>/',ponente.eliminar_ponente ,name="eliminar_ponente"),
]