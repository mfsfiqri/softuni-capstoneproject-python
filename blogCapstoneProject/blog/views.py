from django.contrib.auth.decorators import login_required
from django.views.generic import (
    TemplateView,
    ListView,
)
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Tag, BlogPost, Comment
from .forms import CategoryForm, TagForm, BlogPostForm, CommentForm, DeleteBlogPostForm
# Create your views here.

# views for unauthenticated user
class IndexView(TemplateView):
    template_name = 'index.html'

class AboutView(TemplateView):
    template_name = 'about.html'

# login required
# blog
class BlogListView(ListView):
    model = BlogPost
    template_name = 'blog/blog.html'
    context_object_name = 'posts'
    ordering = ['-created_at']


def blog_detail(request, id):
    post = get_object_or_404(BlogPost, id=id)
    comments = Comment.objects.filter(blog=post).order_by('-created_at')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = post
            comment.author = request.user
            comment.save()
            return redirect('blog_detail', id=id)
    else:
        form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'form': form
    }
    return render(request, 'blog/blog_detail.html', context=context)

@login_required
def myblog(request):
    posts = BlogPost.objects.filter(author=request.user).order_by('-created_at')
    context = {
        'posts': posts
    }
    return render(request, 'blog/myblog.html', context=context)

@login_required
def blog_create(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('blog')
    else:
        form = BlogPostForm()

    context = {
        'form': form,
    }
    return render(request, 'blog/blog_create.html', context=context)

@login_required
def blog_edit(request, id):
    post = get_object_or_404(BlogPost, id=id, author=request.user)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog_detail', id=id)
    else:
        form = BlogPostForm(instance=post)

    context = {
        'form': form,
        'post': post
    }
    return render(request, 'blog/blog_edit.html', context=context)


@login_required
def blog_delete(request, id):
    post = get_object_or_404(BlogPost, id=id, author=request.user)
    form = DeleteBlogPostForm(instance=post)
    if request.method == 'POST':
        post.delete()
        return redirect('blog')

    context = {
        'post': post,
        'form': form
    }
    return render(request, 'blog/blog_delete.html', context=context)

class CategoryListView(ListView):
    model = Category
    template_name = 'category/category.html'
    context_object_name = 'categories'
    ordering = ['name']

def category_detail(request, id):
    category = get_object_or_404(Category, id=id)
    posts = BlogPost.objects.filter(category=category).order_by('-created_at')
    return render(request, 'category/category_detail.html', {'category': category, 'posts': posts})

@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category')
    else:
        form = CategoryForm()
    return render(request, 'category/category_create.html', {'form': form})

class TagListView(ListView):
    model = Tag
    template_name = 'tag/tag.html'
    context_object_name = 'tags'
    ordering = ['name']

def tag_detail(request, id):
    tag = get_object_or_404(Tag, id=id)
    posts = BlogPost.objects.filter(tags=tag).order_by('-created_at')
    return render(request, 'tag/tag_detail.html', {'tag': tag, 'posts': posts})

@login_required
def tag_create(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tag')
    else:
        form = TagForm()
    return render(request, 'tag/tag_create.html', {'form': form})