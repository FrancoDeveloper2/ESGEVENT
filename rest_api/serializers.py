from rest_framework import serializers
from Store.models import Categoria,Detalle

class CategoriaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['idCategoria','nombreCat']

class DetalleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Detalle
        fields = ['idDetalle','cantidad','subTotal','venta','producto']

