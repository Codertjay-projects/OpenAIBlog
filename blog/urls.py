from django.urls import path

from .views import (BloglistView,
                    BlogDetailView, generate_post, update_post_view, DeletePostView, AboutView, AlbumDetailView,
                    HomeView,HomeAboutPageView
                    )

app_name = 'blog'
urlpatterns = [
    path('', HomeAboutPageView.as_view(), name='home_about'),
    path('home/', HomeView.as_view(), name='home'),
    path('blog/list', BloglistView.as_view(), name='blog_list'),
    path('generate/post/', generate_post, name='generate_post'),
    path('about/me/', AboutView.as_view(), name='about'),
    path('album/<int:pk>/', AlbumDetailView.as_view(), name='album'),
    path('blog/<str:slug>/', BlogDetailView.as_view(), name='blog_detail'),
    path('blog/<str:slug>/update/', update_post_view, name='update_post_view'),
    path('blog/<str:slug>/delete/', DeletePostView.as_view(), name='delete'),

]
