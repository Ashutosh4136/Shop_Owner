from .models import Cart, CartItem
from products.models import Product

SESSION_CART_KEY = 'cart_session'
def get_cart(request):
    cart = Cart.objects.filter(user=request.user).first()

    if not cart:
        cart = Cart.objects.create(user=request.user)

    return cart


def add_to_cart(request, product_id, quantity=1):
    product = Product.objects.get(id=product_id)
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        if cart_item.quantity > product.stock:
            cart_item.quantity = product.stock  # stock validation
        cart_item.save()
    else:
        session_cart = request.session.get(SESSION_CART_KEY, {})
        current_qty = session_cart.get(str(product_id), 0)
        new_qty = current_qty + quantity
        if new_qty > product.stock:
            new_qty = product.stock
        session_cart[str(product_id)] = new_qty
        request.session[SESSION_CART_KEY] = session_cart
