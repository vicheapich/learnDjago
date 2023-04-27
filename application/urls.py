from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login-page"),

    path('resgister/', views.registerPage, name="resgister-page"),

    path('logout/', views.logoutPage, name="logout-page"),

    path('profile/<str:pk>/', views.userProfile, name="profile-page"),

    path('', views.homepage, name="homepage"),

    path('room/<str:pk>/', views.room, name="room"),

    path('create-room/', views.createroom, name="create-room"),

    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),

    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),

    path('update-user/', views.updateUser, name="update-user"),

    path('topics/', views.topicsPage, name="topics"),

    path('activity/', views.activityPage, name="activity"),
]