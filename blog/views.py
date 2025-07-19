from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from .forms import CommentForm
from .forms import PostForm
from django.contrib.auth.decorators import login_required
def home(request):
    return render(request, 'main/home.html')

from .models import Post

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'post/post_list.html', {'posts': posts})
def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    comments = post.Comment.objects.filter(post=post)
    is_liked = request.user.is_authenticated and post.Like.objects.filter(post=post, user=request.user).exists()
    return render(request, 'post/post_detail.html', {
        'post': post,
        'comments': comments,
        'is_liked': is_liked,
    })
@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # 👈 set the author
            post.save()
            return redirect('post_list')  # redirect to post list
    else:
        form = PostForm()
    return render(request, 'post/post_form.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return redirect('post_list')  # ❌ not your post

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'post/post_form.html', {'form': form})
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        return redirect('post_list')  # 🚫 Prevent other users from deleting

    post.delete()
    return redirect('post_list')

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post_list')  # Or a detail page if you have it
    else:
        form = CommentForm()

    return render(request, 'post/comment.html', {'form': form})