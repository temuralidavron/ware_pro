
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('pages.urls'))
]





if settings.DEBUG:  # Faqat DEBUG=True bo'lsa ishlaydi
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
