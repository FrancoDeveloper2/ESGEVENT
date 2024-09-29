from django.urls import path
from . import views
from .views import CustomPasswordResetCompleteView, CustomPasswordResetView, agregar_al_carrito, buscar_producto, contacto, enviar_contacto, iniciar_sesion, quienes_somos, ver_producto
from django.contrib.auth import views as auth_views
from .models import Usuario
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('', views.index, name="index"),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('buscar/', buscar_producto, name='buscar_producto'),
    path('bienvenida/', views.bienvenida, name="bienvenida"),
    path('cierresesion/', views.cierresesion, name="cierresesion"),
    path('registro/', views.registro, name="registro"), 
    path('registrar/', views.registrar_usuario, name='registrar_usuario'),
    path('editarperfil/', views.editar_perfil, name='editarperfil'),
    path('categorias/', views.vista_categorias, name='categorias'),
    path('categorias/', views.lista_categorias, name='categorias'),
    path('categoria/<int:id_categoria>/', views.detalle_categoria, name='categoria'),
    path('logout/', auth_views.LogoutView.as_view(next_page='cierresesion'), name='logout'),
    path('editar/', views.editar, name="editar"),
    path('producto/<int:idProducto>/', views.producto_detail, name='producto'),

    path('login/', views.iniciar_sesion, name='iniciar_sesion'),
    path('login/', views.iniciar_sesion, name='login'),
    path('enviar-contacto/', enviar_contacto, name='enviar_contacto'),

    path('cambio_contra/', views.cambio_contra, name='cambio_contra'),
    path('carrito/', views.carrito, name='carrito'),
    path('agregar_al_carrito/<int:idProducto>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('realizar_pedido/', views.realizar_pedido, name='realizar_pedido'),
    path('carrito/disminuir/<int:carrito_id>/', views.disminuir_unidad, name='disminuir_unidad'),
    path('carrito/vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
    path('carrito/finalizar/', views.finalizar_compra, name='finalizar_compra'),
    path('compra_finalizada/', views.compra_finalizada, name='compra_finalizada'),
    path('producto/<int:producto_id>/', ver_producto, name='ver_producto'), 
    path('quienes-somos/', quienes_somos, name='quienes_somos'),
    path('contacto/', contacto, name='contacto'),
    path('lista/', views.lista, name='lista'),
]

#esto es para guardar imagenes en BD
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)