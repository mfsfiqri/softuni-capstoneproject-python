from django import forms
from .models import Category, Tag, BlogPost, Comment

# add bootstrap class to form fields
class BootstrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BootstrapModelForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

# the forms below are used in the views
class CategoryForm(BootstrapModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

class TagForm(BootstrapModelForm):
    class Meta:
        model = Tag
        fields = ['name']

class BlogPostForm(BootstrapModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'image', 'content', 'category', 'tags']

class DeleteBlogPostForm(BlogPostForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'image', 'content']

class CommentForm(BootstrapModelForm):
    class Meta:
        model = Comment
        fields = ['content']