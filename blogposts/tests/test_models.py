import pytest
from django.utils import timezone
from blogposts.models import Posts, Comment
from user.models import Bloguser

@pytest.fixture
def create_test_user(db):
    user = Bloguser.objects.create_user(username='testuser', email='test@example.com', password='password123')
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
def create_comment_for_test_post(db, create_test_post, create_test_user):
    comment = Comment.objects.create(
        post=create_test_post,
        author=create_test_user,
        content='This is a test comment.'
    )
    return comment

@pytest.mark.django_db
def test_post_creation(create_test_post):
    post = create_test_post
    assert isinstance(post, Posts)
    assert post.title == 'Test Post'
    assert post.content == 'This is a test post content.'
    assert post.image == 'test_image.jpg'
    assert post.created_at is not None
    assert post.updated_at is not None

@pytest.mark.django_db
def test_comment_creation(create_comment_for_test_post):
    comment = create_comment_for_test_post
    assert isinstance(comment, Comment)
    assert comment.content == 'This is a test comment.'
    assert comment.post is not None
    assert comment.author is not None
    assert comment.created_at is not None
    assert comment.updated_at is not None

@pytest.mark.django_db
def test_post_str_representation(create_test_post):
    post = create_test_post
    assert str(post) == post.title

@pytest.mark.django_db
def test_comment_str_representation(create_comment_for_test_post):
    comment = create_comment_for_test_post
    expected_str = f"Comment by {comment.author.username} on {comment.post.title}"
    assert str(comment) == expected_str

@pytest.mark.django_db
def test_post_deletion_cascades_comments(create_test_post, create_comment_for_test_post):
    post = create_test_post
    comment = create_comment_for_test_post
    assert comment.post == post  
    post_id = post.id
    comment_id = comment.id
    post.delete()
    with pytest.raises(Posts.DoesNotExist):
        Posts.objects.get(id=post_id)
    
    with pytest.raises(Comment.DoesNotExist):
        Comment.objects.get(id=comment_id)

@pytest.mark.django_db
def test_user_deletion_cascades_posts_and_comments(create_test_user, create_test_post, create_comment_for_test_post):
    user = create_test_user
    post = create_test_post
    comment = create_comment_for_test_post

    assert post.author == user
    assert comment.author == user

    user_id = user.id
    post_id = post.id
    comment_id = comment.id

    user.delete()


    with pytest.raises(Bloguser.DoesNotExist):
        Bloguser.objects.get(id=user_id)

    with pytest.raises(Posts.DoesNotExist):
        Posts.objects.get(id=post_id)
    

    with pytest.raises(Comment.DoesNotExist):
        Comment.objects.get(id=comment_id)
