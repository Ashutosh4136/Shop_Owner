from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.utils import get_cart
from .models import Order, OrderItem
from accounts.models import Address
from products.models import Product
from django.contrib import messages

@login_required
def checkout_view(request):
    cart = get_cart(request)
    if not cart.items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('cart_detail')

    addresses = request.user.addresses.all()
    if request.method == 'POST':
        address_id = request.POST.get('address')
        address = get_object_or_404(Address, id=address_id, user=request.user)

        # Calculate total price
        total = cart.total_price()

        # Create order
        order = Order.objects.create(
            user=request.user,
            address=address,
            total_price=total
        )

        # Create order items
        for item in cart.items.all():
            if item.quantity > item.product.stock:
                messages.error(request, f"Insufficient stock for {item.product.name}")
                order.delete()
                return redirect('cart_detail')

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.get_price()
            )

            # Deduct stock
            item.product.stock -= item.quantity
            item.product.save()

        # Clear cart
        cart.items.all().delete()

        messages.success(request, f"Order #{order.id} placed successfully!")
        return redirect('order_detail', order_id=order.id)

    return render(request, 'orders/checkout.html', {'addresses': addresses, 'cart': cart})


@login_required
def order_list_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})
