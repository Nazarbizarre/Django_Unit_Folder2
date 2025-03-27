from django.shortcuts import render, get_object_or_404

from .models import Product, Category

def index(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    
    category_name = request.GET.get("category")
    filter_name = request.GET.get("filter")
    product_name = request.GET.get("search")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    
    if category_name:
        products = products.filter(category=get_object_or_404(Category, name=category_name))
        
    if product_name:
        products = products.filter(name__icontains=product_name)
        
    if min_price:
        products = products.filter(price__gte=min_price)
        
    if max_price:
        products = products.filter(price__lte=max_price)
    
    match filter_name:
        case "price_increasing":
            products = products.order_by("price")
        case "price_decreasing":
            products = products.order_by("-price")
        case "rating":
            products = products.order_by("-rating")
            
    return render(request, 'index.html', context={"products":products, "categories":categories})

def about(request):
    return render(request, 'about.html')

def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "product_details.html", {"product": product})