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


# Create your views here.
@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    
    # Fetch all posts with related user data
    posts = Post.objects.all().select_related('user')
    
    #makea list of all profiles 
    all_profiles = Profile.objects.exclude(user=request.user)
    
    # Add likes and the profiles of users who liked each post
    for post in posts:
         # Check if the current user has liked the post
        post.liked_by_user = LikePost.objects.filter(post_id=post.id, user=request.user).exists()
        
        # Add a list of users who liked this post (limit to last 3)
        post.liked_users = LikePost.objects.filter(post_id=post.id).select_related('user')[:3]
    
    # Get the list of friends
    friends = user_profile.friends.all()
    
    return render(request,'index.html', {'user_profile': user_profile, 'posts':posts, 'friends':friends, 'profiles':all_profiles})


@login_required(login_url='signin')
def profile(request):
    
    main_user = request.user
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
        'profile_user_id': target_user.id,
        'main_user':main_user,

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
    
    return render(request,'setting.html', {'user_profile': user_profile})

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

@login_required(login_url='signin')
def send_friend_request(request, target_user_id):
    try:
        target_user = User.objects.get(id=target_user_id)
        target_username = target_user.username
        # Logic to handle the friend request goes here
        # Get the profiles of the current user and the target user
        current_user_profile = get_object_or_404(Profile, user=request.user)
        target_user_profile = get_object_or_404(Profile, user__id=target_user_id)
        
        # Add the target user to the current user's friends list
        current_user_profile.friends.add(target_user_profile)
                
        
        return redirect(f"/profile?username={target_username}")
    except User.DoesNotExist:
        # Handle the case where the target user does not exist
        return redirect('/')
    
@login_required(login_url='signin')
def toggle_friend(request, target_user_id):
    target_user_profile = get_object_or_404(Profile, user__id=target_user_id)
    main_user_profile = get_object_or_404(Profile, user=request.user)

    # Check if the target user is already a friend
    if target_user_profile in main_user_profile.friends.all():
        # If they are friends, remove the friendship
        main_user_profile.friends.remove(target_user_profile)
    else:
        # Otherwise, add the friendship
        main_user_profile.friends.add(target_user_profile)

    # Redirect back to the target user's profile
    return redirect(f"/profile?username={target_user_profile.user.username}")

def users_to_follow(request):
    # Exclude the logged-in user from the list (if applicable)
    all_profiles = Profile.objects.exclude(user=request.user)
    return render(request, 'users_to_follow.html', {'profiles': all_profiles})