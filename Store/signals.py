from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Producto

@receiver(post_save, sender=Producto)
def notificar_stock_agotado(sender, instance, **kwargs):
    if instance.stockProd == 0:
        # Enviar correo al administrador
        send_mail(
            'Stock agotado: {}'.format(instance.nombreProducto),
            'El producto "{}" ha agotado su stock.'.format(instance.nombreProducto),
            settings.DEFAULT_FROM_EMAIL,  # Email desde el que se enviará
            [settings.ADMIN_EMAIL],  # Dirección de email del administrador
            fail_silently=False,
        )
