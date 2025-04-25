from django.urls import path
from . import views

app_name = "store"
urlpatterns=[
    path('',views.Store.as_view(),name="store"),
    path("cart_detail/",views.cart,name="cart"),
    path("<int:product_id>/add/", views.add_to_cart, name='add_to_cart'),
    path("cart_detail/<int:item_id>/delete", views.delete_from_cart, name='delete_from_cart'),
    path("cart_detail/<int:item_id>/<int:action>/edit_quantity", views.edit_quantity, name='edit_quantity'),
    path("checkout/",views.checkout,name="checkout"),
    path("checkout/process-order",views.ProcessOrder,name="process-order"),
    path("vendor-register/",views.create_vendor,name="vendor-register"),
    path("wishlist/",views.WishlistViews.as_view(),name="wish-list"),
    path("all-vendors/",views.LoadVendors.as_view(),name="load-vendors"),
    path("all-categories/",views.LoadCategories.as_view(),name="load-category"),
    path("all-categories/<slug:slug>",views.Render_Cat.as_view(), name='render_category'),
    path("all-vendors/<slug:slug>",views.Render_Vendors.as_view(), name='render_vendor'),
    path("<slug:slug>/",views.ProductDetailView.as_view(), name="render_product"),
    path("user/vender-profiles/", views.render_user_vendors, name='render_profiles'),
    path("user/vender-profiles/<slug:slug>", views.VenderDashboard.as_view(), name='vendor_dashboard'),
    path("user/vender-profiles/<slug:vendor_slug>/add-product", views.create_product, name='add-product'),
]