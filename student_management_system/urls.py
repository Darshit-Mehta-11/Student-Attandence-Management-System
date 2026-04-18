from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('homepage.urls')),
    path('', include('results.urls')),
    path('', include('student.urls')),
    path('', include('teachers.urls')),
]
