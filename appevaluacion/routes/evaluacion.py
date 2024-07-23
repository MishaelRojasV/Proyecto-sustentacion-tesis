
from django.urls import path
from appevaluacion.views import evaluacion


urlpatterns = [  
   path('',evaluacion.listar_evaluaciones ,name="listar_evaluaciones"),
   path('listar_evaluacion_json', evaluacion.listar_evaluacion_json,name="listar_evaluacion_json"), 
   path('create/',evaluacion.crear_evaluacion ,name="crear_evaluacion"),
   path('edit/<int:id>/',evaluacion.actualizar_evaluacion ,name="actualizar_evaluacion"),
   path('delete/<int:id>/',evaluacion.eliminar_evaluacion ,name="eliminar_evaluacion"),
  
]