from django.urls import path
from . import views

urlpatterns = [
    path('boec/admin/',views.index, name='common'),
    path('boec/admin/oders/',views.oders, name='list_order'),
    path('boec_admin/edit_status/<int:order_id>',views.changeStatusOrder, name='changeStatus'),
    path('boec/admin/oders/detail/<int:order_id>',views.detailOrder, name='detail_order'),
    path('boec_admin/productlist/',views.productlist, name="productlist"),
    path('boec_admin/add_category/',views.addCategory, name="addCategory"),
    path('boec_admin/add_subCategory/',views.addSubCategory, name="addSubCategory"),
    path('boec_admin/add_vendor/',views.addVendor, name="addVendor"),
    path('boec_admin/add_product/',views.addProduct, name="addProduct"),
    path('boec_admin/add_productvariant/',views.addProductVariant, name="productVariant"),
    path('boec_admin/edit_product/<int:product_id>',views.editProduct, name="editProduct"),
    path('boec_admin/delete_product/<int:product_id>',views.deleteProduct, name="deleteProduct"),
    path('boec_admin/search_product/',views.productSearch, name="productSearch")
    
]

