from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import logout
from django.shortcuts import redirect
from intake.views import register, custom_logout

def custom_logout(request):
    logout(request)
    return redirect('/')  # Redirect to home or another page after logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('intake.urls')),
    path('register/', register, name='register'),
    path('accounts/logout/', custom_logout, name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),  # Auth URLs
]


