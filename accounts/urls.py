from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import home

urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('', home, name='home'),  
]
