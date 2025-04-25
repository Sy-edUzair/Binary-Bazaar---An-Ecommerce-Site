from django.shortcuts import render
from .models import *
from django.views.generic import ListView,DetailView
from .forms import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import random
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.generic.edit import FormMixin
from django.views import View
# Create your views here.

#@login_required
class Store(ListView):
    model = Product
    template_name = 'store/storefront.html'
    context_object_name = 'products'


class LoadVendors(ListView):
    model=Vendor
    template_name='store/allvendors.html'
    context_object_name='vendors'

class LoadCategories(ListView):
    model=Category
    template_name='store/allcategories.html'
    context_object_name='categories'

class Render_Cat(ListView):
    model = Category
    template_name = 'store/render_category.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('slug')
        #Retrieves the slug from the URL parameters.
        context['category'] = get_object_or_404(Category, slug=category_slug)
        context['products'] = Product.objects.filter(category__slug=category_slug)

        if not context['products']:
            messages.info(self.request, "No products available in this category yet :(") 
            
        return context
    
class Render_Vendors(ListView):
    model = Vendor
    template_name = 'store/render_vendor.html'
    context_object_name = 'vendor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vendor_slug = self.kwargs.get('slug')
        #Retrieves the slug from the URL parameters.
        context['vendor'] = get_object_or_404(Vendor, slug=vendor_slug)
        context['products'] = Product.objects.filter(vendors__slug=vendor_slug)

        if not context['products']:
            messages.info(self.request, "Vendor hasn't published any products yet :(") 
            
        return context
    
@method_decorator(csrf_protect, name='dispatch')
class ProductDetailView(FormMixin,DetailView):
    model = Product
    template_name = 'store/product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    form_class = ReviewForm 

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        context['related_products'] = Product.objects.filter(category=self.object.category).exclude(id=self.object.id)
        context['reviews'] = self.object.reviews.all().order_by("-date")
        context['review_form'] = self.get_form()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.product = self.object
            review.user = request.user  
            review.save()
            messages.success(request, "Your review has been submitted successfully!")
            return HttpResponseRedirect(reverse('store:render_product', kwargs={'slug': self.object.slug}))
        else:
            return self.form_invalid(form)
        
@login_required
@csrf_protect
def add_to_cart(request,product_id):
    if request.user.is_authenticated:
        try:
            product = get_object_or_404(Product,id=product_id)
            order,created = Order.objects.get_or_create(user=request.user,is_paid=False)

            order_item,created = OrderItem.objects.get_or_create(order=order, product=product)

            if created:
                messages.success(request, f"Product {product.title} Added to Cart Successfully!")
                order_item.quantity = 1
            else:
                messages.success(request, f"Product {[product.title]} Added to Cart Successfully!")
                order_item.quantity +=1

            order_item.save()
        except:
            messages.warning(request,"Unexpected Error Occured!")
    else:
        messages.warning(request,"You are not authenticated please login/register first!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def cart(request):
    if request.user.is_authenticated:
        order,created = Order.objects.get_or_create(user=request.user,is_paid=False)
        order_items = order.orderitems.all()
        context={
            'order':order,
            'items':order_items
        }
    else:
        context={}
    return render(request,'store/cart.html',context)

@login_required
def delete_from_cart(request, item_id):
    if request.user.is_authenticated:
        order = get_object_or_404(Order, user=request.user, is_paid=False)
        order_item = get_object_or_404(OrderItem, order=order, id=item_id)
        
        order_item.delete()
        
        messages.success(request, "Item removed from cart successfully!")
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def edit_quantity(request,item_id,action = 1): # action = 1 is add and any other number is remove
    if request.user.is_authenticated:
        order = get_object_or_404(Order, user=request.user, is_paid=False)
        order_item = get_object_or_404(OrderItem, order=order, id=item_id)
        
        if action==1:
            order_item.quantity = order_item.quantity+1
            order_item.save()
        else:
            order_item.quantity = order_item.quantity-1
            order_item.save()
            if order_item.quantity <= 0:
                delete_from_cart(request,item_id)
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def checkout(request):
    if request.user.is_authenticated:
        AddressForm = ShippingAddressForm
        order = get_object_or_404(Order,user=request.user,is_paid=False)
        order_items = order.orderitems.all()
        context={
            'order':order,
            'items':order_items,
            'addressform':AddressForm
        }
    else:
        context={'addressform':AddressForm}
    return render(request,'store/checkout.html',context)

@login_required
@csrf_protect
def ProcessOrder(request):
    if request.method=='POST':
        order = get_object_or_404(Order,user=request.user,is_paid=False)
        form = ShippingAddressForm(data=request.POST)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.user = request.user  
            shipping_address.save()

            order.order_status='shipped'
            order.is_paid=True

            order_items = order.orderitems.all()
            for item in order_items:
                item.delete()

            order.save()
            messages.success(request,"Order Processed!")
            return HttpResponseRedirect(reverse('store:store'))
        else:
            messages.warning(request,form.errors)
    else:
        form = ShippingAddressForm()
    return render(request, 'store/vendor_form.html', {'form': form})

@login_required
@csrf_protect
def create_vendor(request):
    if request.method == 'POST':
        form = VendorForm(data= request.POST, files = request.FILES)  # Include request.FILES for images
        if form.is_valid():
            vendor = form.save(commit=False)
            vendor.user = request.user  # Get the logged-in user
            original_slug = slugify(vendor.name)
            unique_slug = original_slug
            counter = 1
            while Vendor.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{original_slug}-{counter}"
                counter += 1
            vendor.slug = unique_slug
            vendor.save()
            messages.success(request, 'Vendor created successfully!')
            return HttpResponseRedirect(reverse('store:store'))
    else:
        form = VendorForm()
    return render(request, 'store/vendor_form.html', {'form': form})

@login_required
@csrf_protect
def create_product(request,vendor_slug):
    if request.method == 'POST':
        form = AddProductForm(data= request.POST, files = request.FILES)  # Include request.FILES for images
        if form.is_valid():
            product = form.save(commit=False)
            if request.user.is_vendor:
                product.vendors = Vendor.objects.get(slug=vendor_slug)
                original_slug = slugify(product.title)
                unique_slug = original_slug
                counter = 1
                while Product.objects.filter(slug=unique_slug).exists():
                    unique_slug = f"{original_slug}-{counter}"
                    counter += 1
                product.slug = unique_slug
                product.save()
                messages.success(request, 'Product created successfully!')
                #return HttpResponseRedirect(reverse('store:vender_dashboard',kwargs={'slug':vendor_slug}))
                return HttpResponseRedirect(reverse('store:render_profiles'))       
    else:
        form = AddProductForm()
    return render(request, 'store/product_form.html', {'form': form})


class VenderDashboard(LoginRequiredMixin,DetailView):
    model = Vendor
    template_name = 'store/vender_dashboard.html'
    context_object_name = 'vendor'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vendor_slug = self.kwargs.get('slug')
        vendor = get_object_or_404(Vendor, slug=vendor_slug)
        
        context['products'] = Product.objects.filter(vendors=vendor).order_by("-date")[:3]
        context['reviews'] = Review.objects.filter(product__in=context['products']).order_by("-date")

        if not context['products']:
            messages.info(self.request, "No published products yet :( ")

        return context
    
@login_required
def render_user_vendors(request):
    if not request.user.is_vendor:
        messages.info(request, "Vendor not Authenticated!")
        return HttpResponseRedirect('store:vendor-register')  # Redirect to login if not vendor

    try:
        vendor_profiles = Vendor.objects.filter(user=request.user)
    except Vendor.DoesNotExist:
        messages.error(request, "You don't have a vendor profile associated with your account.")
        return HttpResponseRedirect('store:vendor-register')  # Redirect to a view for creating a vendor profile
    
    return render(request, 'store/render_vender_profiles.html', {
        "vendors":vendor_profiles,
    })
    
    
class WishlistViews(View):
    def post(self,request):
        wishlist=request.session.get("stored-products")

        if wishlist is None:
            wishlist=[]
        productslug = request.POST.get("product_slug")
        if productslug not in wishlist:#no duplicate ids check
            messages.success(request, 'Product added to wishlist!')
            wishlist.append(productslug)
        else:#if it is in read later list then do this
            messages.success(request, 'Product removed from wishlist!')
            wishlist.remove(productslug)

        request.session["stored-products"] = wishlist
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    def get(self,request):
        wishlist=request.session.get("stored-products")

        context = {}
        if wishlist is None or len(wishlist) == 0:
            context["products"] = []
            context["has_products"] = False
        else:
            context["products"] = Product.objects.filter(slug__in=wishlist) #the "__in" modifier mean that I want slugs that are stored in storedposts list only
            context["has_products"] = True

        return render(request,"store/wishlist.html",context)