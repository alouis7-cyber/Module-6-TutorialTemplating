from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import ContactForm, CommentForm, PostForm
from .models import ContactMessage, Post, Comment


# -----------------------------
# ADD POST (requires login)
# -----------------------------
@login_required
def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()

    return render(request, 'blog/add_post.html', {"form": form})


# -----------------------------
# HOME PAGE
# -----------------------------
def home(request):
    return render(request, 'blog/home.html')


# -----------------------------
# CONTACT PAGE
# -----------------------------
def contact(request):
    form = ContactForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        ContactMessage.objects.create(
            name=form.cleaned_data['name'],
            message=form.cleaned_data['message']
        )
        return redirect('contact')

    messages = ContactMessage.objects.all().order_by('-created_at')

    return render(request, 'blog/contact.html', {
        'form': form,
        'messages': messages,
    })


# -----------------------------
# POSTS LIST
# -----------------------------
def posts(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/post.html', {"posts": posts})


# -----------------------------
# POST DETAIL + COMMENTS
# -----------------------------
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all().order_by('-created')

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post', pk=post.pk)
    else:
        form = CommentForm()

    return render(request, 'blog/post.html', {
        "post": post,
        "comments": comments,
        "form": form,
    })
