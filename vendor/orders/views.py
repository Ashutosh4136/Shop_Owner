from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.utils import get_cart
from .models import Order, OrderItem
from accounts.models import Address
from products.models import Product
from django.contrib import messages
from cart.models import Cart,CartItem


@login_required
def checkout_view(request):
    cart_obj = Cart.objects.filter(user=request.user).first()

    if not cart_obj:
        return redirect('cart_detail')

    cart = CartItem.objects.filter(cart=cart_obj)

    if cart.count() == 0:
        return redirect('cart_detail')

    # total price helper (for template + view)
    cart.get_total_price = lambda: sum(item.total_price() for item in cart)

    addresses = Address.objects.filter(user=request.user)

    if request.method == 'POST':
        address = None  # ✅ VERY IMPORTANT
        address_id = request.POST.get('address')

        # 1️⃣ Existing address selected
        if address_id:
            address = get_object_or_404(Address, id=address_id, user=request.user)

        # 2️⃣ New address
        else:
            full_name = request.POST.get('full_name')
            phone = request.POST.get('phone')
            address_line = request.POST.get('address_text')
            city = request.POST.get('city')
            state = request.POST.get('state')
            pincode = request.POST.get('pincode')

            if all([full_name, phone, address_line, city, state, pincode]):
                address = Address.objects.create(
                    user=request.user,
                    full_name=full_name,
                    phone=phone,
                    address_line=address_line,
                    city=city,
                    state=state,
                    pincode=pincode,
                )

        # 🔒 FINAL SAFETY CHECK
        if address is None:
            return redirect('checkout')

        # 3️⃣ Create Order
        order = Order.objects.create(
            user=request.user,
            address=address,
            total_price=cart.get_total_price(),
            status='PENDING'
        )

        # 4️⃣ Create Order Items + reduce stock
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity
            )

            item.product.stock -= item.quantity
            item.product.save()

        # 5️⃣ Clear cart
        cart_obj.items.all().delete()

        return redirect('order_success')

    return render(request, 'orders/checkout.html', {
        'cart': cart,
        'addresses': addresses
    })


@login_required
def order_success(request):
    return render(request, 'orders/order_success.html')


@login_required
def order_list_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})
