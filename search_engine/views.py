from django.shortcuts import render
from .models import Item
# Create your views here.
def search(request):
    query = request.GET.get('q')
    if query:
        results = Item.objects.filter(name__icontains=query)
    else:
        results = Item.objects.none()
    return render(request, 'index.html', {'results': results})
