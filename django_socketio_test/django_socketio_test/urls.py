from __future__ import absolute_import
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from socketio import sdjango


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^socket\.io/', include(sdjango)),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
