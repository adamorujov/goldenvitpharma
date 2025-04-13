from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from core.models import (
    CustomUser, SiteSettings, Banner, Service, Blog, Testimonial, Category, SubCategory, Product,
    ProductImage, Comment, Favorite, Contact, Message, BasketItem, Promocode, Order, OrderItem
)
from core.api.serializers import (
    UserCreateSerializer, SiteSettingsSerializer, BannerSerializer, ServiceSerializer, BlogSerializer, 
    TestimonialSerializer, CategorySerializer, SubCategorySerializer, ProductSerializer,
    ProductImageSerializer, CommentSerializer, FavoriteSerializer, FavoriteCreateSerializer, ContactSerializer, MessageSerializer, 
    BasketItemSerializer, BasketItemCreateSerializer, PromoCodeSerializer, OrderSerializer, OrderCreateSerializer, OrderItemSerializer
)
from core.api.permissions import IsOwner
from rest_framework.permissions import IsAuthenticated

class UserCreateAPIView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserCreateSerializer

class SiteSettingsAPIView(ListAPIView):
    queryset = SiteSettings.objects.all()
    serializer_class = SiteSettingsSerializer

class BannerListAPIView(ListAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer

class ServiceListAPIView(ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class BlogListAPIView(ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

class BlogRetrieveAPIView(RetrieveAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = "id"

class TestimonialListAPIView(ListAPIView):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer

class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class SubCategoryProductListAPIView(ListAPIView):
    def get_queryset(self):
        id = self.kwargs.get("id")
        return Product.objects.filter(category__id=id)
    serializer_class = ProductSerializer

class ProductRetrieveAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "id"

class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class FavoriteCreateAPIView(CreateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteCreateSerializer
    permission_classes = (IsAuthenticated,)

class UserFavoriteListAPIView(ListAPIView):
    def get_queryset(self):
        email = self.kwargs.get("email")
        return Favorite.objects.filter(user__email=email)
    serializer_class = FavoriteSerializer
    permission_classes = (IsOwner,)

class ContactListAPIView(ListAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

class MessageCreateAPIView(CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class BasketItemCreateAPIView(CreateAPIView):
    queryset = BasketItem.objects.all()
    serializer_class = BasketItemCreateSerializer
    permission_classes = (IsOwner,)

class UserBasketItemListAPIView(ListAPIView):
    def get_queryset(self):
        email = self.kwargs.get("email")
        return BasketItem.objects.filter(user__email=email)
    serializer_class = BasketItemSerializer
    permission_classes = (IsOwner,)

class PromocodeListAPIView(ListAPIView):
    queryset = Promocode.objects.all()
    serializer_class = PromoCodeSerializer

class UserOrderListAPIView(CreateAPIView):
    def get_queryset(self):
        email = self.kwargs.get("email")
        return Order.objects.filter(user__email=email)
    serializer_class = OrderCreateSerializer

class OrderCreateAPIView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer

class OrderRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    lookup_field = "id"


class OrderItemCreateAPIView(CreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

