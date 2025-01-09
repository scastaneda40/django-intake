from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import logout
from django.shortcuts import redirect
from .views import register

def custom_logout(request):
    logout(request)
    return redirect('/')  # Redirect to home or another page after logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('intake.urls')),
    path('register/', register, name='register'),
    path('accounts/logout/', custom_logout, name='logout'),  # Custom logout
    path('accounts/', include('django.contrib.auth.urls')),  # Other auth URLs
]

