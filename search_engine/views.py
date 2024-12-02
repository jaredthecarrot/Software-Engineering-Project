from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

def search(request):
    query = request.GET.get('q')
    if query:
        results = User.objects.filter(username__icontains=query)
    else:
        results = User.objects.none()
    return render(request, 'index.html', {'results': results, 'query': query})

def profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'profile.html', {'user': user})
