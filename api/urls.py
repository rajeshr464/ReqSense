from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('dataset/<int:dataset_id>/blueprint/', views.generate_blueprint, name='generate_blueprint'),
    path('dataset/<int:dataset_id>/data/', views.get_dashboard_data, name='get_dashboard_data'),
    path('dataset/<int:dataset_id>/chat/', views.chat_query, name='chat_query'),
    path('dataset/<int:dataset_id>/insights/', views.get_insights, name='get_insights'),
    path('dataset/<int:dataset_id>/export_pdf/', views.export_pdf, name='export_pdf'),
]
