from django.shortcuts import render, redirect

# Create your views here.
def home(request):
    """
    主页
    :param request:
    :return:
    """
    return redirect('questions:question_list')