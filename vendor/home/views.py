from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Banner, StaticPage

def home_view(request):
    banners = Banner.objects.filter(is_active=True)
    return render(request, 'home/home.html', {'banners': banners})


def about_view(request):
    return render(request, 'home/about.html')


def contact_view(request):
    return render(request, 'home/contact.html')


def page_view(request, slug):
    page = get_object_or_404(StaticPage, slug=slug, is_active=True)
    return render(request, 'home/page.html', {'page': page})
