from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'images/favicon.ico', permanent=True)),
    path('admin/', admin.site.urls),
    path('', include('ginasio.urls')), # ou o nome que deste à tua app
]

# ESTA É A MAGIA PARA AS IMAGENS FUNCIONAREM LOCALMENTE
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
