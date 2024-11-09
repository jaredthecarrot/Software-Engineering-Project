from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import ChatChannel, ChatMessage
from .forms import ChatmessageCreateForm

@login_required
def chat_view(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    
    # Get or create a chat channel between the current user and the target user
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
            return redirect('chat_view', user_id=user_id)
    
    return render(request, 'chat_view.html', {'chat_messages': chat_messages, 'form': form, 'target_user': target_user})