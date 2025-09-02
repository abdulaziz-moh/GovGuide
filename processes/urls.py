from django.urls import path
from . import views
urlpatterns = [
    path('create_process/',views.create_process_steps, name = 'create_process'),
    path('process_list/',views.process_list, name = 'process_list'),
    path('process_detail/<int:pk>/', views.process_detail, name = 'process_detail'),
    path('process_delete/<int:pk>/', views.process_delete, name = 'process_delete'),
    path('process_update/<int:pk>/', views.process_update, name = 'process_update'),

    path("base/", views.baseprocess, name = "base"),
    path("settings/", views.baseprocess, name = "settings"),
    path('personal_posts/',views.personal_posts, name="personal_posts"),
    path('success_page/',views.success_page, name = "success_page"),
    path('notification_page/',views.baseprocess, name = "notification_page"),
    path('contact_us/',views.baseprocess, name = "contact_us"),

    
    
]
