import time

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView

from .forms import PostCreateForm
from .models import Post, Album, HighLight
from .utils import get_contents, query_items


# Create your views here.

def generate_post(request):
    for item in get_contents():
        time.sleep(5)
        post, created = Post.objects.get_or_create(
            name=item
        )
    return redirect("blog:blog_list")


class HomeAboutPageView(View):
    def get(self, request):
        context = {
            "posts": Post.objects.all()[:2],
            "album": Album.objects.first(),
            "highlights": HighLight.objects.first(),
        }
        return render(request, "index.html", context)


class BloglistView(ListView):
    model = Post
    queryset = Post.objects.all()
    template_name = 'blog/blog_list.html'
    paginate_by = 21

    def get_queryset(self):
        query = self.request.GET.get('search')

        queryset = self.queryset.filter()
        ordering = self.get_ordering()
        if query:
            queryset = query_items(item=queryset, query=query)
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        album = Album.objects.all()
        context['albums'] = album
        return context


class HomeView(View):
    def get(self, request):
        return render(request, "blog/home.html", {"albums": Album.objects.all(),
                                                  "highlights": HighLight.objects.all(),
                                                  "post_list": Post.objects.all()[:6]
                                                  }
                      )


class BlogDetailView(DetailView):
    template_name = 'blog/blog_detail.html'
    model = Post
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = context['object']
        """ note this instance.get_content_type is from our models where we 
        linked the comment models and the blog models with content_type and object_id """
        return context


def update_post_view(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    form = PostCreateForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.warning(request, 'The form isn\'t valid')

    return render(request, 'blog/blog_update.html', {'form': form})


class DeletePostView(DeleteView):
    model = Post
    success_url = '/'


class AboutView(View):
    def get(self, request):
        return render(request, "about.html")


class AlbumDetailView(DetailView):
    template_name = 'album/album_detail.html'
    model = Album
    context_object_name = 'album'
