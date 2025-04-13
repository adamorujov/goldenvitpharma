from rest_framework import serializers
from core.models import (
    CustomUser, SiteSettings, Banner, Service, Blog, Testimonial, Category, SubCategory, Product,
    ProductImage, Comment, Favorite, Contact, Message, BasketItem, Promocode, Order, OrderItem
)
from django.contrib.auth.password_validation import validate_password


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'password')

    def validate(self, data):
        validate_password(data["password"])
        return data

    def create(self, validated_data):
        account = CustomUser.objects.create(
            first_name = validated_data["first_name"],
            last_name = validated_data["last_name"],
            email = validated_data["email"],
            phone_number = validated_data["phone_number"],
        )
        account.set_password(validated_data["password"])
        account.save()
        return account
    

class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = "__all__"


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = "__all__"

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = "__all__"

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True)
    class Meta:
        model = Category
        fields = "__all__"

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)
    product_comments = CommentSerializer(many=True)
    class Meta:
        model = Product
        fields = "__all__"

class FavoriteSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = Favorite
        fields = "__all__"

class FavoriteCreateSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset=CustomUser.objects.all(), slug_field='email')
    class Meta:
        model = Favorite
        fields = "__all__"

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"

class BasketItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = BasketItem
        fields = "__all__"

class BasketItemCreateSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset=CustomUser.objects.all(), slug_field='email')
    class Meta:
        model = BasketItem
        fields = "__all__"

class PromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promocode
        fields = "__all__"

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    order_orderitems = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = "__all__"

class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

