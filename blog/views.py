from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse
from .models import Post, Comment
from .forms import CommentForm


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = User
    template_name = 'blog/user_posts.html'
    context_object_name = 'profile'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        return User.objects.filter(username=self.kwargs.get('username'))


class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    success_message = "Post Created"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    success_message = "Post Updated"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/blog/'
    success_message = "Post Deleted"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(PostDeleteView, self).delete(request, *args, **kwargs)


def post_detail_view(request, pk):
    post = Post.objects.filter(pk=pk)
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            form.instance.post = post.get()
            form.save()
        return redirect('/blog/post/{}/#comment'.format(pk))

    context = {'object': post, 'form': form}
    return render(request, 'blog/post_detail.html', context)


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Comment
    fields = ['content', ]
    success_message = "Comment Updated"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return False

    def get_success_url(self):
        comment = get_object_or_404(Comment, id=self.kwargs.get('pk'))
        return reverse('post-detail', kwargs={'pk': comment.post.pk})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    success_message = "Comment Deleted"

    def get_success_url(self):
        comment = get_object_or_404(Comment, id=self.kwargs.get('pk'))
        return reverse('post-detail', kwargs={'pk': comment.post.pk})

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return False

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(CommentDeleteView, self).delete(request, *args, **kwargs)


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


class FeedView(ListView):
    model = Post
    template_name = 'blog/feed.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserFollowingListView(ListView):
    model = User
    template_name = 'blog/user_following.html'
    context_object_name = 'profile'

    def get_queryset(self):
        return User.objects.filter(username=self.kwargs.get('username'))


class UserFollowersListView(ListView):
    model = User
    template_name = 'blog/user_followers.html'
    context_object_name = 'profile'

    def get_queryset(self):
        return User.objects.filter(username=self.kwargs.get('username'))


class PostLikedByListView(ListView):
    model = Post
    template_name = 'blog/post_likes.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.filter(id=self.kwargs.get('pk'))


@login_required
def like_post(request, pk):
    user = request.user
    post_to_like = Post.objects.get(pk=pk)

    user.profile.liked_posts.add(post_to_like)
    post_to_like.liked_by.add(user)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/blog/'))


@login_required
def un_like_post(request, pk):
    user = request.user
    post_to_un_like = Post.objects.get(pk=pk)

    user.profile.liked_posts.remove(post_to_un_like)
    post_to_un_like.liked_by.remove(user)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/blog/'))
