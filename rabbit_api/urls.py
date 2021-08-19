import debug_toolbar
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    url(r'^__debug__/', include(debug_toolbar.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('api.urls'))
]

if settings.DEBUG:
    from django.conf.urls.static import static
    import debug_toolbar
    import mimetypes
    
    mimetypes.add_type("application/javascript", ".js")
    
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
