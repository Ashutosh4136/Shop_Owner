from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import Review
from .forms import ReviewForm
from django.contrib import messages

@login_required
def add_review(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    existing_review = Review.objects.filter(user=request.user, product=product).first()

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=existing_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            messages.success(request, 'Your review has been submitted.')
            return redirect('product_detail', slug=product.slug)
    else:
        form = ReviewForm(instance=existing_review)

    return render(request, 'reviews/add_review.html', {'form': form, 'product': product})
