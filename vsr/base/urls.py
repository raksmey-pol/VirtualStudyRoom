from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginForm, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.regUser, name='register'),
    path('', views.home, name='home'),
    path('room/<int:pk>/', views.room, name='room'),
    path('create_room/', views.createRoom, name='create_room'),
    path('update_room/<int:pk>/', views.updateRoom, name='update_room'),
    path('delete_room/<int:pk>/', views.deleteRoom, name='delete_room'), 
    path('delete_msg/<int:pk>', views.deleteMsg, name='delete_msg'),
    path('update_msg/<int:pk>/', views.updateMsg, name='update_msg'),
    path('add_todo/', views.add_todo, name='add_todo'),
    path('delete_todo/<int:task_id>/', views.delete_todo, name='delete_todo'),
]