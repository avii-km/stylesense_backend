"""stylesense_proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from stylesense_proj import views
from application_config.base_conf import API_BASE_PATH, MIDDLEWARE_MAPPING
from stylesense_proj.apps.feature_extraction import urls as feature_extraction_urls

urlpatterns = [
                  path(f'', views.home),
                  path(f'stylesense/api/feature_extraction/', include(feature_extraction_urls)),
                  path(f"health/", views.health,
                       {"skip_auth_middleware_list": []},
                       name='health'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
