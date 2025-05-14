import os
import uuid
from django.conf import settings
from .forms import PostForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Posts
from .forms import CommentForm  # We'll create this form shortly
from user.models import Bloguser
from django.contrib.auth.decorators import login_required
from .models import Comment
from django.contrib import messages
from django.http import Http404


def createpost_view(request):
    if request.method == 'POST':
        newpost = PostForm(request.POST, request.FILES)
        if newpost.is_valid():
            post = newpost.save(commit=False)
            post.author = request.user
            post.save()

            uploaded_image = request.FILES.get('image')
            if uploaded_image:
                filename = f"{uuid.uuid4().hex}_{uploaded_image.name}"
                folder_path = os.path.join('post_uploads', str(post.id))
                file_path = os.path.join(folder_path, filename)
                full_path = os.path.join(settings.MEDIA_ROOT, file_path)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)

                with open(full_path, 'wb+') as f:
                    for chunk in uploaded_image.chunks():
                        f.write(chunk)

                post.image = file_path
                post.save()

            return redirect('post_detail', post_id=post.id)
    else:
        newpost = PostForm()

    return render(request, 'blogposts/post_create.html', {'form': newpost})


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Posts, id=post_id)
    comments = Comment.objects.filter(post=post).order_by('-created_at')

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        comment_form = CommentForm()

    return render(request, 'blogposts/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'MEDIA_URL': settings.MEDIA_URL
    })


def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)


    if comment.author != request.user:
        return redirect('post_detail', post_id=comment.post.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=comment.post.id)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'blogposts/edit_comment.html', {
        'form': form,
        'comment': comment
    })


def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)


    if comment.author != request.user:
        return redirect('post_detail', post_id=comment.post.id)

    if request.method == "POST":
        comment.delete()
        return redirect('post_detail', post_id=comment.post.id)

    return render(request, 'blogposts/delete_comment.html', {
        'comment': comment
    })

def user_posts(request):

    posts = Posts.objects.filter(author=request.user)

    return render(request, 'blogposts/user_posts.html', {'posts': posts, 'MEDIA_URL': settings.MEDIA_URL})

@login_required
def edit_post(request, id):
    post = get_object_or_404(Posts, id=id)

    if post.author != request.user:
        return redirect('user_posts')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)

            uploaded_image = request.FILES.get('image')
            if uploaded_image:

                filename = f"{uuid.uuid4().hex}_{uploaded_image.name}"
                folder_path = os.path.join('post_uploads', str(post.id))
                file_path = os.path.join(folder_path, filename)
                full_path = os.path.join(settings.MEDIA_ROOT, file_path)

                os.makedirs(os.path.dirname(full_path), exist_ok=True)

                with open(full_path, 'wb+') as f:
                    for chunk in uploaded_image.chunks():
                        f.write(chunk)

                post.image = file_path

            post.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'blogposts/edit_post.html', {'form': form, 'post': post, 'MEDIA_URL': settings.MEDIA_URL})


@login_required
def delete_post(request, id):
    post = get_object_or_404(Posts, id=id)

    if post.author != request.user:
        messages.error(request, "You are not authorized to delete this post.")
        return redirect('user_posts')

    if request.method == 'POST':
        post.delete()
        messages.success(request, "Post deleted successfully!")
        return redirect('user_posts')

    return render(request, 'blogposts/delete_post.html', {'post': post})