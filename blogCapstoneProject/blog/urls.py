from django.urls import path, include

from blogCapstoneProject.blog import views

urlpatterns = [
    path('', views.index, name='index'),
]