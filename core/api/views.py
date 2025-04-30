from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView, RetrieveUpdateDestroyAPIView
from core.models import (
    CustomUser, SiteSettings, Banner, Service, Blog, Testimonial, Category, SubCategory, Product,
    ProductImage, Comment, Favorite, Contact, Message, BasketItem, Promocode, Order, OrderItem, ChatBot
)
from core.api.serializers import (
    UserCreateSerializer, UserSerializer, SiteSettingsSerializer, BannerSerializer, ServiceSerializer, BlogSerializer, 
    TestimonialSerializer, CategorySerializer, SubCategorySerializer, ProductSerializer,
    ProductImageSerializer, CommentSerializer, FavoriteSerializer, FavoriteCreateSerializer, ContactSerializer, MessageSerializer, 
    BasketItemSerializer, BasketItemCreateSerializer, PromoCodeSerializer, OrderSerializer, OrderCreateSerializer, OrderItemSerializer, ChatBotSerializer
)
from core.api.permissions import IsOwner
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

class UserCreateAPIView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserCreateSerializer

class UserRetrieveAPIView(RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = "email"

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

    def perform_create(self, serializer):
        user = serializer.validated_data['user']
        product = serializer.validated_data['product']
        quantity = serializer.validated_data.get('quantity', 1)

        # Try to get existing BasketItem
        basket_item, created = BasketItem.objects.get_or_create(
            user=user,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            basket_item.quantity += quantity
            basket_item.save()

        self.instance = basket_item  # So `.get_success_headers()` works properly

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # Return the updated BasketItem
        updated_serializer = self.get_serializer(self.instance)
        return Response(updated_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class BasketItemRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = BasketItem.objects.all()
    serializer_class = BasketItemCreateSerializer
    lookup_field = "id"

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

class ChatBotListAPIView(ListAPIView):
    queryset = ChatBot.objects.all()
    serializer_class = ChatBotSerializer

class ChatBotRetrieveAPIView(RetrieveAPIView):
    queryset = ChatBot.objects.all()
    serializer_class = ChatBotSerializer
    lookup_field = "id"




# from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
# from allauth.socialaccount.providers.oauth2.client import OAuth2Client
# from dj_rest_auth.registration.views import SocialLoginView

# class GoogleLogin(SocialLoginView):
#     adapter_class = GoogleOAuth2Adapter
#     # callback_url = '/'
#     # client_class = OAuth2Client


import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from dj_rest_auth.jwt_auth import get_refresh_view

class GoogleLoginCallback(APIView):
    def post(self, request):
        code = request.data.get('code')
        redirect_uri = request.data.get('redirect_uri')

        if not code or not redirect_uri:
            return Response({'error': 'Code and redirect_uri are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Step 1: Exchange code for access_token
        token_url = 'https://oauth2.googleapis.com/token'

        payload = {
            'code': code,
            'client_id': settings.SOCIAL_AUTH_GOOGLE_CLIENT_ID,
            'client_secret': settings.SOCIAL_AUTH_GOOGLE_CLIENT_SECRET,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code',
        }

        token_response = requests.post(token_url, data=payload)
        token_data = token_response.json()

        if 'access_token' not in token_data:
            return Response({'error': 'Failed to exchange code.'}, status=status.HTTP_400_BAD_REQUEST)

        access_token = token_data['access_token']

        # Step 2: Get user info from Google
        userinfo_response = requests.get(
            'https://www.googleapis.com/oauth2/v1/userinfo',
            params={'access_token': access_token}
        )
        userinfo = userinfo_response.json()

        if 'email' not in userinfo:
            return Response({'error': 'Failed to get user info.'}, status=status.HTTP_400_BAD_REQUEST)

        # Step 3: Find or create user in your DB
        from django.contrib.auth import get_user_model
        User = get_user_model()

        try:
            user = User.objects.get(email=userinfo['email'])
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=userinfo['email'],
                email=userinfo['email'],
                first_name=userinfo.get('given_name', ''),
                last_name=userinfo.get('family_name', ''),
                password=User.objects.make_random_password()
            )

        # Step 4: Issue JWT tokens
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })