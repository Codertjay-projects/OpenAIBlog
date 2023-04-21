from datetime import time

from celery import shared_task

from blog.utils import get_contents
from .models import Post
import time


@shared_task
def auto_get_datas():
    for item in get_contents():
        time.sleep(5)
        post, created = Post.objects.get_or_create(
            name=item
        )
