from django.db import models
import markdown
# Create your models here.
from authentication.models import User


class Question(models.Model):
    """
    Question 模型
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=2000)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
        ordering = ('-update_date',)  # 比须是元组

    def __str__(self):
        return self.title

    def get_answers(self):
        return Answer.objects.filter(question=self)

    def get_answers_count(self):
        return Answer.objects.filter(questions=self).count()

    def get_description_as_markdown(self):  # 此方法将问题文本渲染为 Markdown 格式
        return markdown.markdown(self.description, safe_mode='escape')


class Answer(models.Model):
    """
    Answer for a question.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    description = models.TextField(max_length=2000)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'
        ordering = ('create_date',)

    def __str__(self):
        return self.description

    def get_description_as_markdown(self):  # 此方法将回答文本渲染为 Markdown 格
        return markdown.markdown(self.description, safe_mode='escape')
