from django.urls import path
from appevaluacion.views import evaluacion,detalle_evaluacion


urlpatterns = [  
   #path('',evaluacion.evaluar ,name="evaluar"),
   path('',detalle_evaluacion.listar_detalleevaluaciones ,name="listar_detalleevaluaciones"),
   #path('listar_detalleevaluacion_json', detalle_evaluacion.listar_detalleevaluacion_json,name="listar_detalleevaluacion_json"), 
   path('evaluar/<int:pk>/',detalle_evaluacion.evaluar_sustentacion ,name="evaluar_sustentacion"),
   
]