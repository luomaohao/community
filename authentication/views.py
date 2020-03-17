from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView
# Create your views here.

from .models import User
from .forms import SignUpForm


class UserSignView(CreateView):
    """
    用户注册
    """
    model = User
    form_class = SignUpForm
    template_name = 'authentication/signup.html'

    def form_valid(self, form):
        """
        保存并登录用户
        :param form:
        :return:
        """
        user = form.save()
        login(self.request, user)
        return redirect('home')
