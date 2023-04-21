from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login-page"),
    path('logout/', views.logoutPage, name="logout-page"),
    path('', views.homepage, name="homepage"),
    path('room/<str:pk>/', views.room, name="room"),
    path('create-room/', views.createroom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
]