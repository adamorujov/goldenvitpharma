from django.urls import path
from core.api import views

urlpatterns = [
    path('user-create/', views.UserCreateAPIView.as_view(), name="user-create"),
    path('settings/', views.SiteSettingsAPIView.as_view(), name="settings"),
    path('banner-list/', views.BannerListAPIView.as_view(), name="banner-list"),
    path('service-list/', views.ServiceListAPIView.as_view(), name="service-list"),
    path('blog-list/', views.BlogListAPIView.as_view(), name="blog-list"),
    path('blog-retrieve/<int:id>/', views.BlogListAPIView.as_view(), name="blog-list"),
    path('testimonial-list/', views.TestimonialListAPIView.as_view(), name="testimonial-list"),
    path('category-list/', views.CategoryListAPIView.as_view(), name="category-list"),
    path('product-list/', views.ProductListAPIView.as_view(), name="product-list"),
    path('subcategory-product-list/<int:id>/', views.SubCategoryProductListAPIView.as_view(), name="subcategory-product-list"),
    path('product-retrieve/<int:id>/', views.ProductRetrieveAPIView.as_view(), name="product-retrieve"),
    path('comment-create/', views.CommentCreateAPIView.as_view(), name="comment-create"),
    path('user-favorite-list/<email>/', views.UserFavoriteListAPIView.as_view(), name="user-favorite"),
    path('favorite-create/', views.FavoriteCreateAPIView.as_view(), name="favorite-create"),
    path('contact-list/', views.ContactListAPIView.as_view(), name="contact-list"),
    path('message-create/', views.MessageCreateAPIView.as_view(), name="message-create"),
    path('basketitem-create/', views.BasketItemCreateAPIView.as_view(), name="basketitem-create"),
    path('user-basketitem-list/<email>/', views.UserBasketItemListAPIView.as_view(), name="user-basketitem-list"),
    path('promocode-list/', views.PromocodeListAPIView.as_view(), name="promocode-list"),
    path('user-order-list/<email>/', views.UserOrderListAPIView.as_view(), name="user-order-list"),
    path('order-create/', views.OrderCreateAPIView.as_view(), name="order-create"),
    path('order-retrieve-update/<int:id>/', views.OrderRetrieveUpdateAPIView.as_view(), name="order-retrive-update"),
    path('order-item-create/', views.OrderItemCreateAPIView.as_view(), name="order-item-create"),
]