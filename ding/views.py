from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render

def index(request):
    """
    Our main index view
    """
    return render(request, 'hauptanwendung/index.html', {'title': 'Anwendung Ding',
    })
