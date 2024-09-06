from django.urls import path
from rest_api.views import lista_categoria,lista_detalle,vista_categoria,vista_detalle
from rest_api.viewsLogin import login_api
from Store.models import Usuario

urlpatterns = [
    path('lista_categoria/', lista_categoria, name="lista_categoria"),
    path('vista_categoria/<int:id>/', vista_categoria, name="vista_categoria"),
    path('lista_detalle/', lista_detalle, name="lista_detalle"),
    path('vista_detalle/<int:id>/', vista_detalle, name="vista_detalle"),
    path('login_api',login_api,name='login_api')
]