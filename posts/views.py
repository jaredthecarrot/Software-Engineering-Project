from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Post, LikePost
from django.shortcuts import redirect



@login_required(login_url='signin')
def upload(request):
    
    if request.method == "POST":
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']
        
        # Assign the User instance (request.user) instead of request.user.username
        new_post = Post(user=request.user, image=image, caption=caption)
        new_post.save()

        return redirect('/')
        
    else:
        return redirect('/')

@login_required(login_url='signin') 
def like_post(request):
    user = request.user
    username = request.user.username
    post_id = request.GET.get('post_id')
    
    post = Post.objects.get(id=post_id)
    
    like_filter = LikePost.objects.filter(post_id=post_id, user=user).first()
    
    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, user=user)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect('/')
    
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect('/')
