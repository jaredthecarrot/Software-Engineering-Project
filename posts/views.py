from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Post, LikePost



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
    

def add_comment(request, post_id):
    
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)  # Get the post
        user = request.user
        comment_content = request.POST.get('comment')  # Get the comment content from the form
        
        if comment_content:  # Check if the comment is not empty
            # Create and save the comment
            PostComment.objects.create(post=post, user=user, content=comment_content)
        return redirect('/')  # Redirect to post detail page or main page
    
    else:
        return redirect('/')

    
