from django.contrib import admin
from store.models import *
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display=['title','vendors','price','product_status']
    prepopulated_fields={"slug":("title",)}

class CategoryAdmin(admin.ModelAdmin):
    list_display=['title','image']
    prepopulated_fields={"slug":("title",)}

class VendorAdmin(admin.ModelAdmin):
    list_display=['name']
    prepopulated_fields={"slug":("name",)}

class OrderAdmin(admin.ModelAdmin):
    list_display=['user','date_ordered','order_status','is_paid']

class OrderItemsAdmin(admin.ModelAdmin):
    list_display=['order','product','quantity','date_added']

class ReviewAdmin(admin.ModelAdmin):
    list_display=['user','product','rating','date']

class WishlistAdmin(admin.ModelAdmin):
    list_display=['user','product']

class ShippingAddressAdmin(admin.ModelAdmin):
    list_display=['user','address','city','state','zipcode']


admin.site.register(Product,ProductAdmin)
admin.site.register(Vendor,VendorAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem,OrderItemsAdmin)
admin.site.register(Review,ReviewAdmin)
admin.site.register(Wishlist,WishlistAdmin)
admin.site.register(ShippingAddress,ShippingAddressAdmin)
admin.site.register(Tag)









