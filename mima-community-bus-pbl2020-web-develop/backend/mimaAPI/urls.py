from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('api/v1/bus/', include('bus.urls')),
    path('api/v1/web/', include('web.urls')),
    path('api/v1/', include('users.urls')),
    path('admin/', admin.site.urls)
]
