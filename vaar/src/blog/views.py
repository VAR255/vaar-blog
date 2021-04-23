from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from . models import Post, Comment, Category
from . forms import CommentForm
from django.views.generic import ListView


# Create your views here.
def web_home(request):
    post = Post.newmanager.all()
    context = {
        "post": post
    }
    return render(request, 'pages/index.html', context)
    
    
def home_views(request):
    queryset = Post.newmanager.all()
    context = {
        "posts": queryset 
    }
    return render(request, 'base/index.html', context)


def post_single(request, post):
    post = get_object_or_404(Post, slug=post, status='published')

    fav = bool

    if post.favourites.filter(id=request.user.id).exists():
        fav = True
        message= 'Successfully removed from your favourates !!'
    else:
        message= 'Successfully added to your favourates !!'

    comments = post.comments.order_by("-publish").filter(status=True)


    comment_form = CommentForm()

    context = {
        "post": post,
        "comments": comments,
        "comment_form": comment_form,
        "fav": fav,
        "message": message
    }
    return render(request, 'base/single.html', context)


def addcomment(request):
    comment_form = CommentForm(request.POST)
    if request.method == 'POST':
        if comment_form.is_valid():
            print(comment_form)
            user_comment = comment_form.save(commit=False)
            user_comment.author = request.user
            user_comment.save()
            result = comment_form.cleaned_data.get('content')
            user = request.user.username
            return JsonResponse({'result': result, 'user': user})

# Categories filtering

class CatListView(ListView):
    template_name = 'base/category.html'
    context_object_name = 'catlist'

    def get_queryset(self):
        content = {
            'cat': self.kwargs['category'],
            'posts': Post.objects.filter(category__name=self.kwargs['category']).filter(status='published')
        }
        return content
    

def category_list(request):
    category_list = Category.objects.all()
    context = {
        "category_list": category_list
    }
    return context