from django.shortcuts import render, redirect
from django.contrib.auth import authenticate as auth_authenticate, login as auth_login
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import UserProfile, User
from posts.models import Post, LikePost
from django.shortcuts import render, get_object_or_404
from .forms import RegistrationForm
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User #To be check
from django.contrib.auth import authenticate, login


# Create your views here.
@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = UserProfile.objects.get(user=user_object)
    
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
    # Check if a specific username is provided in the URL
    username = request.GET.get('username')
    
    if username:
        # Retrieve the user profile by the provided username
        user = get_object_or_404(User, username=username)
        user_profile = get_object_or_404(UserProfile, user=user)
    else:
        # Fallback to the logged-in user's profile
        user_profile = UserProfile.objects.get(user=request.user)
    
    return render(request, 'profile.html', {'user_profile': user_profile})
    
    


@login_required(login_url='signin')
def settings(request):
    user_profile = UserProfile.objects.get(user=request.user)
    
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
                user_login = authenticate(username=username, password=password)
                login(request,user_login)
                
                
            # Create a profile object for the new user
            user_model = User.objects.get(username=username)
            new_profile = UserProfile.objects.create(user=user_model)  # Associate user with profile
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
        
        user = authenticate(username=username, password=password)
    
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')
    
    else:
        return render(request, 'signin.html')

   
@login_required(login_url='signin') 
def logout(request):
    logout(request)
    return redirect('signin')

def about(request):
    return render(request,'about.html')

def select_account_type(request):
    if request.method == 'POST':
        account_type = request.POST.get('account_type')
        if account_type in ['regular', 'organization']:
            # Redirect to login with the selected account type
            return redirect(f'/login/?account_type={account_type}')
    return render(request, 'core/select_account_type.html')

def login_view(request):
    account_type = request.GET.get('account_type', 'regular')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth_authenticate(request, username=username, password=password)

        if user is not None:
            # Check if the user's account type matches the selected type
            user_profile = UserProfile.objects.get(user=user)
            if user_profile.account_type == account_type:
                auth_login(request, user)
                return redirect('home')  # Redirect to the home page after successful login
            else:
                messages.error(request, 'Invalid account type selected.')

        messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html', {'account_type': account_type})




'''
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            account_type = form.cleaned_data['account_type']

            user = User.objects.create_user(username=username, email=email, password=password)
            UserProfile.objects.create(user=user, account_type=account_type)

            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'core/register.html', {'form': form})
'''

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('password2')
        account_type = request.POST.get('account_type')
        organization_name = request.POST.get('organization_name') if account_type == 'organization' else None

        # Password validation
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        # Create the user
        user_model = User.objects.create_user(username=username, email=email, password=password)

        # Create or get the user profile
        new_profile, created = UserProfile.objects.get_or_create(
            user=user_model,
            defaults={'account_type': account_type}
        )

        # If it's an organization account, add the organization name
        if account_type == 'organization' and organization_name:
            new_profile.organization_name = organization_name
            new_profile.save()

        # Success message and redirect
        messages.success(request, 'Account created successfully!')
        return redirect('login')

    # Render the sign-up page for GET requests
    return render(request, 'core/signup.html')

def logout_view(request):
    auth_logout(request)
    return redirect('login')  # Ensure 'login' is the correct name for your login URL
