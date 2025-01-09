# intake/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('submit/', views.submit_form, name='submit_form'),
    path('history/', views.submission_history, name='submission_history'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/change_status/<int:submission_id>/<str:status>/', views.change_status, name='change_status'),
]
