from django.db import models
# 信号，新知识
from django.db.models.signals import post_save
from authentication.models import User


# Create your models here.
class Profile(models.Model):
    """
    profile of a user .
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    url = models.CharField(max_length=50, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    job_title = models.CharField(max_length=50, null=True, blank=True)
    avatar = models.ImageField(upload_to='pic_folder', default='img/user.png')

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    post_save.connect(create_user_profile, sender=User)
    post_save.connect(save_user_profile, sender=User)