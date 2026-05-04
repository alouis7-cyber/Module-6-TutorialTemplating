from django.shortcuts import render, redirect
from .forms import ContactForm
from .models import ContactMessage, Post


def home(request):
    return render(request, 'blog/home.html')


def contact(request):
    form = ContactForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        ContactMessage.objects.create(
            name=form.cleaned_data['name'],
            message=form.cleaned_data['message']
        )
        return redirect('contact')

    messages = ContactMessage.objects.all().order_by('-created_at')

    context = {
        'form': form,
        'messages': messages,
    }

    return render(request, 'blog/contact.html', context)


def posts(request):
    posts = Post.objects.all().order_by('-created_at')

    context = {
        'posts': posts
    }

    return render(request, 'blog/post.html', context)

