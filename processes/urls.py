from django.urls import path
from . import views
urlpatterns = [
    path('create_process/',views.create_process_steps, name = 'create_process'),
    path('process_list/',views.process_list, name = 'process_list'),
    path('process_detail/<int:pk>/', views.process_detail, name = 'process_detail'),
    path("base/", views.baseprocess, name = "base"),
    path("profile/", views.baseprocess, name = "profile"),
    path("settings/", views.baseprocess, name = "settings"),
    path('personal_posts/',views.personal_posts, name="personal_posts"),
    path('success_page/',views.success_page, name = "success_page"),
    path('notification_page/',views.baseprocess, name = "notification_page"),
    path('contact_us/',views.baseprocess, name = "contact_us"),

    
    
]
