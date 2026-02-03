from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect, render, get_object_or_404
from products.models import Product
from .models import CartItem
from .utils import add_to_cart, get_cart, SESSION_CART_KEY

def add_to_cart_view(request, product_id):
    quantity = int(request.GET.get('qty', 1))
    add_to_cart(request, product_id, quantity)
    return redirect('cart_detail')


def cart_detail_view(request):
    if request.user.is_authenticated:
        cart = get_cart(request)
        items = cart.items.select_related('product').all()
        total = cart.total_price()
    else:
        session_cart = request.session.get(SESSION_CART_KEY, {})
        product_ids = session_cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        items = []
        total = 0
        for product in products:
            qty = session_cart.get(str(product.id), 0)
            item_total = qty * product.get_price()
            total += item_total
            items.append({
                'product': product,
                'quantity': qty,
                'total_price': item_total,
            })

    return render(request, 'cart/cart_detail.html', {
        'items': items,
        'total': total,
    })


def remove_from_cart_view(request, product_id):
    if request.user.is_authenticated:
        cart = get_cart(request)
        cart_item = cart.items.filter(product_id=product_id).first()
        if cart_item:
            cart_item.delete()
    else:
        session_cart = request.session.get(SESSION_CART_KEY, {})
        session_cart.pop(str(product_id), None)
        request.session[SESSION_CART_KEY] = session_cart
    return redirect('cart_detail')
