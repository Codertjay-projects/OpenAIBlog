from django.urls import path

from .views import (BloglistView,
                    BlogDetailView, generate_post, update_post_view, DeletePostView
                    )

app_name = 'blog'
urlpatterns = [
    path('', BloglistView.as_view(), name='blog_list'),
    path('generate/post/', generate_post, name='generate_post'),
    path('<str:slug>/', BlogDetailView.as_view(), name='blog_detail'),
    path('<str:slug>/update/', update_post_view, name='update_post_view'),
    path('<str:slug>/delete/', DeletePostView.as_view(), name='delete'),

]
