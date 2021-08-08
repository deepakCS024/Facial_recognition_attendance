"""Attendence_System URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from attendence_sys.views import attendance_download
from django.conf.urls.static import static
from django.conf import settings

admin.site.site_header = "SVCE 20CS20 FINAL YEAR PROJECT "
admin.site.site_title = "FINAL YEAR PROJECT 20CS20"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('arkauth/',include("arkauth.urls")),
    path('', include('attendence_sys.urls')),
    path('attendance-download/',attendance_download,name='attendance_download'),

]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)