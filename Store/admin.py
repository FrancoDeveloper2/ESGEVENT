from django.contrib import admin
from .models import Background, Logo, QuienesSomos, Usuario
from .models import Producto
from .models import Carrito
from .models import Categoria

admin.site.register(Usuario)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombreProducto', 'precioProducto', 'stockProd', 'imagen', 'destacado']
    list_filter = ['destacado']  
    search_fields = ['nombreProducto']  


@admin.register(Carrito)
class ventas(admin.ModelAdmin):
    list_display = ['usuario', 'producto', 'cantidad']

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('idCategoria', 'nombreCat', 'imagenCat', 'visible_en_carrusel')  
    search_fields = ('nombreCat',)
    list_filter = ('nombreCat', 'visible_en_carrusel')  

@admin.register(QuienesSomos)
class QuienesSomosAdmin(admin.ModelAdmin):
    list_display = ['id', 'contenido']


admin.site.register(Logo)

@admin.register(Background)
class BackgroundAdmin(admin.ModelAdmin):
    pass

