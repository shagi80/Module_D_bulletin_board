""" URL configuration for b_board project """
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),    
    path('tinymce/', include('tinymce.urls'), name='tinymce_url'),
    path('', include('advert.urls')),
    path('accounts/', include('allauth.urls')),
]
