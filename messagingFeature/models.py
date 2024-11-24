from django.db import models
from django.contrib.auth.models import User

class ChatChannel(models.Model):
    channel_name = models.CharField(max_length=255)
    user0 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user0_chat_links")
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user1_chat_links")


class ChatMessage(models.Model):
    chat_channel = models.ForeignKey(ChatChannel, related_name='chat_messages', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.author.username} : {self.body}'
    
    class Meta:
        ordering = ['-created']
    
    
    

