from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio_construccion, name='inicio_construccion'),
    
    # URLs para Empleados
    path('empleado/agregar/', views.agregar_empleado, name='agregar_empleado'),
    path('empleado/ver/', views.ver_empleados, name='ver_empleados'),
    path('empleado/actualizar/<int:empleado_id>/', views.actualizar_empleado, name='actualizar_empleado'),
    path('empleado/realizar_actualizacion/<int:empleado_id>/', views.realizar_actualizacion_empleado, name='realizar_actualizacion_empleado'),
    path('empleado/borrar/<int:empleado_id>/', views.borrar_empleado, name='borrar_empleado'),
    
    # URLs para Clientes
    path('cliente/agregar/', views.agregar_cliente, name='agregar_cliente'),
    path('cliente/ver/', views.ver_clientes, name='ver_clientes'),
    path('cliente/actualizar/<int:cliente_id>/', views.actualizar_cliente, name='actualizar_cliente'),
    path('cliente/realizar_actualizacion/<int:cliente_id>/', views.realizar_actualizacion_cliente, name='realizar_actualizacion_cliente'),
    path('cliente/borrar/<int:cliente_id>/', views.borrar_cliente, name='borrar_cliente'),
    
    # URLs para Proyectos
    path('proyecto/agregar/', views.agregar_proyecto, name='agregar_proyecto'),
    path('proyecto/ver/', views.ver_proyectos, name='ver_proyectos'),
    path('proyecto/actualizar/<int:proyecto_id>/', views.actualizar_proyecto, name='actualizar_proyecto'),
    path('proyecto/realizar_actualizacion/<int:proyecto_id>/', views.realizar_actualizacion_proyecto, name='realizar_actualizacion_proyecto'),
    path('proyecto/borrar/<int:proyecto_id>/', views.borrar_proyecto, name='borrar_proyecto'),
]