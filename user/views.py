import os
import uuid

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, UserUpdateForm, LoginForm
from django.conf import settings
from .models import Bloguser

# Create your views here.
def customauthenticate(username, raw_password):
    try:
        user= Bloguser.objects.get(username=username)
        if check_password(raw_password, user.password):
            return user
    except Bloguser.DoesNotExist:
        return None
    return None




def signup_view(request):
            if request.method == 'POST':
                usercreationform= CustomUserCreationForm(request.POST, request.FILES)
                if usercreationform.is_valid():
                    user= usercreationform.save(commit=False)
                    uploaded_file= request.FILES.get('image')
                    user.password= make_password(usercreationform.cleaned_data['password1'])
                    user.save()

                    if uploaded_file:
                        filename = f"{uuid.uuid4().hex}_{uploaded_file.name}"
                        folder_path = os.path.join('user_uploads', user.username)  # Folder named after username
                        file_path = os.path.join(folder_path, filename)
                        full_path = os.path.join(settings.MEDIA_ROOT, file_path)
                        os.makedirs(os.path.dirname(full_path), exist_ok=True)

                        with open(full_path, 'wb+') as f:
                            for chunks in uploaded_file.chunks():
                                f.write(chunks)
                        user.image = file_path

                    user.save()
                    login(request, user)
                    return redirect('main_view')
                else:
                    print(usercreationform.errors)
                    return render(request, 'user/signup.html', {'form': usercreationform})

            else:
                usercreationform= CustomUserCreationForm()
                return render(request, 'user/signup.html', {'form': usercreationform})


def logout_view(request):
    logout(request)
    return redirect('main_view')




def profile_view(request, user_id):
    user= Bloguser.objects.get(id=user_id)
    if request.method == 'POST':
        form= UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user= form.save(commit=False)
            uploaded_file= request.FILES.get('image')
            if uploaded_file:
                filename = f"{uuid.uuid4().hex}_{uploaded_file.name}"
                folder_path = os.path.join('user_uploads', user.username)  # Folder named after username
                file_path = os.path.join(folder_path, filename)
                full_path = os.path.join(settings.MEDIA_ROOT, file_path)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)

                with open(full_path, 'wb+') as f:
                    for chunks in uploaded_file.chunks():
                        f.write(chunks)
                user.image = file_path

            user.save()
            return redirect('main_view')
        else:
            print(form.errors.as_json())


    else:
        user= Bloguser.objects.get(id=user_id)
        form= UserUpdateForm(instance=user)

    return render(request, 'user/profile.html', {'form': form, 'user': user, 'MEDIA_URL': settings.MEDIA_URL})

def login_view(request):
    if request.method == "POST" :
        loginuser= LoginForm(request.POST)
        if loginuser.is_valid():
            username= loginuser.cleaned_data['username']
            password= loginuser.cleaned_data['password']
            user= customauthenticate(username=username, raw_password=password)
            if user is not None:
                login(request, user)
                return redirect('main_view')
            else:
                print(user)
                return render(request, 'user/login.html', {'form': loginuser})
    else:
        loginuser= LoginForm()
        return render(request, 'user/login.html', {'form': loginuser})