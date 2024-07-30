from django.urls import path
from . import views

urlpatterns = [
    path('auth/register/' , views.UserRegisterView.as_view() , name='user_reg'),
    path('auth/login/' , views.UserLoginView.as_view() , name='user_reg'),
    path('auth/users/' , views.UserDetailView.as_view() , name='user_detail'),

    path('articles/' , views.ArticleView.as_view() , name='articles'),
    path('articles/<int:pk>' , views.ArticleView.as_view() , name='articles_detail'),

]   