from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from accounts.models import Profile



# Create your models here.
def user_directory_path(instance, filename):
    return 'posts/{0}/{1}'.format(instance.id, filename)


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    
class Post(models.Model):

    class NewManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')

    options = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )

    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)
    title = models.CharField(max_length=250)
    excerpt = models.TextField(null=True)
    image = models.ImageField(upload_to=user_directory_path, default='posts/default.jpg')
    image_caption = models.CharField(max_length=100, default='Phot by Blog')
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    publish = models.DateTimeField(auto_now=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    favourites = models.ManyToManyField(User, related_name='favourite', default=None, blank=True)
    status = models.CharField(max_length=10, choices=options, default='draft')
    likes = models.ManyToManyField(User, related_name='like', default=None, blank=True,)
    like_count = models.BigIntegerField(default=0)
    objects = models.Manager()
    newmanager = NewManager()


    def get_absolute_url(self):
        return reverse("blog:post_single", args=[self.slug])
    

    class Meta:
        ordering = ('-publish',)
    
    def __str__(self):
        return self.title


class Comment(MPTTModel):
    author = models.ForeignKey(User, related_name='author', on_delete=models.CASCADE, default=None, blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    content = models.TextField()
    likes_comment = models.ManyToManyField(User, default=None, blank=True, related_name='comment_like')
    publish = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.content



 
    

    
