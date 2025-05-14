from django.shortcuts import render
from blogposts.models import Posts
from django.conf import settings


def main_view(request):

    recent_posts = Posts.objects.all().order_by('-created_at')[:5]

    return render(request, 'main/main.html', {
        'recent_posts': recent_posts,
        'MEDIA_URL': settings.MEDIA_URL,
    })
