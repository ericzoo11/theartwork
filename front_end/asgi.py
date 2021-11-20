"""
ASGI config for front_end project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
import django 
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
#import canvas.routing
from channels.http import AsgiHandler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'front_end.settings')
django.setup()

# application = get_asgi_application()
application = ProtocolTypeRouter({
    "http": AsgiHandler(),
    #"http": get_asgi_application(),
    #"websocket": AuthMiddlewareStack(
    #    URLRouter(
    #        canvas.routing.websocket_urlpatterns
    #    )
    #),
})
