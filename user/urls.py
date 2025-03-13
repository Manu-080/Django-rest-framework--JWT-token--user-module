from django.urls import path

from . import views

urlpatterns = [
    path('users/', views.UsersView.as_view()),
    path('users/<int:pk>', views.UserView.as_view()),

    path('register/', views.RegisterView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.Logout.as_view(), name='logout'),

    path('profile/', views.UserProfile.as_view(), name='profile'),
    
]
