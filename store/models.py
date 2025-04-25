from django.db import models
from django.conf import settings
from shortuuid.django_fields import ShortUUIDField
from django.utils.text import slugify
from userauth.models import User
from django.db.models import Avg


ORDER_STATUS=(
    ("process","In Process"),
    ("shipped","Shipped"),
    ("delivered","Delivered"),
)

PRODUCT_STATUS=(
    ("rejected","Rejected"),
    ("in_review","In Review"),
    ("published","Published"),
)

RATING=(
    (1,"⭐"),
    (2,"⭐⭐"),
    (3,"⭐⭐⭐"),
    (4,"⭐⭐⭐⭐"),
    (5,"⭐⭐⭐⭐⭐"),
    (6,"⭐⭐⭐⭐⭐⭐"),
)

class Tag(models.Model):
    caption = models.CharField(max_length=20)

    def __str__(self):
        return self.caption

class Category(models.Model):
    cid = ShortUUIDField(unique=True,length=10,max_length=20,prefix="category",alphabet="abcdef12345")
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="category")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Categories"

    @property
    def imageURL(self):
        try:
            URL = self.image.url
        except:
            URL= ' '
        return URL
    

class Vendor(models.Model):
    vid = ShortUUIDField(unique=True,length=10,max_length=20,prefix="vendor",alphabet="abcdef12345")

    name = models.CharField(null=True,max_length=30)
    description=models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to="vendors",null=True)

    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name="vendor")
    #one user can have multiple vendor profiles hence why I used Foreign Key

    address=models.CharField(max_length=100,default="123 Main Street, Karachi")
    contact=models.CharField(max_length=100,default="+123 (456) 789")
    shipping_on_time=models.CharField(max_length=100,default="100")
    v_rating = models.IntegerField(choices=RATING,default=1)

    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.user.is_vendor=True
        self.user.save()
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def imageURL(self):
        try:
            URL = self.image.url
        except:
            URL= ' '
        return URL
    #@property
    #def get_rating(self):
    #    return round(self.products.reviews.aggregate(Avg('rating'))['rating__avg'] or 0.0)
    


class Product(models.Model):
    pid = ShortUUIDField(unique=True,length=10,max_length=20,prefix="product",alphabet="abcdef12345")


    title = models.CharField(max_length=200,null=True,default="New product")
    price = models.DecimalField(max_digits=7,decimal_places=2)
    image = models.ImageField(upload_to="products",null=True,blank=True)
    description=models.TextField(null=True,default="This is a product")
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True,blank=True)

    tags = models.ManyToManyField(Tag)
    slug = models.SlugField(unique=True)

    category=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    vendors = models.ForeignKey(Vendor,on_delete=models.CASCADE,null=True,related_name="products")

    product_status = models.CharField(choices=PRODUCT_STATUS,max_length=10,default="in_review")
    rating = models.IntegerField(choices=RATING,default=1)
    in_stock=models.BooleanField(default=True,null=True)
    is_digital = models.BooleanField(default=False,null=True)

    def __str__(self):
        return self.title
    
    @property
    def imageURL(self):
        try:
            URL = self.image.url
        except:
            URL= ' '
        return URL
    
    @property
    def get_rating(self):
        return round(self.reviews.aggregate(Avg('rating'))['rating__avg'] or 0.0)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    
################################### Order Models #####################################
class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    date_ordered=models.DateTimeField(auto_now_add=True)
    transaction_id=ShortUUIDField(unique=True,length=10,max_length=20,prefix="trans",alphabet="abcdefghijk1234567890")

    order_status = models.CharField(choices=ORDER_STATUS,max_length=10,default="process")
    is_paid=models.BooleanField(default=False)


    def __str__(self):
        return f"Order {self.transaction_id}"
    
    @property
    def get_total_cart(self):
        orderitems = self.orderitems.all()
        total=sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems=self.orderitems.all()
        total=sum([item.quantity for item in orderitems])
        return total
    
    @property
    def shipping(self):
        shipping=False
        orderitems = self.orderitems.all()
        for item in orderitems:
            if item.product.is_digital == False:
                shipping = True
        return shipping
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,related_name="products")
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,related_name="orderitems")
    quantity=models.IntegerField(default=0,null=True,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


########################## Review, Wishlists ###################################

class Review(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="reviews")
    text = models.TextField(max_length=400)
    rating = models.IntegerField(choices=RATING,default=1)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review ({self.product.title})"
    
    def get_rating(self):
        return self.rating

class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="wishlist")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title
    
    



################################### Address ###############################

class ShippingAddress(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    address= models.CharField(max_length=200,null=False)
    city=models.CharField(max_length=200,null=False)
    state=models.CharField(max_length=200,null=False)
    zipcode=models.CharField(max_length=200,null=False)
    Country = models.CharField(max_length=200,null=True)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address  
    class Meta:
        verbose_name_plural = "Shipping Addresses"




