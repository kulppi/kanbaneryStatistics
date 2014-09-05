# Estadísticas de Kanbanery

## Descripción

Script para conseguir estadísticas de kanbanery

Actualmente retorna estadísticas por tipo de tarea y por usuario


    # Resultado de ejemplo
    Email, Name, Time, Estimate Time
    mimail@gmail.com, mkulppi, 68:15, 51:30
    ...
    Task type, Time
    administration, 68:43

Junto con esto genera dos gráficos usando Google Charts
uno que considera las tareas adjuntas y otro que no. Por ejemplo

![Image of Chart Example](https://dl.dropboxusercontent.com/u/43408721/example.png)

## Instalación

Setea tu ApiKey al inicio del archivo

    # correr mediante
   python request_time_data_no_api_token.py
  
## Uso

En kambanery los títulos de tus tareas deben indicar el tiempo real dedicado a ellas, esto se hace mediante el siguiente formato:

* $HH:MM : Tiempo dedicado individualemte a dicha tarea 
* @$HH:MM : Tiempo dedicado por todos los integrantes del grupo

por ejemplo:

    "[API] Crear request para actualizar información del usuario en el servidor $02:45"
        
## Futuras implementaciones

+ **Reconocer filtros de categoria** : [Categoría][Subcategoría] , no la unica forma pero la recomendamos altamente por su contexto
+ **Reconocer filtros por fecha** 

Todo usuario sientase libre de usar esto y agradecemos cualquier aporte para hacer este código más funcional


