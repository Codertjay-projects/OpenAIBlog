from django.urls import path

from .views import (BloglistView,
                    BlogDetailView, generate_post, update_post_view, DeletePostView, AboutView, AlbumDetailView
                    )

app_name = 'blog'
urlpatterns = [
    path('', BloglistView.as_view(), name='blog_list'),
    path('generate/post/', generate_post, name='generate_post'),
    path('about/me/', AboutView.as_view(), name='about'),
    path('album/<int:pk>/', AlbumDetailView.as_view(), name='album'),
    path('<str:slug>/', BlogDetailView.as_view(), name='blog_detail'),
    path('<str:slug>/update/', update_post_view, name='update_post_view'),
    path('<str:slug>/delete/', DeletePostView.as_view(), name='delete'),

]
