from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from . forms import RegistrationForm, UserEditForm, UserProfileForm
from . token import account_activation_token
from django.contrib.auth.models import User
from django.contrib.auth import login
from . models import Profile
from blog.models import Post


# Create your views here.
@login_required
def like(request):
    if request.user.is_authenticated:
        like_post = bool
        if request.POST.get('action') == 'post':
            result = ''
            id = int(request.POST.get('postid'))
            print(id)
            post = get_object_or_404(Post, id=id)
            if post.likes.filter(id=request.user.id).exists():
                post.likes.remove(request.user)
                post.like_count -=1
                result = post.like_count
                post.save()
                like_post = True
            else:
                post.likes.add(request.user)
                post.like_count += 1
                result = post.like_count
                post.save()
            return JsonResponse({'result': result,})
    else:
        return render(request, 'registration/login.html')



@login_required
def favourite_list(request):
    new = Post.newmanager.filter(favourites=request.user)
    
    return render(request, 'accounts/favourites.html', {'new': new})

@login_required
def favourite_add(request, id):
    post = get_object_or_404(Post, id=id)
    if post.favourites.filter(id=request.user.id).exists():
        post.favourites.remove(request.user)
        context = {'message': 'Successfully saved to your favourates !!'}
    else:
        post.favourites.add(request.user)
        context = {'message': 'Successfully removed from your favourates !!'}
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
    



def avatar(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        avatar = Profile.objects.filter(user=user)
    else:
        avatar = []
    context = {
        "avatar": avatar,
    }
    return context


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form and user_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)
    return render(request, 'accounts/update.html', {'user_form': user_form, 'profile_form':profile_form})



@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {'section': 'profile'})


def accounts_register(request):
    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        print(registerForm)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate your account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return HttpResponse('registerd successfully and activation sent')
    else:
        registerForm = RegistrationForm()
    return render(request, 'registration/register.html', {'form': registerForm })


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user=None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('login')
    else:
        return render(request, 'registration/activation_invalid.html')


@login_required
def delete_user(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        user.is_active = False
        user.delete()
        return redirect('accounts:login')
    return render(request, 'accounts/delete.html')