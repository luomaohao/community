from django.urls import include, path
#  django 内置的认证视图
from django.contrib.auth import views as auth_views

from .views import UserSignView


app_name = 'authentication'


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='authentication/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', UserSignView.as_view(), name='signup'),
]