"""
URL configuration for blog_service project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('healthz/', include('core.urls')),
    path('api/', include('categories.urls')),
    path('api/', include('posts.urls')),
]