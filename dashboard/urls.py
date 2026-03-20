from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('dashboard/', views.index, name='index'),
    path('dashboard/<int:pk>/', views.view_dataset, name='view'),
    path('dashboard/<int:pk>/chat/', views.chat_terminal, name='chat'),
    path('dashboard/<int:pk>/reports/', views.reports_view, name='reports'),
    path('dashboard/<int:pk>/delete/', views.delete_dataset, name='delete'),
]
