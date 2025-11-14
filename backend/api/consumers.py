"""
WebSocket consumers for real-time updates.
"""
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Product
from .serializers import ProductSerializer


class ProductConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for real-time product updates.

    Handles:
    - New product arrivals
    - Product stock updates
    - Product price changes
    """

    async def connect(self):
        """Accept WebSocket connection and join product updates group."""
        self.group_name = 'product_updates'

        # Join product updates group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

        # Send initial new arrivals data
        await self.send_new_arrivals()

    async def disconnect(self, close_code):
        """Leave product updates group."""
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Receive message from WebSocket.
        Expected message types:
        - get_new_arrivals: Fetch latest new arrivals
        - get_featured: Fetch featured products
        """
        try:
            data = json.loads(text_data)
            message_type = data.get('type')

            if message_type == 'get_new_arrivals':
                await self.send_new_arrivals()
            elif message_type == 'get_featured':
                await self.send_featured_products()

        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON'
            }))

    async def product_update(self, event):
        """
        Send product update to WebSocket.
        Called when a product is created/updated.
        """
        await self.send(text_data=json.dumps({
            'type': 'product_update',
            'data': event['data']
        }))

    async def send_new_arrivals(self):
        """Fetch and send new arrivals to client."""
        products = await self.get_new_arrivals()
        await self.send(text_data=json.dumps({
            'type': 'new_arrivals',
            'data': products
        }))

    async def send_featured_products(self):
        """Fetch and send featured products to client."""
        products = await self.get_featured_products()
        await self.send(text_data=json.dumps({
            'type': 'featured_products',
            'data': products
        }))

    @database_sync_to_async
    def get_new_arrivals(self):
        """Get new arrival products from database."""
        products = Product.objects.filter(new_arrival=True).select_related('category').prefetch_related('reviews')[:8]
        serializer = ProductSerializer(products, many=True)
        return serializer.data

    @database_sync_to_async
    def get_featured_products(self):
        """Get featured products from database."""
        products = Product.objects.filter(featured=True).select_related('category').prefetch_related('reviews')[:8]
        serializer = ProductSerializer(products, many=True)
        return serializer.data
