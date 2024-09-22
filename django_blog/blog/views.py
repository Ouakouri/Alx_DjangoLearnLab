from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django import forms

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile') 
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'blog/profile.html', {'form': form})

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post

# ListView for displaying all blog posts
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']  # Show latest posts first

# DetailView for a single blog post
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

# CreateView for new blog post creation
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']

    # Set the author of the post to the logged-in user
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# UpdateView for editing a post by the author
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']

    # Ensure the author is editing their own post
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# DeleteView for deleting a post by the author
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('posts')  # Redirect to the post list after deletion

    # Ensure only the author can delete their post
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, DeleteView
from .models import Post, Comment
from .forms import CommentForm

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post-detail', pk=post.id)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    success_url = reverse_lazy('post_list')  # Redirect after successful creation

    def form_valid(self, form):
        # Automatically set the post and author before saving
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        form.instance.post = post
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.kwargs['post_id']})

class CommentUpdateView(UpdateView):
    model = Comment
    fields = ['content']
    template_name = 'blog/comment_form.html'

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class CommentDeleteView(DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    success_url = '/'

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)

from django.db.models import Q
from django.shortcuts import render
from .models import Post

def post_search(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    return render(request, 'blog/post_search_results.html', {'query': query, 'results': results})


from taggit.models import Tag

def post_list_by_tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags__in=[tag])
    return render(request, 'blog/post_list_by_tag.html', {'tag': tag, 'posts': posts})
