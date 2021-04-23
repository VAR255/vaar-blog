from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save



def user_directory_path(instance, filename):
    return 'users/avatars/{0}/{1}'.format(instance.user.id, filename)

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    avatar = models.ImageField(
        upload_to=user_directory_path, default='users/avatar.jpg', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.user.username
    


@ receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
