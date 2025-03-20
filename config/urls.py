
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404
from pages.views import homeing
from django.shortcuts import render


# Asosiy 404 sahifasi
def custom_404_view(request, exception):
    return render(request, "404.html", status=404)


# DEBUG=True bo'lsa ham ishlashi uchun
if settings.DEBUG:
    def custom_404_debug(request, exception=None):
        return render(request, "404.html", status=404)


    handler404 = custom_404_debug
else:
    handler404 = custom_404_view


urlpatterns = [
    path('', homeing, name='home'),
    path('admin/', admin.site.urls),
    path('',include('pages.urls')),

]






#
# if settings.DEBUG:  # Faqat DEBUG=True bo'lsa ishlaydi
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)