import pytest
from django.urls import reverse
from django.test import Client
from blogposts.models import Posts
from user.models import Bloguser

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def create_test_user(db):
    user = Bloguser.objects.create_user(username='testuser', email='test@example.com', password='password123', first_name='Test', last_name='User')
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
def logged_in_client(client, create_test_user):
    client.login(username='testuser', password='password123')
    return client

@pytest.mark.django_db
def test_all_posts_view_get(client, create_test_post):
    url = reverse('all_posts') 
    response = client.get(url)
    assert response.status_code == 200
    assert 'blogposts/all_posts.html' in [t.name for t in response.templates]
    assert 'all_posts' in response.context
    assert create_test_post in response.context['all_posts']

@pytest.mark.django_db
def test_signup_view_get(client):
    url = reverse('signup_view')
    response = client.get(url)
    assert response.status_code == 200
    assert 'user/signup.html' in [t.name for t in response.templates]

@pytest.mark.django_db
def test_signup_view_post_valid_data(client):
    url = reverse('signup_view')
    data = {
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password1': 'newpassword123',
        'password2': 'newpassword123',
        'first_name': 'New',
        'last_name': 'User'
    }
    response = client.post(url, data)
    assert response.status_code == 302 
    assert Bloguser.objects.filter(username='newuser').exists()

@pytest.mark.django_db
def test_signup_view_post_invalid_data(client):
    url = reverse('signup_view')
    data = {
        # 'username': 'newuser', # Omit username to make it invalid
        'email': 'invalid-email', # Still keep this invalid email
        'password1': 'newpassword123',
        'password2': 'newpassword123',
        'first_name': 'New',
        'last_name': 'User'
    }
    response = client.post(url, data)
    assert response.status_code == 200 
    assert 'user/signup.html' in [t.name for t in response.templates]
    assert not Bloguser.objects.filter(username='newuser').exists()

@pytest.mark.django_db
def test_post_detail_view_get_existing_post(logged_in_client, create_test_post):
    url = reverse('post_detail', args=[create_test_post.id])
    response = logged_in_client.get(url)
    assert response.status_code == 200
    assert 'blogposts/post_detail.html' in [t.name for t in response.templates]
    assert 'post' in response.context
    assert response.context['post'] == create_test_post

@pytest.mark.django_db
def test_post_detail_view_get_non_existing_post(logged_in_client):
    url = reverse('post_detail', args=[999]) 
    response = logged_in_client.get(url)
    assert response.status_code == 404

@pytest.mark.django_db
def test_login_view_get(client):
    url = reverse('login_view')
    response = client.get(url)
    assert response.status_code == 200
    assert 'user/login.html' in [t.name for t in response.templates]

@pytest.mark.django_db
def test_login_view_post_valid_credentials(client, create_test_user):
    url = reverse('login_view')
    data = {
        'username': 'testuser',
        'password': 'password123'
    }
    response = client.post(url, data)
    
    assert response.status_code == 302
    assert '_auth_user_id' in client.session 

@pytest.mark.django_db
def test_login_view_post_invalid_credentials(client):
    url = reverse('login_view')
    data = {
        'username': 'nonexistentuser',
        'password': 'wrongpassword'
    }
    response = client.post(url, data)
    assert response.status_code == 200 
    assert 'user/login.html' in [t.name for t in response.templates]
    assert '_auth_user_id' not in client.session
