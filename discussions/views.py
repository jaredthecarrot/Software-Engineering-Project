from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Thread, Reply
from .forms import ThreadForm, ReplyForm

@login_required
def discussions_view(request):
    threads = Thread.objects.all().order_by('-created_at')  # Fetch all threads, ordered by creation date
    thread_form = ThreadForm()  # Initialize form for creating threads

    if request.method == 'POST':
        if 'reply_thread_id' in request.POST:
            # Handle reply to a thread
            thread_id = request.POST['reply_thread_id']
            reply_form = ReplyForm(request.POST)
            if reply_form.is_valid():
                reply = reply_form.save(commit=False)
                reply.thread = get_object_or_404(Thread, id=thread_id)  # Link the reply to the correct thread
                reply.author = request.user  # Set the author of the reply to the current user
                reply.save()  # Save the reply instance
                return redirect('discussions_view')  # Redirect after successfully creating a reply
        else:
            # Handle creating a new thread
            thread_form = ThreadForm(request.POST)
            if thread_form.is_valid():
                thread = thread_form.save(commit=False)
                thread.author = request.user  # Set the author of the thread to the current user
                thread.save()  # Save the thread instance
                return redirect('discussions_view')  # Redirect after successfully creating a thread

    else:
        reply_form = ReplyForm()  # Initialize reply form for GET requests

    # Render the template with threads, thread form, and reply form
    return render(request, 'discussions.html', {
        'threads': threads,
        'thread_form': thread_form,
        'reply_form': ReplyForm(),  # Initialize a new reply form for use in the template
    })

