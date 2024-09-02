from django.contrib import admin
from .models import Usuario
from .models import Producto
from .models import Carrito
from .models import Categoria
admin.site.register(Usuario)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombreProducto', 'precioProducto', 'stockProd', 'imagen']

@admin.register(Carrito)
class ventas(admin.ModelAdmin):
    list_display = ['usuario', 'producto', 'cantidad']

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('idCategoria', 'nombreCat', 'imagenCat')
    search_fields = ('nombreCat',)
    list_filter = ('nombreCat',)