from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Built-in django admin (accessible at /admin/)
    path('admin/', admin.site.urls),

    # Application Modules
    path('', include('apps.destinations.urls')),
    path('', include('apps.accounts.urls')),
    path('', include('apps.trips.urls')),
    path('', include('apps.weather.urls')),
    path('', include('apps.bookings.urls')),
    path('', include('apps.ai_assistant.urls')),
    path('', include('apps.notifications.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
