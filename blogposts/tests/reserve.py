def test_post_author_relationship(create_test_post, create_test_user):
    post = create_test_post
    assert post.author == create_test_user


def test_post_updated_at_auto_now(create_test_post):
    post = create_test_post
    old_updated_at = post.updated_at
    post.title = 'Updated Test Post'
    post.save()
    assert post.updated_at > old_updated_at

def test_comment_creation(create_test_comment):
    comment = create_test_comment
    assert isinstance(comment, Comment)
    assert comment.content == 'This is a test comment.'
    assert comment.created_at is not None
    assert comment.updated_at is not None

def test_comment_relationships(create_test_comment, create_comment_post, create_comment_user):
    comment = create_test_comment
    assert comment.post == create_comment_post
    assert comment.author == create_comment_user

def test_comment_str_representation(create_test_comment):
    comment = create_test_comment
    assert str(comment) == f"Comment by {comment.author.username} on {comment.post.title}"

def test_comment_updated_at_auto_now(create_test_comment):
    comment = create_test_comment
    old_updated_at = comment.updated_at
    comment.content = 'Updated test comment.'
    comment.save()
    assert comment.updated_at > old_updated_at