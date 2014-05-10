kanbaneryStatistics
===================

# Estadísticas de Kanbanery

Script para conseguir estadísticas de kanbanery

Actualmente retorna estadísticas por tipo de tarea y por usurio

  # Resultado de ejmplos
  Email, Name, Time, Estimate Time
  mimail@gmail.com, mkulppi, 68:15, 51:30
  ...
  Task type, Time
  administration, 68:43

## Instalación

Setea tu ApiKey al inicio del archivo

  # correlo mediante
  request_time_date.py
  
## Uso

En kambanery los títulos de tus tareas deben indicar el tiempo real dedicado a ellas, esto se hace mediante el siguiente formato:

* $HH:MM : Tiempo dedicado individualemte a dicha tarea 
* @$HH:MM : Tiempo dedicado por todos los integrantes del grupo

  # por ejemplo:
  "[API] Crear request para actualizar información del usuario en el servidor $02:45"
  
## Futuras implementaciones

+ **Reconocer filtros de categoria** : [Categoría][Subcategoría] , no la unica forma pero la recomendamos altamente por su contexto
+ **Graficos inmediatos** : El script está diseñador en python, por lo que Bokeh es una librería que hemos pensado, la cual requiere anaconda  

Todo usuario sientase libre de usar esto y agradecemos cualquier aporte para hacer este código más funcional


