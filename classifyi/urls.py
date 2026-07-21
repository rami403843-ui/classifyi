from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # Готовые страницы входа/выхода от Django (login, logout)
    path('accounts/', include('django.contrib.auth.urls')),
    # Наше приложение с объявлениями
    path('', include('ads.urls')),
]

# Раздача загруженных фото в режиме разработки
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
