from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views.generic import (CreateView, ListView)

from .models import Question, Answer
from .forms import AnswerForm, QuestionForm


# Create your views here.
@method_decorator([login_required], name='dispatch')
class CreateQuestionView(CreateView):
    """
    @method_decorator([login_required], name='dispatch')装饰器声明了只有登录用户才能访问此页面，
    这样避免了非登录用户创建问题的情况。
    继承自CreateView,可以很方便的给模板传入表单信息.
    model指定了创建的模型,
    form_class指定了使用的表单,也就是先前创建的QuestionForm,
    template_name指定使用的模板.

    form_valid是当表单传入合法数据后执行的方法.在传入合法数据后,
    使用form.save(commit=False)暂时先不将数据保存至数据库,
    先指定问题的提问人,创建时间和更改时间,最后再保存至数据库.
    在所有操作完成后,再重定向至问题详情页.
    """
    model = Question
    form_class = QuestionForm
    template_name = 'questions/ask_question.html'

    def form_valid(self, form):
        question = form.save(commit=False)  # 当commit 为false 则会生成一个对象
        question.user = self.request.user
        question.update_date = question.create_date
        question.save()
        form.save_m2m()
        messages.success(self.request, 'The question was created with success!')
        return redirect('questions:question_detail', question.pk)


class QuestionListView(ListView):
    """
    show the list of questions.
    继承自ListView可以很方便的向模板传入集合数据.
    model指定了使用的模型为Question,
    ordering指定按照更改的时间顺序排序,
    context_object_name指定了传入模板的上下文中集合的名称,
    queryset指定了返回的集合,这里返回了包含所有问题的集合,
    paginate_by指定每页显示的最多问题数
    """
    model = Question
    ordering = ('update_date')
    context_object_name = 'questions'
    template_name = 'questions/questions_list.html'
    queryset = Question.objects.all()
    paginate_by = 1


class QuestionDetailView(CreateView):
    """
    show question detail
    继承自CreateView,可以很方便的给模板传入表单信息.
    model指定了创建的模型,form_class指定了使用的表单,也就是先前创建的AnswerForm,
    template_name指定使用的模板.

    get_context_data方法是向模板传入上下文的关键方法.
    其中的super方法继承了父类的上下文,在这里我们增加传入了问题及其回答的字段
    """
    model = Answer
    form_class = AnswerForm
    template_name = 'questions/question_detail.html'

    def get_context_data(self, **kwargs):
        question_id = self.kwargs.get('pk')
        question = Question.objects.get(pk=question_id)
        kwargs['question'] = question
        if Answer.objects.filter(question=question):
            kwargs['answers'] = Answer.objects.filter(question=question)

        context = super().get_context_data(**kwargs)
        return context

@login_required
def create_answer(request, pk):
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = Answer()
            answer.user = request.user
            answer.question = Question.objects.get(pk=pk)
            answer.description = form.cleaned_data.get('description')
            answer.save()
            messages.success(request, 'The answer was created successfully.')
            return redirect('questions:question_detail', answer.question.pk)
    return redirect('questions:question_detail', pk)
