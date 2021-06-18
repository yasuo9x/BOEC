from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Vendor)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductVariant)
admin.site.register(OrderedProduct)
admin.site.register(Order)
admin.site.register(CustomerReview)
admin.site.register(SubCategory)
admin.site.register(OrderShip)
admin.site.register(ShippingDepartment)
admin.site.register(OrderStatus)