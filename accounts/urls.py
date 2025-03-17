from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import home, evaluation_input, evaluation_complete,  evaluation_result_list, evaluation_result_detail

urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('', home, name='home'),
    path('evaluation/input/<str:reviewee_name>/', evaluation_input, name='evaluation_input'),
    path('evaluation/complete/', evaluation_complete, name='evaluation_complete'),
    path('evaluation/result/', evaluation_result_list, name='evaluation_result_list'),
    path('evaluation/result/<str:form_title>/', evaluation_result_detail, name='evaluation_result_detail'),  # 評価結果詳細

    #管理者用
    # path('admin/evaluation/list/', admin_evaluation_list, name='admin_evaluation_list'),
    # path('admin/evaluation/detail/<str:username>/<str:form_title>/', admin_evaluation_detail, name='admin_evaluation_detail'),
    # path('accounts/admin/evaluation/detail/<str:username>/<str:form_title>/', admin_evaluation_detail, name='admin_evaluation_detail'),
]
