from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('user/login', views.LoginView.as_view(template_name="boec_core/user_base/login.html"), name="login"),
    path('user/logout', auth_views.LogoutView.as_view(next_page='/user/login'), name='logout'),
    # path('boec/admin', views.AdminIndexView.as_view(), name="login"),
    path('boec/customer', views.CustomerIndexView.as_view(), name="main_customer"),
    path('boec/shopping-cart', views.CartView.as_view(), name="cart_view"),
    path('boec/checkout', views.CheckoutView.as_view(), name="checkout"),
    path('boec/favourite', views.FavoriteView.as_view(), name="favorite"),
    path('boec/variant/<int:variant_id>', views.VariantDetailView.as_view(), name="variant_detail"),
    path('api/cart/add_product_to_cart', views.add_product_to_cart, name='add_product_to_cart'),
    path('api/favorite/add_product_to_favorite', views.add_product_to_favorite, name='add_product_to_favorite'),
    path('api/review/add_review', views.add_review, name='add_review'),
    path('api/review/add_reply', views.add_reply, name='add_reply'),
    path('boec/shop-grid', views.ShopGridView.as_view(), name="shop_grid"),
    path('api/cart/update_cart', views.update_cart, name='update_cart'),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    
    path('edit_profile/',views.edit_profile,name = 'edit_profile'),
    path('signup/',views.signup,name = "signup"),
    path('', views.CustomerIndexView.as_view(), name='index')
]