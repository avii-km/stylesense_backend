import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stylesense_proj.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
})



