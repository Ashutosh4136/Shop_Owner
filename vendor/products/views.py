from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404,redirect
from .models import Product,ProductImage
from categories.models import Category
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

def product_list(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.filter(is_active=True, parent=None)

    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    images = product.images.all()
    print(product.slug)
    return render(request, 'products/product_detail.html', {
        'product': product,
        'images': images
    })

def product_search(request):
    query = request.GET.get('q')
    products = Product.objects.filter(name__icontains=query) if query else []
    return render(request, 'products/search_result.html', {
        'products': products,
        'query': query
    })





@login_required
def add_product(request):
    #Customers blocked
    if request.user.role != 'vendor' :
        return HttpResponseForbidden("Only vendors can add products")
    categories = Category.objects.filter(is_active=True,parent__isnull=False)

#     
    if request.method == 'POST':
        category_id = request.POST.get('category')
        category = Category.objects.get(id=category_id)

        product = Product.objects.create(
            vendor=request.user,
            name=request.POST.get('name'),
            category=category,
            price=request.POST.get('price'),
            stock=request.POST.get('stock'),
            description=request.POST.get('description'),
        )

        image = request.FILES.get('image')
        if image:
            ProductImage.objects.create(
                product=product,
                image=image,
                is_primary=True
            )

        return redirect('vendor_products')

    return render(request, 'products/add_product.html', {'categories': categories})
