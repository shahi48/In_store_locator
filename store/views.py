from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from .models import Category, Product, ShoppingList, Review, Order, OrderItem
from .forms import ProductSearchForm
from django.core.paginator import Paginator

def home(request):
    form = ProductSearchForm(request.GET)
    products = []
    
    if form.is_valid() and (form.cleaned_data.get('query') or form.cleaned_data.get('category')):
        query = form.cleaned_data.get('query', '')
        category = form.cleaned_data.get('category')
        
        # Build the query
        products = Product.objects.all()
        
        if query:
            products = products.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(aisle__icontains=query)
            )
        
        if category:
            products = products.filter(category=category)
            
        # Pagination for search results
        paginator = Paginator(products, 12)  # Show 12 products per page
        page = request.GET.get('page')
        products = paginator.get_page(page)
    
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    total_aisles = len(set(Product.objects.values_list('aisle', flat=True)))
    
    context = {
        'form': form,
        'products': products,
        'total_products': total_products,
        'total_categories': total_categories,
        'total_aisles': total_aisles,
    }
    return render(request, 'store/home.html', context)

def categories(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'store/categories.html', context)

def category_products(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category).order_by('name')
    
    # Get user's shopping list items if logged in
    if request.user.is_authenticated:
        shopping_list_items = ShoppingList.objects.filter(user=request.user).values_list('product_id', flat=True)
    else:
        shopping_list_items = []
    
    # Pagination
    paginator = Paginator(products, 12)  # Show 12 products per page
    page = request.GET.get('page')
    products = paginator.get_page(page)
    
    context = {
        'category': category,
        'products': products,
        'shopping_list_items': list(shopping_list_items)
    }
    return render(request, 'store/category_products.html', context)

@login_required
def add_to_list(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        shopping_list_item, created = ShoppingList.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': 1}
        )
        
        message = 'Added to shopping list' if created else 'Already in shopping list'
        return JsonResponse({'status': 'success', 'message': message})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

@login_required
def remove_from_list(request, product_id):
    if request.method == 'POST':
        ShoppingList.objects.filter(user=request.user, product_id=product_id).delete()
        return JsonResponse({'status': 'success', 'message': 'Removed from shopping list'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

def get_product_location(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return JsonResponse({
        'product_name': product.name,
        'aisle': product.aisle,
        'shelf': product.shelf,
    })

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    order = Order.objects.filter(
        user=request.user,
        orderitem__product=product
    ).last()
    
    if not order:
        messages.error(request, 'You need to purchase this product before reviewing it.')
        return redirect('home')
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        if rating and comment:
            # Check if user has already reviewed this product
            existing_review = Review.objects.filter(
                user=request.user,
                product=product
            ).first()
            
            if existing_review:
                # Update existing review
                existing_review.rating = rating
                existing_review.comment = comment
                existing_review.save()
                messages.success(request, 'Your review has been updated!')
            else:
                # Create new review
                Review.objects.create(
                    user=request.user,
                    product=product,
                    rating=rating,
                    comment=comment
                )
                messages.success(request, 'Thank you for your review!')
            
            # Redirect to product detail page instead of order confirmation
            return redirect('product_detail', product_id=product_id)
    
    # Check if user has already reviewed this product
    existing_review = Review.objects.filter(
        user=request.user,
        product=product
    ).first()
    
    context = {
        'product': product,
        'order': order,
        'existing_review': existing_review
    }
    return render(request, 'store/add_review.html', context)

@login_required
def shopping_list(request):
    items = ShoppingList.objects.filter(user=request.user).select_related('product')
    total = sum(item.product.price * item.quantity for item in items)
    
    context = {
        'items': items,
        'total': total,
    }
    return render(request, 'store/shopping_list.html', context)

@login_required
def update_quantity(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(ShoppingList, id=item_id, user=request.user)
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0 and quantity <= item.product.stock:
            item.quantity = quantity
            item.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def checkout(request):
    if request.method == 'POST':
        items = ShoppingList.objects.filter(user=request.user).select_related('product')
        if not items:
            messages.error(request, 'Your shopping list is empty!')
            return redirect('shopping_list')

        total_amount = sum(item.product.price * item.quantity for item in items)
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            total_amount=total_amount,
            status='processing'
        )

        # Create order items and update stock
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            
            # Update product stock
            product = item.product
            product.stock -= item.quantity
            product.save()

        # Clear shopping list
        items.delete()

        messages.success(request, 'Order placed successfully!')
        return redirect('order_confirmation', order_id=order.id)

    return redirect('shopping_list')

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = order.orderitem_set.all()
    
    context = {
        'order': order,
        'items': items,
    }
    return render(request, 'store/order_confirmation.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product).order_by('-created_at')
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    in_list = False
    if request.user.is_authenticated:
        in_list = ShoppingList.objects.filter(user=request.user, product=product).exists()
    
    context = {
        'product': product,
        'reviews': reviews,
        'average_rating': average_rating,
        'in_list': in_list,
    }
    return render(request, 'store/product_detail.html', context)
