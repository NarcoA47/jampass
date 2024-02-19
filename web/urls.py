from django.urls import path
from .import views


urlpatterns = [
    path('', views.home, name="home"),
    # path('<int:pk>', views.all_details, name="details"),
    path('Signup/', views.register, name="register"),
    path('logout/', views.logout, name="logout"),
    path('login/', views.login, name="login"),
    # path('<int:pk>/', views.balance, name="balance"),
    path('<int:pk>', views.getting, name="getting"),
    path('user_keys/', views.user_keys, name='user_keys'),
]

