from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from . forms import UserLoginForm, PwdResetForm, PwdResetComfirmForm, PwdchangeForm


app_name = 'accounts'


urlpatterns = [
  
    path('login/', auth_views.LoginView.as_view(template_name="registration/login.html", authentication_form=UserLoginForm), name='login'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html', form_class=PwdchangeForm), name='pwdforgot'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="registration/password_reset_form.html", form_class=PwdResetForm), name='pwdreset'),
    path('password_reset_conform/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html', form_class=PwdResetComfirmForm), name='pwdresetconfirm'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit, name='edit'),
    path('profile/favourites/', views.favourite_list, name='favourite_list'),
    path('like/', views.like, name='like'),
    path('fav/<int:id>/', views.favourite_add, name='favourite_add'),
    path('profile/delete/', views.delete_user, name='deleteuser'),
    path('register/', views.accounts_register, name='register'),
    path('activate/<slug:uidb64>/<slug:token>', views.activate, name='activate'),   
]
