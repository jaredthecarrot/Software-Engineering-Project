from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.shortcuts import render, get_object_or_404

@login_required
def chat_view(request):
    chat_channel = get_object_or_404(ChatChannel, channel_name="angel-newUser")
    chat_messages = chat_channel.chat_messages.all()[:30]
    form = ChatmessageCreateForm()
    
    if request.method == 'POST':
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid:
            message= form.save(commit=False)
            message.author = request.user
            message.chat_channel = chat_channel 
            message.save()
            return redirect('chat_view')
    
    
    return render(request, 'chat_view.html', {'chat_messages' : chat_messages, 'form' : form})