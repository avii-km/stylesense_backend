import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stylesense_proj.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
})


#
#  pip install Django
#
#  pip install channels
#
# pip install django-cors-headers
#
#
# pip install mysqlclient

# pip pip install torch
#
# pip install torchvision


