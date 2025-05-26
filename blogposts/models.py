from django.db import models
from user.models import Bloguser
from django.utils import timezone

class Posts(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField()
    author = models.ForeignKey(Bloguser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    author = models.ForeignKey(Bloguser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
