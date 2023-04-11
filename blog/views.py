from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, DeleteView

from .forms import PostCreateForm
from .models import Post
from .utils import get_read_time, get_contents, query_items


# Create your views here.

def generate_post(request):
    for item in get_contents():
        post, created = Post.objects.get_or_create(
            name=item
        )
    return redirect("blog:blog_list")


class BloglistView(ListView):
    model = Post
    queryset = Post.objects.all()
    template_name = 'blog/blog_list.html'
    paginate_by = 20

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
