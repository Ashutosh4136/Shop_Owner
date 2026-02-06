from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test,login_required
from django.contrib.auth import get_user_model
from orders.models import Order,OrderItem
from products.models import Product
from django.db.models import Sum, Count
from django.utils.timezone import now
from datetime import timedelta
from django.contrib import messages


User = get_user_model()

def admin_required(view_func):
    return user_passes_test(lambda u: u.is_staff)(view_func)


@login_required(login_url='login')
def vendor_dashboard(request):
    if request.user.role != 'vendor':
        return redirect('home')

    return render(request, 'adminpanel/vendor_dashboard.html')


def vendor_products(request):
    products = Product.objects.filter(vendor=request.user)
    return render(request, 'adminpanel/manage_product.html', {
        'products': products
    })



@login_required
def edit_product(request, id):
    product = get_object_or_404(Product, id=id, vendor=request.user)

    if request.method == "POST":
        product.name = request.POST.get("name")
        product.price = request.POST.get("price")
        product.stock = request.POST.get("stock")
        product.save()
        return redirect("vendor_products")

    return render(request, "adminpanel/edit_product.html", {
        "product": product
    })

@login_required
def delete_product(request, id):
    product = get_object_or_404(Product, id=id, vendor=request.user)
    product.delete()
    return redirect("vendor_products")



@login_required
def vendor_orders(request):
    orders = OrderItem.objects.filter(
        product__vendor=request.user
    ).select_related("order", "product")

    return render(request, "adminpanel/vendor_order.html", {
        "orders": orders
    })




@login_required
def customer_dashboard(request):
    if request.user.role != 'customer':
        return redirect('home')

    return render(request, 'adminpanel/dashboard.html')

@admin_required
def dashboard_view(request):
    total_revenue = Order.objects.filter(status='DELIVERED').aggregate(total=Sum('total_price'))['total'] or 0
    total_orders = Order.objects.count()
    user_count = User.objects.count()
    product_count = Product.objects.count()

    # Sales analytics: monthly sales for last 6 months
    from django.db.models.functions import TruncMonth
    from django.db.models import DateTimeField

    six_months_ago = now() - timedelta(days=180)
    sales = (
        Order.objects.filter(created_at__gte=six_months_ago, status='DELIVERED')
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(monthly_total=Sum('total_price'))
        .order_by('month')
    )

    months = []
    totals = []
    for sale in sales:
        months.append(sale['month'].strftime('%b %Y'))
        totals.append(float(sale['monthly_total']))

    # Stock alerts (products with stock < 10)
    low_stock_products = Product.objects.filter(stock__lt=10, is_active=True)

    context = {
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'user_count': user_count,
        'product_count': product_count,
        'months': months,
        'totals': totals,
        'low_stock_products': low_stock_products,
    }
    return render(request, 'adminpanel/dashboard.html', context)


@admin_required
def order_list_view(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'adminpanel/order_list.html', {'orders': orders})


@admin_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES).keys():
            order.status = new_status
            order.save()
            messages.success(request, f"Order #{order.id} status updated to {new_status}.")
        else:
            messages.error(request, "Invalid status.")
        return redirect('admin_order_list')
    return render(request, 'adminpanel/update_order_status.html', {'order': order, 'status_choices': Order.STATUS_CHOICES})
