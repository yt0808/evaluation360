from django.contrib import admin
from django.urls import path, include  # path を正しくインポート
from django.contrib.auth.views import LoginView, LogoutView
from accounts.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('accounts/logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('', home, name='home'),  # ルートページ
]
