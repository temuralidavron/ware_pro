
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404
from pages.views import custom_404,homeing

urlpatterns = [
    path('', homeing, name='home'),
    path('admin/', admin.site.urls),
    path('',include('pages.urls'))
]




handler404 = custom_404



if settings.DEBUG:  # Faqat DEBUG=True bo'lsa ishlaydi
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
