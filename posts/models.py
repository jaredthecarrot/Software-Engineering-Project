from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

User = get_user_model()

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to User model
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)
    
    # This will automatically provide a list of related comments
    @property
    def comments(self):
        return PostComment.objects.filter(post=self)
    
    def __str__(self):
        return self.user.username  # Use username from User model 

class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return self.user.username


class PostComment(models.Model):
    post= models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)  # Link to Post model
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to User model
    content = models.TextField()  # The comment text
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.id} : {self.post.user} post. "