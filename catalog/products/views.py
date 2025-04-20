from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import F, ExpressionWrapper, FloatField
from django.conf import settings

from .models import Product, Category, Cart, CartItem

def index(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    
    category_name = request.GET.get("category")
    filter_name = request.GET.get("filter")
    product_name = request.GET.get("search")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    
    product_amount = Product.objects.all().count()
    
    if category_name:
        products = products.filter(category=get_object_or_404(Category, name=category_name))
        product_amount = products.count()
        
    if product_name:
        products = products.filter(name__icontains=product_name)
        product_amount = products.count()
        
    if min_price:
        products = products.annotate(
        discount_price=ExpressionWrapper(
            F("price") * F("discount") / 100,
            output_field=FloatField(),
        )
    ).filter(discount_price__gte=min_price)
    product_amount = products.count()
        
    if max_price:
        products = products.annotate(
        discount_price=ExpressionWrapper(
            F("price") * F("discount") / 100,
            output_field=FloatField(),
        )
    ).filter(discount_price__lte=max_price)
    product_amount = products.count()
    
    match filter_name:
        case "price_increasing":
            products = products.order_by("price")
        case "price_decreasing":
            products = products.order_by("-price")
        case "rating":
            products = products.order_by("-rating")
        case "newest_first":
            products = products.order_by('-created_at')
        case "oldest_first":
            products = products.order_by('created_at')
            
    return render(request, 'index.html', context={"products":products, "categories":categories, "product_amount":product_amount})

def about(request):
    return render(request, 'about.html')

def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "product_details.html", {"product": product})

def cart_detail(request):
    if not request.user.is_authenticated:
        cart = request.session.get(settings.CART_SESSION_ID, dict())
        product_ids = cart.keys()
        products = Product.objects.filter(id__in = product_ids)
        cart_items = []
        total_price = 0
        for product in products:
            count = cart[str(product.id)]
            if count == 0:
                continue
            if product.discount:
                raw_price = round(((product.price * product.discount) / 100), 2)
            else:
                raw_price = product.price
            price = count * raw_price
            total_price += price
            cart_items.append({"product" : product, "count" : count, "price": price})

    # else:
    #     try:
    #         cart = request.user.cart
    #     except Cart.DoesNotExist:
    #         cart = None
    #     if not cart or not cart.items.count():
    #         cart_items = []
    #         total_price = 0
    #     else:
    #         cart_items = cart.items.select_related("product").all()
    #         total_price = sum(item.product.price * item.amount  if not item.product.discount else round(((item.product.price * item.product.discount) / 100), 2) for item in cart_items)
    else:
        try:
            cart = request.user.cart
        except Cart.DoesNotExist:
            cart = None

        if not cart or not cart.items.count():
            cart_items = []
            total_price = 0
        else:
            raw_items = cart.items.select_related("product").all()
            cart_items = []
            total_price = 0
            for item in raw_items:
                product = item.product
                count = item.amount
                if count == 0:
                    continue
                if product.discount:
                    raw_price = round(((product.price * product.discount) / 100), 2)
                else:
                    raw_price = product.price
                price = count * raw_price
                total_price += price
                cart_items.append({"product": product, "count": count, "price": price})
    return render(request, "cart_detail.html", context={"cart_items": cart_items, "total_price" : round(total_price,2)})

def cart_add(request, product_id:int):
    product = get_object_or_404(Product, id=product_id)
    if not request.user.is_authenticated:
        cart = request.session.get(settings.CART_SESSION_ID, {})
        product_key = str(product_id)
        if cart.get(product_key):
            cart[product_key] += 1
        else:
            cart[product_key] = 1
        request.session[settings.CART_SESSION_ID] = cart
    else:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.amount += 1
            cart_item.save()
    return redirect('products:cart_detail')
    

def cart_delete(request, product_id:int):
    product = get_object_or_404(Product, id=product_id)
    product_key = str(product_id)
    if not request.user.is_authenticated:
        cart = request.session.get(settings.CART_SESSION_ID, {})
        cart[product_key] -= 1
        request.session[settings.CART_SESSION_ID] = cart
    else:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.amount -= 1
            cart_item.save()
    return redirect("products:cart_detail")


