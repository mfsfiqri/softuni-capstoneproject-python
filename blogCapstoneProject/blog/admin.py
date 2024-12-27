from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html, mark_safe
from django.urls import reverse
from .models import Category, Tag, BlogPost, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # 1. Custom List Display
    list_display = ('name', 'description', 'blog_count')

    # 2. Search and Filtering
    search_fields = ['name', 'description']
    list_filter = ['name']

    # 3. Custom Method to Show Blog Count
    def blog_count(self, obj):
        return obj.blogpost_set.count()

    blog_count.short_description = 'Number of Blog Posts'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    # 4. Custom List Display with Annotation
    list_display = ('name', 'used_in_posts')

    def used_in_posts(self, obj):
        return obj.blogpost_set.count()

    used_in_posts.short_description = 'Used in Posts'


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    # 5. Comprehensive List Display
    list_display = (
        'title',
        'category',
        'author',
        'created_at',
        'tags_list',
        'post_actions'
    )

    # 6. Advanced Filtering
    list_filter = [
        'category',
        'author',
        ('created_at', admin.DateFieldListFilter)
    ]

    # 7. Search Capabilities
    search_fields = ['title', 'content', 'author__username']

    # 8. Custom Method for Tags
    def tags_list(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])

    tags_list.short_description = 'Tags'

    # 9. Custom Method for Post Actions
    def post_actions(self, obj):
        return format_html(
            '<a class="button" href="{}">View</a>',
            reverse('admin:blog_blogpost_change', args=[obj.pk])
        )

    post_actions.short_description = 'Actions'

    # 10. Custom Actions
    actions = ['mark_featured']

    def mark_featured(self, request, queryset):
        # Example custom action (you'd need to add a featured field to the model)
        queryset.update(is_featured=True)

    mark_featured.short_description = "Mark selected posts as featured"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # 11. Comprehensive List Display
    list_display = (
        'short_content',
        'blog',
        'author',
        'created_at',
        'blog_link'
    )

    # 12. Advanced Filtering
    list_filter = [
        'author',
        ('created_at', admin.DateFieldListFilter)
    ]

    # 13. Search Capabilities
    search_fields = ['content', 'author__username', 'blog__title']

    # 14. Custom Methods
    def short_content(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content

    short_content.short_description = 'Content'

    def blog_link(self, obj):
        return format_html(
            '<a href="{}">View Post</a>',
            reverse('admin:blog_blogpost_change', args=[obj.blog.pk])
        )

    blog_link.short_description = 'Related Post'


# Global Admin Site Customization
admin.site.site_header = 'Blog Management Admin'
admin.site.site_title = 'Blog Admin'
admin.site.index_title = 'Welcome to Blog Administration'