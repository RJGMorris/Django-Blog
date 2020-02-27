from django.urls import path
from .views import PostListView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView, PostLikedByListView, \
     CommentDeleteView, CommentUpdateView, post_detail_view, \
     FeedView, UserFollowingListView, UserFollowersListView
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('user/<str:username>/following/', UserFollowingListView.as_view(), name='user-following'),
    path('user/<str:username>/followers/', UserFollowersListView.as_view(), name='user-followers'),
    path('post/<int:pk>/', post_detail_view, name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/likes', PostLikedByListView.as_view(), name='post-likes'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    path('about/', views.about, name='blog-about'),
    path('feed/', FeedView.as_view(), name='blog-feed'),
]
