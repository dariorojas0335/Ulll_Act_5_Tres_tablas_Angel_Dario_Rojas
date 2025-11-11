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