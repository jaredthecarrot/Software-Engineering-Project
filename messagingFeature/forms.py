from django.forms import ModelForm
from django import forms
from .models import ChatMessage

class ChatmessageCreateForm(ModelForm):
    class Meta:
        model = ChatMessage 
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'placeholder': 'Type your message...',
                'class': 'chat-textarea',  # Custom class for styling
                'rows': 1,  # Set to 1 row initially
                'style': 'resize:none; width: 100%; height: 35px; padding: 8px; font-size: 14px; border: 1px solid maroon; border-radius: 10px;',
            }),
        }