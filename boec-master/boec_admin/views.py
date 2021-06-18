from django.shortcuts import redirect, render
from django.http import HttpResponse
from boec_core.models import *

# Create your views here.
def index(request):
    return render(request,"common/index.html")

def oders(request):
    list_Order = Order.objects.all()
    
    return render(request, "common/oders.html", {"oders":list_Order} )

def detailOrder(request,order_id):
    order = Order.objects.filter(id = order_id)
    products = OrderedProduct.objects.filter(order = order_id)
    return render(request, 'common/detail_order.html',{'products':products, 'order':order})

def productlist(request):
    productVars = ProductVariant.objects.all()
    products = Product.objects.all()
    categorys = Category.objects.all()
    sub_categorys = SubCategory.objects.all()
    vendors = Vendor.objects.all()
    # 
    return render(request, "common/productlist.html",{'products':products,'categorys':categorys,'sub_categorys':sub_categorys,'vendors':vendors,'productVars':productVars})

def addCategory(request):
    name= request.GET['category_name']
    discription =request.GET['category_desc']
    category= Category( name=name, desc=discription)
    category.save()
    return redirect('productlist')

def addSubCategory(request):
    name= request.GET['subCategory_name']
    discription =request.GET['subCategory_desc']
    id_ca = request.GET['category']
    category = Category.objects.get(id=id_ca)
    subCategory= SubCategory( name=name, desc=discription,parent=category)
    subCategory.save()
    return redirect('productlist')

def addVendor(request):
    name= request.GET['vendor_name']
    address= request.GET['vendor_address']
    phone= request.GET['vendor_phone']
    desc= request.GET['vendor_desc']
    vendor= Vendor( name=name,address = address,phone=phone,desc=desc)
    vendor.save()
    return redirect('productlist')

def addProduct(request):
    name= request.GET['product_name']
    id_ca = request.GET['category']
    id_sub = request.GET['subcategory']
    category = Category.objects.get(id=id_ca)
    sub = SubCategory.objects.get(id=id_sub)
    discription =request.GET['disscription']
    Product.objects.create(name=name, desc = discription,category= category,sub_category=sub)
    data = Product.objects.all()
    return redirect('productlist')

def addProductVariant(request):
    id_product = request.GET['product']
    product = Product.objects.get(id=id_product)
    quantity = request.GET['productVar_quantity']
    price = request.GET['productVar_price']
    saleOff = request.GET['productVar_sale_off']
    id_vendor = request.GET['vendor']
    vendor = Vendor.objects.get(id=id_vendor)
    is_selling = request.GET['selling']
    is_feature = request.GET['feature']
    ProductVariant.objects.create(product=product,quantity=quantity,price=price,vendor=vendor,is_feature=is_feature,is_selling=is_selling,sale_off=saleOff)
    return redirect('productlist')


def deleteProduct(request,product_id):
    ProductVariant.objects.get(id=product_id).delete()
    # Product.objects.get(id=product_id).delete()
    return redirect('productlist')

def editProduct(request,product_id):
    if request.method == 'POST':
        id = request.POST['id']
        productVariant = ProductVariant.objects.get(id=product_id)
        product = productVariant.product
        name = request.POST['name']
        desc = request.POST['description']
        id_category = request.POST['category']
        category = Category.objects.get(id=id_category)
        id_sub = request.POST['subcategory']
        sub = SubCategory.objects.get(id=id_sub)
        product.name = name
        product.desc = desc
        product.category = category
        product.sub_category = sub
        product.save()
        return redirect('productlist')



    productVariant = ProductVariant.objects.get(id=product_id)
    categorys = Category.objects.all()
    sub_categorys = SubCategory.objects.all()
    return render(request, "common/productEdit.html",{'productVariant':productVariant,'categorys':categorys,'sub_categorys':sub_categorys})


# Search
def productSearch(request):
    
    productName = request.GET['search_name']
    if productName == "":
        productVars =ProductVariant.objects.all()
    else:
        productVars =ProductVariant.objects.filter(product__name__icontains=productName)
        
    
    # ,{'productVariant':productVariant,'productName':productName}
    
    return render(request, "common/productlist.html",{'productVars':productVars})
def editProduct(request):
    return render(request, "common/productEdit.html")

def changeStatusOrder(request, order_id):
    order = Order.objects.get(pk = order_id)
    value = request.POST["choice"]
    order.status = value
    order.save()
    listOrder = Order.objects.all() 
    return render(request, 'common/oders.html', {"oders":listOrder})
