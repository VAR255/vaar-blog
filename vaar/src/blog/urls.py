from django.urls import path
from . views import home_views, post_single, CatListView, addcomment, web_home



app_name = 'blog'


urlpatterns = [
    path('', web_home, name='web-home'),
    path('blog/', home_views, name='home' ),
    path('addcomment/', addcomment, name='addcomment'),
    path('<slug:post>/', post_single, name='post_single'),
    path('category/<category>/', CatListView.as_view(), name='category'),
]
