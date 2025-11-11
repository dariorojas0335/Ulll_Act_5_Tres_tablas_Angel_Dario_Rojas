# Tercera Parte: Implementación del CRUD para Proyectos

## Estructura Actualizada Completa

```
UIII_Construccion_0335/
├── backend_Construccion/
│   ├── backend_Construccion/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── app_Construccion/
│   │   ├── migrations/
│   │   │   └── __init__.py
│   │   ├── templates/
│   │   │   ├── empleado/
│   │   │   │   ├── agregar_empleado.html
│   │   │   │   ├── ver_empleado.html
│   │   │   │   ├── actualizar_empleado.html
│   │   │   │   └── borrar_empleado.html
│   │   │   ├── cliente/
│   │   │   │   ├── agregar_cliente.html
│   │   │   │   ├── ver_cliente.html
│   │   │   │   ├── actualizar_cliente.html
│   │   │   │   └── borrar_cliente.html
│   │   │   ├── proyecto/
│   │   │   │   ├── agregar_proyecto.html
│   │   │   │   ├── ver_proyecto.html
│   │   │   │   ├── actualizar_proyecto.html
│   │   │   │   └── borrar_proyecto.html
│   │   │   ├── base.html
│   │   │   ├── header.html
│   │   │   ├── navbar.html
│   │   │   ├── footer.html
│   │   │   └── inicio.html
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── manage.py
│   └── db.sqlite3
└── .venv/
```

## Archivos Actualizados

### 1. views.py (completo con todas las funciones)
```python
from django.shortcuts import render, redirect, get_object_or_404
from .models import Empleado, Cliente, Proyecto

def inicio_construccion(request):
    return render(request, 'inicio.html')

# Funciones para Empleados
def agregar_empleado(request):
    if request.method == 'POST':
        empleado = Empleado(
            nombre=request.POST['nombre'],
            apellido=request.POST['apellido'],
            cargo=request.POST['cargo'],
            telefono=request.POST['telefono'],
            email=request.POST['email'],
            fecha_contratacion=request.POST['fecha_contratacion'],
            salario=request.POST['salario']
        )
        empleado.save()
        return redirect('ver_empleados')
    return render(request, 'empleado/agregar_empleado.html')

def ver_empleados(request):
    empleados = Empleado.objects.all()
    return render(request, 'empleado/ver_empleado.html', {'empleados': empleados})

def actualizar_empleado(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)
    if request.method == 'POST':
        empleado.nombre = request.POST['nombre']
        empleado.apellido = request.POST['apellido']
        empleado.cargo = request.POST['cargo']
        empleado.telefono = request.POST['telefono']
        empleado.email = request.POST['email']
        empleado.fecha_contratacion = request.POST['fecha_contratacion']
        empleado.salario = request.POST['salario']
        empleado.save()
        return redirect('ver_empleados')
    return render(request, 'empleado/actualizar_empleado.html', {'empleado': empleado})

def realizar_actualizacion_empleado(request, empleado_id):
    return actualizar_empleado(request, empleado_id)

def borrar_empleado(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)
    if request.method == 'POST':
        empleado.delete()
        return redirect('ver_empleados')
    return render(request, 'empleado/borrar_empleado.html', {'empleado': empleado})

# Funciones para Clientes
def agregar_cliente(request):
    if request.method == 'POST':
        cliente = Cliente(
            nombre=request.POST['nombre'],
            apellido=request.POST['apellido'],
            tipo_cliente=request.POST['tipo_cliente'],
            telefono=request.POST['telefono'],
            email=request.POST['email'],
            direccion=request.POST['direccion']
        )
        cliente.save()
        return redirect('ver_clientes')
    return render(request, 'cliente/agregar_cliente.html')

def ver_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'cliente/ver_cliente.html', {'clientes': clientes})

def actualizar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        cliente.nombre = request.POST['nombre']
        cliente.apellido = request.POST['apellido']
        cliente.tipo_cliente = request.POST['tipo_cliente']
        cliente.telefono = request.POST['telefono']
        cliente.email = request.POST['email']
        cliente.direccion = request.POST['direccion']
        cliente.save()
        return redirect('ver_clientes')
    return render(request, 'cliente/actualizar_cliente.html', {'cliente': cliente})

def realizar_actualizacion_cliente(request, cliente_id):
    return actualizar_cliente(request, cliente_id)

def borrar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('ver_clientes')
    return render(request, 'cliente/borrar_cliente.html', {'cliente': cliente})

# Funciones para Proyectos
def agregar_proyecto(request):
    if request.method == 'POST':
        proyecto = Proyecto(
            nombre=request.POST['nombre'],
            descripcion=request.POST['descripcion'],
            fecha_inicio=request.POST['fecha_inicio'],
            fecha_fin=request.POST['fecha_fin'],
            presupuesto=request.POST['presupuesto'],
            cliente_id=request.POST['cliente'],
            estado=request.POST['estado']
        )
        proyecto.save()
        
        # Asignar empleados al proyecto (ManyToMany)
        empleados_ids = request.POST.getlist('empleados')
        proyecto.empleados.set(empleados_ids)
        
        return redirect('ver_proyectos')
    
    clientes = Cliente.objects.all()
    empleados = Empleado.objects.all()
    return render(request, 'proyecto/agregar_proyecto.html', {
        'clientes': clientes,
        'empleados': empleados
    })

def ver_proyectos(request):
    proyectos = Proyecto.objects.all().select_related('cliente').prefetch_related('empleados')
    return render(request, 'proyecto/ver_proyecto.html', {'proyectos': proyectos})

def actualizar_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    
    if request.method == 'POST':
        proyecto.nombre = request.POST['nombre']
        proyecto.descripcion = request.POST['descripcion']
        proyecto.fecha_inicio = request.POST['fecha_inicio']
        proyecto.fecha_fin = request.POST['fecha_fin']
        proyecto.presupuesto = request.POST['presupuesto']
        proyecto.cliente_id = request.POST['cliente']
        proyecto.estado = request.POST['estado']
        proyecto.save()
        
        # Actualizar empleados del proyecto
        empleados_ids = request.POST.getlist('empleados')
        proyecto.empleados.set(empleados_ids)
        
        return redirect('ver_proyectos')
    
    clientes = Cliente.objects.all()
    empleados = Empleado.objects.all()
    return render(request, 'proyecto/actualizar_proyecto.html', {
        'proyecto': proyecto,
        'clientes': clientes,
        'empleados': empleados
    })

def realizar_actualizacion_proyecto(request, proyecto_id):
    return actualizar_proyecto(request, proyecto_id)

def borrar_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    if request.method == 'POST':
        proyecto.delete()
        return redirect('ver_proyectos')
    return render(request, 'proyecto/borrar_proyecto.html', {'proyecto': proyecto})
```

### 2. urls.py (app_Construccion - completo)
```python
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
```

### 3. navbar.html (actualizado completo)
```html
<nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <div class="container">
        <a class="navbar-brand" href="{% url 'inicio_construccion' %}">
            🏗️ Sistema de Administración Construcción
        </a>
        
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span class="navbar-toggler-icon"></span>
        </button>
        
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav me-auto">
                <li class="nav-item">
                    <a class="nav-link" href="{% url 'inicio_construccion' %}">
                        🏠 Inicio
                    </a>
                </li>
                
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                        👥 Empleados
                    </a>
                    <ul class="dropdown-menu">
                        <li><a class="dropdown-item" href="{% url 'agregar_empleado' %}">Agregar Empleado</a></li>
                        <li><a class="dropdown-item" href="{% url 'ver_empleados' %}">Ver Empleados</a></li>
                    </ul>
                </li>
                
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                        👨‍💼 Clientes
                    </a>
                    <ul class="dropdown-menu">
                        <li><a class="dropdown-item" href="{% url 'agregar_cliente' %}">Agregar Cliente</a></li>
                        <li><a class="dropdown-item" href="{% url 'ver_clientes' %}">Ver Clientes</a></li>
                    </ul>
                </li>
                
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                        📋 Proyectos
                    </a>
                    <ul class="dropdown-menu">
                        <li><a class="dropdown-item" href="{% url 'agregar_proyecto' %}">Agregar Proyecto</a></li>
                        <li><a class="dropdown-item" href="{% url 'ver_proyectos' %}">Ver Proyectos</a></li>
                    </ul>
                </li>
            </ul>
        </div>
    </div>
</nav>
```

## Nuevos Templates para Proyecto

### 4. agregar_proyecto.html
```html
{% extends 'base.html' %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-10">
        <div class="card">
            <div class="card-header bg-info text-white">
                <h4 class="mb-0">Agregar Nuevo Proyecto</h4>
            </div>
            <div class="card-body">
                <form method="POST">
                    {% csrf_token %}
                    
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label for="nombre" class="form-label">Nombre del Proyecto</label>
                            <input type="text" class="form-control" id="nombre" name="nombre" required>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label for="presupuesto" class="form-label">Presupuesto</label>
                            <input type="number" step="0.01" class="form-control" id="presupuesto" name="presupuesto" required>
                        </div>
                    </div>
                    
                    <div class="mb-3">
                        <label for="descripcion" class="form-label">Descripción</label>
                        <textarea class="form-control" id="descripcion" name="descripcion" rows="3" required></textarea>
                    </div>
                    
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label for="fecha_inicio" class="form-label">Fecha de Inicio</label>
                            <input type="date" class="form-control" id="fecha_inicio" name="fecha_inicio" required>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label for="fecha_fin" class="form-label">Fecha de Finalización</label>
                            <input type="date" class="form-control" id="fecha_fin" name="fecha_fin" required>
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label for="cliente" class="form-label">Cliente</label>
                            <select class="form-select" id="cliente" name="cliente" required>
                                <option value="">Seleccionar Cliente</option>
                                {% for cliente in clientes %}
                                <option value="{{ cliente.id }}">{{ cliente.nombre }} {{ cliente.apellido }}</option>
                                {% endfor %}
                            </select>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label for="estado" class="form-label">Estado</label>
                            <select class="form-select" id="estado" name="estado" required>
                                <option value="En planificación">En planificación</option>
                                <option value="En curso">En curso</option>
                                <option value="Finalizado">Finalizado</option>
                            </select>
                        </div>
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">Empleados Asignados</label>
                        <div class="border rounded p-3" style="max-height: 200px; overflow-y: auto;">
                            {% for empleado in empleados %}
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" name="empleados" value="{{ empleado.id }}" id="empleado{{ empleado.id }}">
                                <label class="form-check-label" for="empleado{{ empleado.id }}">
                                    {{ empleado.nombre }} {{ empleado.apellido }} - {{ empleado.cargo }}
                                </label>
                            </div>
                            {% endfor %}
                        </div>
                    </div>
                    
                    <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                        <a href="{% url 'ver_proyectos' %}" class="btn btn-secondary me-md-2">Cancelar</a>
                        <button type="submit" class="btn btn-info text-white">Guardar Proyecto</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 5. ver_proyecto.html
```html
{% extends 'base.html' %}

{% block content %}
<div class="card">
    <div class="card-header bg-info text-white d-flex justify-content-between align-items-center">
        <h4 class="mb-0">Lista de Proyectos</h4>
        <a href="{% url 'agregar_proyecto' %}" class="btn btn-light">➕ Agregar Proyecto</a>
    </div>
    <div class="card-body">
        {% if proyectos %}
        <div class="table-responsive">
            <table class="table table-striped table-hover">
                <thead class="table-dark">
                    <tr>
                        <th>Nombre</th>
                        <th>Descripción</th>
                        <th>Cliente</th>
                        <th>Fecha Inicio</th>
                        <th>Fecha Fin</th>
                        <th>Presupuesto</th>
                        <th>Estado</th>
                        <th>Empleados</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    {% for proyecto in proyectos %}
                    <tr>
                        <td><strong>{{ proyecto.nombre }}</strong></td>
                        <td>{{ proyecto.descripcion|truncatewords:10 }}</td>
                        <td>{{ proyecto.cliente.nombre }} {{ proyecto.cliente.apellido }}</td>
                        <td>{{ proyecto.fecha_inicio }}</td>
                        <td>{{ proyecto.fecha_fin }}</td>
                        <td>${{ proyecto.presupuesto }}</td>
                        <td>
                            <span class="badge 
                                {% if proyecto.estado == 'En planificación' %}bg-secondary
                                {% elif proyecto.estado == 'En curso' %}bg-warning
                                {% else %}bg-success{% endif %}">
                                {{ proyecto.estado }}
                            </span>
                        </td>
                        <td>
                            <small>
                                {% for empleado in proyecto.empleados.all %}
                                {{ empleado.nombre }}{% if not forloop.last %}, {% endif %}
                                {% endfor %}
                            </small>
                        </td>
                        <td>
                            <div class="btn-group" role="group">
                                <a href="{% url 'actualizar_proyecto' proyecto.id %}" class="btn btn-warning btn-sm">✏️ Editar</a>
                                <a href="{% url 'borrar_proyecto' proyecto.id %}" class="btn btn-danger btn-sm">🗑️ Borrar</a>
                            </div>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        {% else %}
        <div class="alert alert-info text-center">
            <h5>No hay proyectos registrados</h5>
            <p>Comienza agregando el primer proyecto al sistema.</p>
            <a href="{% url 'agregar_proyecto' %}" class="btn btn-info text-white">Agregar Primer Proyecto</a>
        </div>
        {% endif %}
    </div>
</div>
{% endblock %}
```

### 6. actualizar_proyecto.html
```html
{% extends 'base.html' %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-10">
        <div class="card">
            <div class="card-header bg-warning text-dark">
                <h4 class="mb-0">Actualizar Proyecto</h4>
            </div>
            <div class="card-body">
                <form method="POST">
                    {% csrf_token %}
                    
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label for="nombre" class="form-label">Nombre del Proyecto</label>
                            <input type="text" class="form-control" id="nombre" name="nombre" value="{{ proyecto.nombre }}" required>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label for="presupuesto" class="form-label">Presupuesto</label>
                            <input type="number" step="0.01" class="form-control" id="presupuesto" name="presupuesto" value="{{ proyecto.presupuesto }}" required>
                        </div>
                    </div>
                    
                    <div class="mb-3">
                        <label for="descripcion" class="form-label">Descripción</label>
                        <textarea class="form-control" id="descripcion" name="descripcion" rows="3" required>{{ proyecto.descripcion }}</textarea>
                    </div>
                    
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label for="fecha_inicio" class="form-label">Fecha de Inicio</label>
                            <input type="date" class="form-control" id="fecha_inicio" name="fecha_inicio" value="{{ proyecto.fecha_inicio|date:'Y-m-d' }}" required>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label for="fecha_fin" class="form-label">Fecha de Finalización</label>
                            <input type="date" class="form-control" id="fecha_fin" name="fecha_fin" value="{{ proyecto.fecha_fin|date:'Y-m-d' }}" required>
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label for="cliente" class="form-label">Cliente</label>
                            <select class="form-select" id="cliente" name="cliente" required>
                                <option value="">Seleccionar Cliente</option>
                                {% for cliente in clientes %}
                                <option value="{{ cliente.id }}" {% if cliente.id == proyecto.cliente.id %}selected{% endif %}>
                                    {{ cliente.nombre }} {{ cliente.apellido }}
                                </option>
                                {% endfor %}
                            </select>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label for="estado" class="form-label">Estado</label>
                            <select class="form-select" id="estado" name="estado" required>
                                <option value="En planificación" {% if proyecto.estado == "En planificación" %}selected{% endif %}>En planificación</option>
                                <option value="En curso" {% if proyecto.estado == "En curso" %}selected{% endif %}>En curso</option>
                                <option value="Finalizado" {% if proyecto.estado == "Finalizado" %}selected{% endif %}>Finalizado</option>
                            </select>
                        </div>
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">Empleados Asignados</label>
                        <div class="border rounded p-3" style="max-height: 200px; overflow-y: auto;">
                            {% for empleado in empleados %}
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" name="empleados" value="{{ empleado.id }}" id="empleado{{ empleado.id }}"
                                    {% if empleado in proyecto.empleados.all %}checked{% endif %}>
                                <label class="form-check-label" for="empleado{{ empleado.id }}">
                                    {{ empleado.nombre }} {{ empleado.apellido }} - {{ empleado.cargo }}
                                </label>
                            </div>
                            {% endfor %}
                        </div>
                    </div>
                    
                    <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                        <a href="{% url 'ver_proyectos' %}" class="btn btn-secondary me-md-2">Cancelar</a>
                        <button type="submit" class="btn btn-warning">Actualizar Proyecto</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 7. borrar_proyecto.html
```html
{% extends 'base.html' %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header bg-danger text-white">
                <h4 class="mb-0">Confirmar Eliminación</h4>
            </div>
            <div class="card-body text-center">
                <h5>¿Está seguro que desea eliminar el proyecto?</h5>
                <p class="lead">{{ proyecto.nombre }}</p>
                <p><strong>Cliente:</strong> {{ proyecto.cliente.nombre }} {{ proyecto.cliente.apellido }}</p>
                <p><strong>Presupuesto:</strong> ${{ proyecto.presupuesto }}</p>
                <p><strong>Estado:</strong> {{ proyecto.estado }}</p>
                <p><strong>Empleados asignados:</strong> {{ proyecto.empleados.count }}</p>
                
                <form method="POST">
                    {% csrf_token %}
                    <div class="d-grid gap-2 d-md-flex justify-content-md-center">
                        <a href="{% url 'ver_proyectos' %}" class="btn btn-secondary me-md-2">Cancelar</a>
                        <button type="submit" class="btn btn-danger">Confirmar Eliminación</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

## Comandos para Ejecutar

```bash
# Activar entorno virtual
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Mac/Linux

# Realizar migraciones (si hay cambios en modelos)
python manage.py makemigrations
python manage.py migrate

# Ejecutar servidor
python manage.py runserver 8032
```

## Características Implementadas para Proyectos

✅ **CRUD completo para Proyectos**:
- Agregar nuevos proyectos con relaciones ManyToMany
- Ver lista de proyectos con información relacionada
- Actualizar proyectos y sus relaciones
- Borrar proyectos

✅ **Relaciones implementadas**:
- ForeignKey con Cliente
- ManyToMany con Empleado
- Campos de estado con choices

✅ **Diseño moderno y atractivo**:
- Colores azules/info para proyectos
- Badges para estados
- Tablas responsivas con información completa
- Formularios con selects y checkboxes para relaciones

✅ **Funcionalidades avanzadas**:
- Selección múltiple de empleados
- Visualización de relaciones en tablas
- Filtros y búsquedas optimizadas con `select_related` y `prefetch_related`

El sistema ahora está completo con todas las tres entidades principales: **Empleados**, **Clientes** y **Proyectos**, totalmente funcional y listo para usar en el puerto 8032.
