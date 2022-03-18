from django.shortcuts import render
from django.contrib.auth.models import User
from django.views import View
from .forms import SearchBar
# Create your views here.

def loginView(request):
    pass
    return render(request, 'login.html', {'form': form})

def NewsPage(request):
    
    if request.method == 'POST':
        form = SearchBar(request.POST)
        if form.is_valid():
            keyword = form.cleaned_data["keyword"]
            print("AAAAAAAAAAAAAAA")
            print(keyword)
    else:
        form = SearchBar()
    
    return render(request, 'newspage.html', {'form': form})