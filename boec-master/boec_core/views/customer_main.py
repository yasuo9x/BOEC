from .views import *
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import AnonymousUser
import code; 

class CustomerIndexView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        user = request.user
        featured_products = ProductVariant.objects.filter(is_selling=True, is_feature=True)[:6]
        electronic_category = Category.objects.get(pk=1)
        electronic_subcategories = SubCategory.objects.filter(parent=electronic_category)
        for subcategory in electronic_subcategories:
            products = ProductVariant.objects.distinct().filter(is_selling=True,product__sub_category__id=subcategory.id)
            setattr(subcategory, "products", products)

        clothing_category = Category.objects.get(pk=3)
        clothing_subcategories = SubCategory.objects.filter(parent=clothing_category)
        for subcategory in clothing_subcategories:
            products = ProductVariant.objects.distinct().filter(is_selling=True,product__sub_category__id=subcategory.id)
            setattr(subcategory, "products", products)

        book_category = Category.objects.get(pk=2)
        book_subcategories = SubCategory.objects.filter(parent=book_category)
        for subcategory in book_subcategories:
            products = ProductVariant.objects.distinct().filter(is_selling=True,product__sub_category__id=subcategory.id)
            setattr(subcategory, "products", products)

        if 'cart' not in request.session:
            cart = []
        else:
            cart = request.session['cart']
        if user.is_authenticated:
            context["user_id"] = user
            context["favorite"] = Favorite.objects.filter(customer=user).count()
        context["featured_products"] = featured_products
        context["electronic_subcategories"] = electronic_subcategories
        context["clothing_subcategories"] = clothing_subcategories
        context["book_subcategories"] = book_subcategories

        context["cart"] = len(cart)
        return render(request, "boec_core/customer/index.html",context)

class CartView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        user = request.user
        context["user"] = user
        cart = {}
        cart_items = []
        total = 0
        if 'cart' not in request.session:
            cart = {}
        else:
            cart = request.session['cart']
        for item in cart:
            variant = ProductVariant.objects.get(pk=item)
            quantity = cart[item]
            amount = quantity * variant.price
            setattr(variant, 'quantity', quantity)
            setattr(variant, 'total', amount)
            total += amount
            cart_items.append(variant)
        context["cart"] = len(cart)
        context["cart_items"] = cart_items
        context["total"] = total

        return render(request, "boec_core/customer/shoping-cart.html",context)

class FavoriteView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        user = request.user
        favorites = Favorite.objects.filter(customer=user)
        featured_products = []
        for favorite in favorites:
            featured_products.append(favorite.product)
        
        if 'cart' not in request.session:
            cart = []
        else:
            cart = request.session['cart']
        if user.is_authenticated:
            context["user_id"] = user
            context["favorite"] = Favorite.objects.filter(customer=user).count()
        context["featured_products"] = featured_products
        context["cart"] = len(cart)
        return render(request, "boec_core/customer/favorite.html",context)

class ShopGridView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        user = request.user
        search = request.GET.get("search")
        if search is None:
            selling_products = ProductVariant.objects.filter(is_selling=True)
        else:
            selling_products = ProductVariant.objects.distinct().filter(is_selling=True, product__name__icontains=search)

        if 'cart' not in request.session:
            cart = []
        else:
            cart = request.session['cart']
        if user.is_authenticated:
            favorites = Favorite.objects.filter(customer=user)
            context["user_id"] = user
            context["favorite"] = Favorite.objects.filter(customer=user).count()
        context["selling_products"] = selling_products
        context["cart"] = len(cart)
        page_size = settings.PAGE_SIZE
        page_num = request.GET.get("page_num")
        p = Paginator(selling_products, page_size)
        cur_page = p.page(1)
        if page_num is not None:
            cur_page = p.page(page_num)
        
        context["num_pages"] = p.num_pages
        context["pages"] = range(1, p.num_pages+1)
        return render(request, "boec_core/customer/shop-grid.html",context)
class VariantDetailView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        user = request.user
        variant_id = kwargs.get('variant_id')
        variant = ProductVariant.objects.get(pk=variant_id)
        reviews = CustomerReview.objects.filter(product=variant)
        recommend_products = ProductVariant.objects.filter(is_selling=True, is_feature=True)[:6]
        if 'cart' not in request.session:
            cart = []
        else:
            cart = request.session['cart']
        if user.is_authenticated:
            context["user_id"] = user
            context["favorite"] = Favorite.objects.filter(customer=user).count()
        rating = 0
        for review in reviews:
            rating += review.rating
            replies = Reply.objects.filter(review=review)
            setattr(review, "replies", replies)
        
        if reviews.count() == 0:
            rating = 0
            context["is_float"] = False
        else:
            rating = rating/reviews.count()
            if(rating%1!=0):
                context["is_float"] = True
        context["cart"] = len(cart)
        context["variant"] = variant
        context["reviews"] = reviews
        context["ratings"] = int(rating)
        context["max_rating"] = [1,2,3,4,5]
        context["current_rating"] = [1] * int(rating)
        return render(request, "boec_core/customer/shop-details.html",context)


class CheckoutView(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        cart = {}
        cart_items = []
        total = 0
        name = request.POST.get("name")
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        city = request.POST.get("city")
        note = request.POST.get("note")
        if user.is_authenticated:
            order = Order(recv_name=name,recv_city=city,recv_phone=phone,
            recv_email=email,note=note,customer=user,payment_type="COD",shipping_address=address)
        else:
            order = Order(recv_name=name,recv_city=city,recv_phone=phone,
            recv_email=email,note=note,payment_type="COD",shipping_address=address)

        order.save()
        if 'cart' not in request.session:
            cart = {}
        else:
            cart = request.session['cart']
        for item in cart:
            variant = ProductVariant.objects.get(pk=item)
            quantity = cart[item]
            amount = quantity * variant.price
            ordered_product = OrderedProduct(quantity=quantity, price=variant.price,
             order=order, product=variant)
            variant.quantity -= quantity
            variant.save()
            ordered_product.save()
        del request.session['cart']
        order.amount = total
        order.save()
        return HttpResponseRedirect("/boec/customer")

    def get(self, request, *args, **kwargs):
        context = {}
        user = request.user
        context["user"] = user
        cart = {}
        cart_items = []
        total = 0
        if 'cart' not in request.session:
            cart = {}
        else:
            cart = request.session['cart']
        for item in cart:
            variant = ProductVariant.objects.get(pk=item)
            quantity = cart[item]
            amount = quantity * variant.price
            setattr(variant, 'quantity', quantity)
            setattr(variant, 'total', amount)
            total += amount
            cart_items.append(variant)
        context["cart"] = len(cart)
        context["cart_items"] = cart_items
        context["total"] = total

        return render(request, "boec_core/customer/checkout.html",context)
