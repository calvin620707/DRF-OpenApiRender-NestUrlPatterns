"""demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from rest_framework.compat import urlparse
from rest_framework.schemas import get_schema_view
from rest_framework.renderers import JSONOpenAPIRenderer
from rest_framework.permissions import AllowAny

class JSONOpenAPIDeepRenderer(JSONOpenAPIRenderer):
    def get_paths(self, document):
        paths = {}

        tag = None
        for name, link in document.links.items():
            path = urlparse.urlparse(link.url).path
            method = link.action.lower()
            paths.setdefault(path, {})
            paths[path][method] = self.get_operation(link, name, tag=tag)

        for tag, section in document.data.items():
            if not section.links:
                sub_paths = self.get_paths(section)
                paths.update(sub_paths)
                continue

            for name, link in section.links.items():
                path = urlparse.urlparse(link.url).path
                method = link.action.lower()
                paths.setdefault(path, {})
                paths[path][method] = self.get_operation(link, name, tag=tag)

        return paths

schema_view = get_schema_view(
    title='Deep API Document',
    renderer_classes=[JSONOpenAPIDeepRenderer],
    permission_classes=[AllowAny]
)

default_schema_view = get_schema_view(
    title='API Document',
    renderer_classes=[JSONOpenAPIRenderer],
    permission_classes=[AllowAny]
)

urls = [
    path('v1.0/', include(([path('app/', include('app.urls'))], 'v1.0'))),
    path('v2.0/', include(([path('app/', include('app.urls'))], 'v2.0'))),
    path('default-schema.json', default_schema_view),
    path('deep-schema.json', schema_view),
]

urlpatterns = [path('demo/', include(urls))]
