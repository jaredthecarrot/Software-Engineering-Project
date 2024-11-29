from django.shortcuts import render
from django.contrib.auth.models import User

def search(request):
    query = request.GET.get('q')
    if query:
        results = User.objects.filter(username__icontains=query)
    else:
        results = User.objects.none()
    return render(request, 'index.html', {'results': results, 'query': query})
