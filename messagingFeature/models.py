from django.db import models
from django.contrib.auth.models import User


class ChatChannel(models.Model):
    channel_name = models.CharField(max_length=255, unique=True)
    user0 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user0_chat_links")
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user1_chat_links")

    @staticmethod
    def get_or_create_channel(user_a, user_b):
        # Ensure the channel name is unique regardless of user order
        sorted_users = sorted([user_a.id, user_b.id])
        channel_name = f"chat_{sorted_users[0]}_{sorted_users[1]}"

        # Retrieve or create the chat channel
        channel, created = ChatChannel.objects.get_or_create(
            channel_name=channel_name,
            defaults={'user0': user_a, 'user1': user_b} if sorted_users[0] == user_a.id else {'user0': user_b, 'user1': user_a}
        )
        return channel


class ChatMessage(models.Model):
    chat_channel = models.ForeignKey(ChatChannel, related_name='chat_messages', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.author.username} : {self.body}'
    
    class Meta:
        ordering = ['-created']
    
    
    

