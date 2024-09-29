from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from decimal import Decimal
from django.db.models import Count

class UsuarioManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('El campo Email es obligatorio')
        usuario = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, username, email, password=None, nombre=None, apellidos=None):
        usuario = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        usuario.is_superuser = True
        usuario.is_staff = True
        if nombre is not None:
            usuario.nombre = nombre
        if apellidos is not None:
            usuario.apellidos = apellidos
        usuario.save(using=self._db)
        return usuario

    def get_by_natural_key(self, username):
        return self.get(username=username)

class Usuario(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=16, unique=True, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    nombre = models.CharField(max_length=255, null=False, blank=False)
    apellidos = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)  
    is_staff = models.BooleanField(default=False)  

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'nombre', 'apellidos']

    objects = UsuarioManager()

class Categoria(models.Model):
    idCategoria = models.AutoField(primary_key=True, verbose_name="ID de la categoria")
    nombreCat = models.CharField(max_length=30, verbose_name="Nombre de la categoria", null=False, blank=False)
    imagenCat = models.ImageField(upload_to='categoria', null=True, blank=True)
    visible_en_carrusel = models.BooleanField(default=False, verbose_name="Visible en carrusel")  # Nuevo campo

    class Meta:
        db_table = 'STORE_CATEGORIA'

    def __str__(self):
        return str(self.nombreCat) if self.nombreCat else "Sin nombre"




class Logo(models.Model):
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)

    def __str__(self):
        return "Logos"
    

class Background(models.Model):
    background_image = models.ImageField(upload_to='backgrounds/', null=True, blank=True)

    def __str__(self):
        return "Fondo de la página"



class Producto(models.Model):
    idProducto = models.AutoField(primary_key=True, verbose_name="Id del Producto")
    nombreProducto = models.CharField(max_length=50, verbose_name="Nombre del Producto", null=False, blank=False)
    precioProducto = models.IntegerField(verbose_name="Precio del Producto", null=False, blank=False)
    descripcionProducto = models.CharField(max_length=900, verbose_name="Descripcion del Producto", null=False, blank=False)
    stockProd = models.IntegerField(verbose_name="Stock del Producto", null=False, blank=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='productos', null=True, blank=True)
    destacado = models.BooleanField(default=False, verbose_name="Destacado")  

    class Meta:
        db_table = 'STORE_PRODUCTO'

    def __str__(self):
        return self.nombreProducto  


class QuienesSomos(models.Model):
    contenido = models.TextField(verbose_name="Contenido", null=False, blank=False)

    class Meta:
        db_table = 'quienes_somos'

    def __str__(self):
        return "Contenido de Quiénes Somos"



class Venta(models.Model):
    idVenta = models.AutoField(primary_key=True, verbose_name="Id de venta", null=False, blank=False)
    fechaVenta = models.DateField(auto_now_add=True, verbose_name="Fecha de venta")
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    imagen_producto = models.ImageField(upload_to='productos', null=True, blank=True)  

    def __str__(self):
        return f"{self.usuario} - {self.producto.nombreProducto} - {self.fechaVenta}"

    @classmethod
    def obtener_productos_mas_vendidos(cls, limite=5):
        return cls.objects.values(
            'producto__idProducto',
            'producto__nombreProducto',
            'imagen_producto',  
            'precio_unitario'
        ).annotate(total_vendidos=Count('idVenta')).order_by('-total_vendidos')[:limite]





class Detalle (models.Model):
    idDetalle = models.AutoField(primary_key=True,verbose_name="Id del detalle",null=False, blank=False)
    cantidad = models.IntegerField(verbose_name="Cantidad",null=False, blank=False)
    subTotal = models.IntegerField(verbose_name="Subtotal",null=False, blank=False)
    venta = models.ForeignKey(Venta,on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto,on_delete=models.CASCADE)
    def __str__(self):
        return self.subTotal




class Carrito(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)  

    @classmethod
    def obtener_productos_mas_vendidos(cls, limite=5):
        return cls.objects.values('producto__idProducto', 'producto__nombreProducto', 'producto__imagen', 'producto__precioProducto').annotate(total_vendidos=Count('producto')).order_by('-total_vendidos')[:limite]
