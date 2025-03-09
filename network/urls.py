
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path('newpost/', views.newPost, name="newpost"),
    path('profile/<int:user_id>', views.profile, name="profile"),
    path('follow/', views.follow, name="follow"),
    path('unfollow/', views.unfollow, name="unfollow"),
    path('following/', views.following, name="following"),
    path('addlike/<int:post_id>', views.add_like, name="addlike"),
    path('removelike/<int:post_id>', views.remove_like, name="removelike"),
    path('edit/<int:id>', views.edit, name="edit")
]
