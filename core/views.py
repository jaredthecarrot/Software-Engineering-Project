from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile, User
from posts.models import Post, LikePost
from django.shortcuts import render, get_object_or_404
from messagingFeature.models import ChatChannel, ChatMessage
from messagingFeature.forms import ChatmessageCreateForm

from django.shortcuts import render, get_object_or_404
from django.contrib import messages


# Create your views here.
@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    
    # Fetch all posts with related user data
    posts = Post.objects.all().select_related('user')
    
    # Add likes and the profiles of users who liked each post
    for post in posts:
         # Check if the current user has liked the post
        post.liked_by_user = LikePost.objects.filter(post_id=post.id, user=request.user).exists()
        
        # Add a list of users who liked this post (limit to last 3)
        post.liked_users = LikePost.objects.filter(post_id=post.id).select_related('user')[:3]
    return render(request,'index.html', {'user_profile': user_profile, 'posts':posts})


@login_required(login_url='signin')
def profile(request):
    # Get the username from the query parameters
    username = request.GET.get('username')
    if not username:
        return HttpResponse("Username not provided", status=400)  # Handle missing username error
    
    # Find the target user based on the username
    target_user = get_object_or_404(User, username=username)
    chat_channel = ChatChannel.get_or_create_channel(request.user, target_user)
    chat_messages = chat_channel.chat_messages.all()[:30]
    form = ChatmessageCreateForm()
    
    if request.method == 'POST':
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.chat_channel = chat_channel 
            message.save()

    # Pass user data to the template
    return render(request, 'profile.html', {
        'chat_messages': chat_messages,
        'form': form,
        'target_user': target_user,
        'user_profile': target_user.profile,  # Assuming Profile model is related to User
        'profile_user_id': target_user.id
    })


@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']
            
            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']
            
            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        return redirect('settings')

    try:
             # Get profile information from form data
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            gender = request.POST.get('gender')
            dob = request.POST.get('dob')
            age = request.POST.get('age')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            bio = request.POST.get('bio')
            location = request.POST.get('location')
            theme = request.POST.get('theme')

            # Validate unique email if it's being changed
            if User.objects.filter(email=email).exclude(username=user_profile.username).exists():
                messages.error(request, 'This email is already associated with another account.')
                return redirect('settings')

             # Update the user's email and save
            user_profile.email = email
            user_profile.save()

            # Update Profile with new data
            user_profile.profileimg = user_profile.image
            user_profile.first_name = first_name
            user_profile.last_name = last_name
            user_profile.gender = gender
            user_profile.dob = dob
            user_profile.age = age
            user_profile.phone = phone
            user_profile.bio = bio
            user_profile.location = location
            user_profile.theme = theme
            user_profile.save()

            # Success message
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('settings')
        
    except Exception as e:
            # Error message
            messages.error(request, 'An error occurred. Please try again.')
            print(e)  # Optional: Print the error to console for debugging
            return redirect('settings')
    
    return render(request,'setting.html', {'user_profile': user_profile})

@login_required(login_url='signin')
def profile_update(request):
    if request.method == 'POST':
        try:
            # Code for updating profile, e.g., updating user details
            profile_image = request.FILES.get('image')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            gender = request.POST.get('gender')
            dob = request.POST.get('dob')
            age = request.POST.get('age')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            bio = request.POST.get('bio')
            location = request.POST.get('location')
            theme = request.POST.get('theme')

            # Validate unique email if it's being changed
            if User.objects.filter(email=email).exclude(username=request.user.username).exists():
                messages.error(request, 'This email is already associated with another account.')
                return redirect('profile_update')

            # Update the user's email and save
            user = request.user
            user.email = email
            user.save()

            # Update or create Profile with new data
            profile, created = Profile.objects.get_or_create(user=user)
            if profile_image:
                profile.profileimg = profile_image
            profile.first_name = first_name
            profile.last_name = last_name
            profile.gender = gender
            profile.dob = dob
            profile.age = age
            profile.phone = phone
            profile.bio = bio
            profile.location = location
            profile.theme = theme
            profile.save()

            # Success message
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('profile_update')
        
        except Exception as e:
            # Error message
            messages.error(request, 'An error occurred. Please try again.')
            print(e)  # Optional: Print the error to console for debugging
            return redirect('profile_update')
    
    return render(request, 'profile_update.html')
    
def signup(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email is Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username is Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                
                #log user in and direct to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request,user_login)
                
                
                #create a profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
        else:   
            messages.info(request, 'Password does not Match')
            return redirect('signup')
        
    else:
        return render(request,'signup.html')
    
def signin(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password)
    
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')
    
    else:
        return render(request, 'signin.html')
   
@login_required(login_url='signin') 
def logout(request):
    auth.logout(request)
    return redirect('signin')

def about(request):
    return render(request,'about.html')
    