"""
Django signals for real-time product updates.
Broadcasts changes to all connected WebSocket clients.
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Product
from .serializers import ProductSerializer


@receiver(post_save, sender=Product)
def product_updated(sender, instance, created, **kwargs):
    """
    Signal handler for product creation/update.
    Broadcasts the update to all connected WebSocket clients.
    """
    channel_layer = get_channel_layer()

    # Serialize the product data
    serializer = ProductSerializer(instance)
    product_data = serializer.data

    # Prepare the message
    message_type = 'product_created' if created else 'product_updated'

    # Broadcast to all clients in the product_updates group
    if channel_layer:
        async_to_sync(channel_layer.group_send)(
            'product_updates',
            {
                'type': 'product_update',
                'data': {
                    'type': message_type,
                    'product': product_data,
                    'is_new_arrival': instance.new_arrival,
                    'is_featured': instance.featured,
                    'is_on_sale': instance.on_sale,
                }
            }
        )

    print(f'📢 WebSocket broadcast: {message_type} - {instance.name}')


@receiver(post_delete, sender=Product)
def product_deleted(sender, instance, **kwargs):
    """
    Signal handler for product deletion.
    Notifies all connected clients about the deletion.
    """
    channel_layer = get_channel_layer()

    if channel_layer:
        async_to_sync(channel_layer.group_send)(
            'product_updates',
            {
                'type': 'product_update',
                'data': {
                    'type': 'product_deleted',
                    'product_id': instance.id,
                    'product_name': instance.name,
                }
            }
        )

    print(f'📢 WebSocket broadcast: product_deleted - {instance.name}')


def broadcast_price_change(product, old_price, new_price):
    """
    Utility function to broadcast price changes.
    Can be called manually when you want to notify about price drops.
    """
    channel_layer = get_channel_layer()

    if channel_layer and old_price != new_price:
        price_dropped = new_price < old_price

        async_to_sync(channel_layer.group_send)(
            'product_updates',
            {
                'type': 'product_update',
                'data': {
                    'type': 'price_change',
                    'product_id': product.id,
                    'product_name': product.name,
                    'old_price': float(old_price),
                    'new_price': float(new_price),
                    'price_dropped': price_dropped,
                    'discount_percent': ((old_price - new_price) / old_price * 100) if price_dropped else 0
                }
            }
        )

        print(f'📢 WebSocket broadcast: price_change - {product.name} (${old_price} → ${new_price})')


def broadcast_stock_update(product, old_stock, new_stock):
    """
    Utility function to broadcast stock changes.
    Notifies clients when products are restocked or running low.
    """
    channel_layer = get_channel_layer()

    if channel_layer and old_stock != new_stock:
        restocked = new_stock > old_stock
        low_stock = new_stock > 0 and new_stock < 10
        out_of_stock = new_stock == 0

        async_to_sync(channel_layer.group_send)(
            'product_updates',
            {
                'type': 'product_update',
                'data': {
                    'type': 'stock_update',
                    'product_id': product.id,
                    'product_name': product.name,
                    'old_stock': old_stock,
                    'new_stock': new_stock,
                    'restocked': restocked,
                    'low_stock': low_stock,
                    'out_of_stock': out_of_stock,
                }
            }
        )

        status = 'restocked' if restocked else 'low stock' if low_stock else 'out of stock' if out_of_stock else 'updated'
        print(f'📢 WebSocket broadcast: stock_update - {product.name} ({old_stock} → {new_stock}) [{status}]')
