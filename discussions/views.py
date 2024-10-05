from django.shortcuts import render, redirect, get_object_or_404
from .models import Thread, Comment
from .forms import ThreadForm, CommentForm
from django.contrib.auth.decorators import login_required

def thread_list(request):
    threads = Thread.objects.all().order_by('-created_at')
    return render(request, 'discussions/thread_list.html', {'threads': threads})

@login_required
def create_thread(request):
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.user = request.user
            thread.save()
            return redirect('thread_list')
    else:
        form = ThreadForm()
    return render(request, 'discussions/create_thread.html', {'form': form})

@login_required
def thread_detail(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    comments = thread.comments.all()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.thread = thread
            comment.save()
            return redirect('thread_detail', pk=thread.pk)
    else:
        comment_form = CommentForm()
    
    return render(request, 'discussions/thread_detail.html', {'thread': thread, 'comments': comments, 'comment_form': comment_form})

