from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Banner, StaticPage
from categories.models import Category
from products.models import Product

def home(request):
    categories = Category.objects.all()

    category_products = []
    for category in categories:
        products = Product.objects.filter(category=category)[:4]
        category_products.append({
            'category': category,
            'products': products
        })

    context = {
        'category_products': category_products
    }
    return render(request, 'home/home.html', context)



def about_view(request):
    return render(request, 'home/about.html')


def contact_view(request):
    return render(request, 'home/contact.html')


def page_view(request, slug):
    page = get_object_or_404(StaticPage, slug=slug, is_active=True)
    return render(request, 'home/page.html', {'page': page})
