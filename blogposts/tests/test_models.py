import pytest
from django.utils import timezone
from blogposts.models import Posts, Comment
from user.models import Bloguser

@pytest.fixture
def create_test_user(db):
    user = Bloguser.objects.create_user(username='testuser', email='test@example.com', password='password123')
    return user

@pytest.fixture
def create_comment_user(db):
    user = Bloguser.objects.create_user(username='commentuser', email='comment@example.com', password='password123')
    return user

@pytest.fixture
def create_test_post(db, create_test_user):
    post = Posts.objects.create(
        title='Test Post',
        content='This is a test post content.',
        author=create_test_user,
        image='test_image.jpg'
    )
    return post

@pytest.fixture
def create_comment_post(db, create_comment_user):
    post = Posts.objects.create(
        title='Comment Post',
        content='This post is for comments.',
        author=create_comment_user
    )
    return post

@pytest.fixture
def create_test_comment(db, create_comment_post, create_comment_user):
    comment = Comment.objects.create(
        post=create_comment_post,
        author=create_comment_user,
        content='This is a test comment.'
    )
    return comment

def test_post_creation(create_test_post):
    post = create_test_post
    assert isinstance(post, Posts)
    assert post.title == 'Test Post'
    assert post.content == 'This is a test post content.'
    assert post.image == 'test_image.jpg'
    assert post.created_at is not None
    assert post.updated_at is not None


