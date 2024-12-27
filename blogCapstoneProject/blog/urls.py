from django.urls import path, include

from blogCapstoneProject.blog import views
from .views import IndexView, AboutView, BlogListView, CategoryListView, TagListView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),
    path('blog/', include([
        path('', BlogListView.as_view(), name='blog'),
        path('<int:id>', views.blog_detail, name='blog_detail'),
        path('create/', views.blog_create, name='blog_create'),
        path('<int:id>/edit/', views.blog_edit, name='blog_edit'),
        path('<int:id>/delete/', views.blog_delete, name='blog_delete'),
        path('myblog', views.myblog, name='myblog'),
    ])),
    path('category/', include([
        path('', CategoryListView.as_view(), name='category'),
        path('<int:id>', views.category_detail, name='category_detail'),
        path('create/', views.category_create, name='category_create'),
    ])),
    path('tag/', include([
        path('', TagListView.as_view(), name='tag'),
        path('<int:id>', views.tag_detail, name='tag_detail'),
        path('create/', views.tag_create, name='tag_create'),
    ]))
]