import json
import requests

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import views as auth_views
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.utils import IntegrityError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404
from .models import Producto, Venta
from .models import Carrito, Venta, Producto
from .forms import ProductoSearchForm
from .models import Background, Logo, Usuario, Producto, Categoria, Carrito, Detalle


def vista_categorias(request):
    categorias = Categoria.objects.all()
    site_settings = Logo.objects.first()
    background = Background.objects.first()

    context = {
        'categorias': categorias,
        'site_settings': site_settings,
        'background': background,
    }

    return render(request, 'Store/html/categorias.html', context)




def detalle_categoria(request, id_categoria):
    categoria = get_object_or_404(Categoria, idCategoria=id_categoria)
    productos = Producto.objects.filter(categoria=categoria)
    site_settings = Logo.objects.first()
    background = Background.objects.first()

    context = {
        'categoria': categoria,
        'productos': productos,
        'site_settings': site_settings,
        'background': background,
    }

    return render(request, 'Store/html/detalle_categoria.html', context)


def lista_categorias(request):
    categorias = Categoria.objects.all()
    site_settings = Logo.objects.first()
    background = Background.objects.first()

    context = {
        'categorias': categorias,
        'site_settings': site_settings,
        'background': background,
    }

    return render(request, 'Store/html/categorias.html', context)


def categorias(request):
    site_settings = Logo.objects.first()
    background = Background.objects.first()

    context = {
        'site_settings': site_settings,
        'background': background,
    }

    return render(request, 'Store/html/categorias.html', context)

def cierresesion(request):
    logout(request)

    return render(request, 'Store/html/cierresesion.html')




def bienvenida(request):
    return render(request, 'Store/html/bienvenida.html')


def editar(request):
    site_settings = Logo.objects.first()
    return render(request, 'Store/html/editar_perfil.html', {'site_settings': site_settings})

def realizar_pedido(request):
    return render(request, 'Store/html/realizar_pedido.html')

def confirmar_venta(request):
    if request.method == 'POST':
        # Asegúrate de que el usuario esté autenticado
        if not request.user.is_authenticated:
            return redirect('login')  # Redirigir a la página de inicio de sesión

        # Obtener todos los artículos del carrito del usuario
        carrito = Carrito.objects.filter(usuario=request.user)

        # Verificar que el carrito no esté vacío
        if not carrito.exists():
            return redirect('carrito_vacio')  # Manejar carrito vacío

        for item in carrito:
            # Crear la venta por cada artículo en el carrito
            venta = Venta(
                usuario=request.user,
                producto=item.producto,
                cantidad=item.cantidad,
                precio_unitario=item.precio_total / item.cantidad,  # Calcula el precio unitario
                total=item.precio_total
            )
            venta.save()  # Guardar la venta en la base de datos

            # Limpiar el artículo del carrito después de la compra
            item.delete()

        # Redirigir a una página de éxito
        return redirect('pagina_de_exito')

    return render(request, 'carrito/confirmar.html')




def cambio_contra(request):
    site_settings = Logo.objects.first()
    background = Background.objects.first()

    context = {
        'site_settings': site_settings,
        'background': background,
    }

    return render(request, 'Store/html/cambio_contrasena.html', context)




def compra_finalizada(request):
    return render(request, 'Store/html/compra_finalizada.html')

def lista (request):
    return render(request, 'Store/html/lista_detalles.html')

def index(request):
    site_settings = Logo.objects.first()
    background = Background.objects.first()

    # Filtrar las categorías que deben aparecer en el carrusel
    categorias = Categoria.objects.filter(visible_en_carrusel=True)

    # Obtener productos más vendidos
    productos_mas_vendidos = Venta.obtener_productos_mas_vendidos()

    # Obtener productos más nuevos
    productos_mas_nuevos = Producto.objects.order_by('-idProducto')[:5]

    context = {
        'site_settings': site_settings,
        'background': background,
        'categorias': categorias,
        'productos_mas_vendidos': productos_mas_vendidos,  # Añadir productos más vendidos al contexto
        'productos_mas_nuevos': productos_mas_nuevos,  
    }

    return render(request, 'Store/index.html', context)



def producto_detail(request, idProducto):
    producto = get_object_or_404(Producto, idProducto=idProducto)
    context = {
        'producto': producto
    }
    return render(request, 'Store/producto_detail.html', context)

def registro(request):
    site_settings = Logo.objects.first()
    background = Background.objects.first()

    context = {
        'site_settings': site_settings,
        'background': background,
    }

    return render(request, 'Store/html/registro.html', context)


class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    template_name = 'registration/password_reset_form.html'
    success_url = reverse_lazy('password_reset_done')
    from_email = 'francopavez1@outlook.com'

    def get_users(self, email):
        UserModel = get_user_model()
        # Busca usuarios activos con ese correo
        active_users = UserModel.objects.filter(email=email, is_active=True)
        if not active_users.exists():
            print(f"No se encontraron usuarios activos con el correo: {email}")
        else:
            print(f"Usuarios encontrados: {active_users}")
        return (u for u in active_users)

class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'
    success_url = reverse_lazy('iniciar_sesion') 


#CARRITO
def carrito(request):
    site_settings = Logo.objects.first()
    background = Background.objects.first()
    
    carrito_items = Carrito.objects.filter()
    context = {
        'site_settings': site_settings,
        'background': background,
        'carrito_items': carrito_items,
    }
    return render(request, 'Store/html/carrito.html', context)

@login_required
def editar_perfil(request):
    site_settings = Logo.objects.first()
    background = Background.objects.first()
    usuario = request.user
    
    # Recuperar los detalles asociados con el usuario actualmente autenticado
    detalles = Detalle.objects.filter(venta__usuario=usuario)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellidos = request.POST.get('apellidos')
        email = request.POST.get('email')
        nuevo_username = request.POST.get('usuario')

        try:
            existing_user = Usuario.objects.exclude(pk=usuario.pk).filter(username=nuevo_username).exists()
            existing_email = Usuario.objects.exclude(pk=usuario.pk).filter(email=email).exists()

            if existing_user:
                error_message = "El nombre de usuario ya está en uso. Por favor, elige otro."
            elif existing_email:
                error_message = "El correo electrónico ya está en uso. Por favor, utiliza otro."
            else:
                # Actualizar los datos del usuario
                usuario.username = nuevo_username
                usuario.nombre = nombre
                usuario.apellidos = apellidos
                usuario.email = email
                usuario.save()
                messages.success(request, 'Perfil actualizado exitosamente.')
                return redirect('index')

        except IntegrityError as e:
            error_message = "Ha ocurrido un error durante la actualización. Por favor, inténtalo nuevamente."
        
        messages.error(request, error_message)
        return redirect('editar_perfil')  # Redirigir a la misma página en caso de error


    return render(request, 'Store/html/editar_perfil.html', {
        'detalles': detalles,
        'site_settings': site_settings,
        'background': background,
    })
#CAMBIAR CONTRASENA
@login_required
def cambiar_contrasena(request):
    if request.method == 'POST':
        usuario = request.user
        contrasena_antigua = request.POST['contrasena_antigua']
        nueva_contrasena = request.POST['nueva_contrasena']
        verificacion_contrasena = request.POST['verificacion_contrasena']

        try: 
            if usuario.check_password(contrasena_antigua):
                if nueva_contrasena == verificacion_contrasena:
                    usuario.set_password(nueva_contrasena)
                    usuario.save()
                    update_session_auth_hash(request, usuario)  
                    messages.success(request, 'Contraseña cambiada exitosamente.')
                    return redirect('cambiar_contrasena')
                else:
                    error_message = "Las contraseñas no coinciden."
            else:
                error_message = "La contraseña antigua no es válida."
        except IntegrityError as e:
            error_message = "Ha ocurrido un error al cambiar la contraseña. Por favor, inténtalo nuevamente."

        messages.error(request, error_message)

    return render(request, 'Store/html/cambio_contrasena.html')




#VISTA DE REGISTRAR USUARIO

def registrar_usuario(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        apellidos = request.POST['apellidos']
        email = request.POST['correo']
        username = request.POST['user']
        password = request.POST['pass']
        
        captcha_token = request.POST.get("g-recaptcha-response")
        cap_url = "https://www.google.com/recaptcha/api/siteverify"
        cap_secret = "6LfxrGooAAAAAAZX1lgSKeFjKZ1s4INgXReeBuXJ"  
        cap_data = {"secret": cap_secret, "response": captcha_token}
        cap_server_response = requests.post(url=cap_url, data=cap_data)
        cap_json = json.loads(cap_server_response.text)
        if cap_json['success']:
            try:
                existing_user = Usuario.objects.filter(username=username).exists()
                existing_email = Usuario.objects.filter(email=email).exists()
                
                if existing_user:
                    error_message = "El nombre de usuario ya está en uso. Por favor, elige otro."
                elif existing_email:
                    error_message = "El correo electrónico ya está en uso. Por favor, utiliza otro."
                else:
                    usuario_nuevo = Usuario(
                        username=username,
                        password=password,
                        email=email,
                        nombre=nombre,
                        apellidos=apellidos,
                    )
                    usuario_nuevo.set_password(password)
                    usuario_nuevo.save()
                    
                    # Establecer el backend en el objeto de usuario y luego iniciar sesión
                    usuario_nuevo.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, usuario_nuevo)
                    return redirect('bienvenida')
            except IntegrityError as e:
                error_message = "Ha ocurrido un error durante el registro. Por favor, inténtalo nuevamente."
        else:
            # La verificación del Captcha falló
            error_message = "Por favor, completa el Captcha correctamente."

        return render(request, 'Store/html/registro.html', {'error_message': error_message})
    
    return render(request, 'Store/html/registro.html')



# INICAR SESION
def iniciar_sesion(request):
    # Obtén los objetos 'Logo' y 'Background' antes de procesar la solicitud
    site_settings = Logo.objects.first()
    background = Background.objects.first()

    if request.method == 'POST':
        username = request.POST['user']
        password = request.POST['pass']
        captcha_token = request.POST.get("g-recaptcha-response")

        # Verificar el Captcha
        cap_url = "https://www.google.com/recaptcha/api/siteverify"
        cap_secret = "6LfxrGooAAAAAAZX1lgSKeFjKZ1s4INgXReeBuXJ"
        cap_data = {"secret": cap_secret, "response": captcha_token}
        cap_server_response = requests.post(url=cap_url, data=cap_data)
        cap_json = json.loads(cap_server_response.text)

        if cap_json['success']:
            usuario = authenticate(request, username=username, password=password)
            if usuario is not None:
                login(request, usuario)
                return redirect('index')
            else:
                error_message = "Nombre de usuario o contraseña incorrectos."
                return render(request, 'Store/html/login.html', {
                    'error_message': error_message,
                    'site_settings': site_settings,
                    'background': background
                })
        else:
            error_message = "Por favor, completa el Captcha correctamente."
            return render(request, 'Store/html/login.html', {
                'error_message': error_message,
                'site_settings': site_settings,
                'background': background
            })
    
    return render(request, 'Store/html/login.html', {
        'site_settings': site_settings,
        'background': background
    })



def buscar_producto(request):
    form = ProductoSearchForm()
    productos = None
    site_settings = Logo.objects.first()
    background = Background.objects.first()

    if 'query' in request.GET:
        query = request.GET.get('query')
        productos = Producto.objects.filter(
            nombreProducto__icontains=query
        ) | Producto.objects.filter(
            descripcionProducto__icontains=query
        ) | Producto.objects.filter(
            precioProducto__icontains=query
        )
     
    return render(request, 'Store/html/search_results.html', {
        'form': form,
        'site_settings': site_settings,
        'background': background,
        'productos': productos
    })


#AGREGAR UNIDADES AL CARRITO

def agregar_al_carrito(request, idProducto):
    producto = get_object_or_404(Producto, idProducto=idProducto)
    
    # Obtener la cantidad del formulario
    cantidad = int(request.POST.get('cantidad', 1))

    # Lógica para agregar al carrito
    carrito_item, created = Carrito.objects.get_or_create(
        usuario=request.user,
        producto=producto,
        defaults={'cantidad': 0}
    )
    carrito_item.cantidad += cantidad
    carrito_item.precio_total = carrito_item.cantidad * producto.precioProducto
    carrito_item.save()

    # Verificar si el artículo se agrega correctamente
    print(f'Producto agregado: {producto.nombreProducto}, Cantidad: {carrito_item.cantidad}')

    # Redirigir a la página anterior
    return redirect(request.META.get('HTTP_REFERER', 'index'))



#FUNCIONP QUITAR STOCK EN CARRITO
def disminuir_unidad(request, carrito_id):
    item = Carrito.objects.get(id=carrito_id, usuario=request.user)
    if item.cantidad > 1:  # Si hay más de una unidad, disminuye
        item.cantidad -= 1
        item.precio_total -= item.producto.precioProducto  #
        item.save()
    else:  
        item.delete()
    return redirect('carrito')

#FUNCION PARA VACIAR CARRITO
def vaciar_carrito(request):
    Carrito.objects.filter(usuario=request.user).delete()
    return redirect('carrito')



def finalizar_compra(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            # Procesa la dirección del envío
            direccion = request.POST.get('direccion')
            carrito_items = Carrito.objects.filter(usuario=request.user)

            if carrito_items.exists():
                for item in carrito_items:
                    # Crea una nueva venta por cada artículo en el carrito
                    venta = Venta(
                        usuario=request.user,
                        producto=item.producto,
                        cantidad=item.cantidad,
                        precio_unitario=item.producto.precioProducto,
                        total=item.precio_total,
                        imagen_producto=item.producto.imagen  # Guardar la imagen del producto
                    )
                    venta.save()

                # Vaciar el carrito después de la compra
                carrito_items.delete()

                return redirect('index') 
            else:
                return redirect('carrito_vacio')  

    return render(request, 'carrito/finalizar_compra.html')
