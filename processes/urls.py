from django.urls import path
from . import views
urlpatterns = [
    path('create_process/',views.create_process_steps, name = 'create_process'),
    path('process_list/',views.process_list, name = 'process_list'),
    path('process_detail/', views.process_detail, name = 'process_detail'),
]