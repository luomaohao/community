from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
# 新知识
from django.utils.decorators import method_decorator
from django.views.generic import (TemplateView, UpdateView)
# Create your views here.

from authentication.models import User
from .models import Profile


@method_decorator([login_required], name='dispatch')
class ProfileDetailView(TemplateView):
    """
    show the profile
    """
    # 如何使用django中的通用视图
    # 指定使用的数据模型
    model = Profile
    # 指定使用的模板文件，用于渲染数据
    template_name = 'user_profile/profile.html'

    # 重写这个方法，用于向模板传递数据
    def get_context_data(self, **kwargs):
        # 获取用户id
        context = super(ProfileDetailView, self).get_context_data(**kwargs)  # why?
        user_id = self.kwargs.get('user_id')  # why?
        context['user'] = User.objects.get(id=user_id)
        context['profile'] = Profile.objects.get(user_id=user_id)
        return context


class UpdateProfileView(UpdateView):
    """
    update the profile
    """
    model = Profile
    fields = ['avatar', 'url', 'location']
    template_name = 'user_profile/profile_update.html'

    def get_object(self, queryset=None):
        # 重写方法,获得当前视图使用的对象
        return Profile.objects.get(user_id=self.kwargs.get('user_id'))

    def form_valid(self, form):
        """
        do something before save the profile
        :param form:
        :return:
        """
        profile = form.save(commit=False)
        profile.save()
        form.save_m2m()
        return redirect('user_profile:profile', self.kwargs.get('user_id'))

    def get_success_url(self):
        return reverse('user_profile:profile', self.kwargs.get('user_id'))
