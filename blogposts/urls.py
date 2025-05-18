from django.urls import path
from . import views
from .views import createpost_view, post_detail, edit_comment, delete_comment, user_posts, edit_post, delete_post

urlpatterns=[
    path('', views.all_posts_view, name='all_posts'),
    path('createpost/',createpost_view, name='createpost_view' ),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('comment/edit/<int:comment_id>/', edit_comment, name='edit_comment'),
    path('comment/delete/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('user/posts/', user_posts, name='user_posts'),
    path('user/post/edit/<int:id>/', edit_post, name='edit_post'),
    path('user/post/delete/<int:id>/', delete_post, name='delete_post'),
]
