from django import forms
from .models import Posts, Comment


class PostForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    class Meta:
        model = Posts
        fields = ['title', 'content', 'image']

        labels = {
            'title': 'Post Title',
            'content': 'Post Content',
            'image': 'Post Image',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  #
        labels = {
            'content': 'Your Comment'
        }
