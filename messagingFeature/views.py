from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import ChatChannel, ChatMessage
from .forms import ChatmessageCreateForm

@login_required
def chat_view(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
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

            # Return JSON response for AJAX requests
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': message.body})
            
            # Fallback to redirect for non-AJAX POST requests
            return redirect('chat_view', user_id=user_id)

    # Handle AJAX GET requests for chat messages
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        messages_data = [
            {
                "author": message.author.id,
                "body": message.body,
                "created": message.created.strftime("%Y-%m-%d %H:%M:%S")
            }
            for message in chat_messages
        ]
        return JsonResponse({
            "chat_messages": messages_data,
            "current_user": request.user.id
        })

    return render(request, 'profile.html', {
        'chat_messages': chat_messages,
        'form': form,
        'target_user': target_user,
        'profile_user_id': target_user.id
    })