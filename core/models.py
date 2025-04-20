from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib import auth
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def with_perm(self, perm, is_active=True, include_superusers=True, backend=None, obj=None):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    'You have multiple authentication backends configured and '
                    'therefore must provide the `backend` argument.'
                )
        elif not isinstance(backend, str):
            raise TypeError(
                'backend must be a dotted import path string (got %r).'
                % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, 'with_perm'):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(max_length=30, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        ordering = ["-id"]
        verbose_name = "user"

    objects = UserManager()


class SiteSettings(models.Model):
    # meta
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.TextField(blank=True, null=True)

    # main
    logo = models.TextField(blank=True, null=True)
    favicon = models.ImageField(upload_to='core_images/', blank=True, null=True)
    slogan = models.TextField(blank=True, null=True)

    # poster
    poster_title1 = models.TextField(blank=True, null=True)
    poster_text1 = models.TextField(blank=True, null=True)
    poster_image1 = models.ImageField(upload_to='core_images/', blank=True, null=True)

    poster_title2 = models.TextField(blank=True, null=True)
    poster_text2 = models.TextField(blank=True, null=True)
    poster_image2 = models.ImageField(upload_to='core_images/', blank=True, null=True)

    # contact
    contact_email = models.EmailField(max_length=256, blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = "settings"
        verbose_name_plural = "settings"

    def save(self, *args, **kwargs):
        if not self.id and SiteSettings.objects.exists():
            return None
        return super(SiteSettings, self).save(*args, **kwargs)

    def __str__(self):
        return "Settings"


class Banner(models.Model):
    title = models.CharField(max_length=300)
    image = models.ImageField(upload_to="core_images/")

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return self.title
    
class Service(models.Model):
    title = models.CharField(max_length=300)
    text = models.TextField()
    image = models.ImageField(upload_to="service_images/")

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return self.title
    
class BlogTag(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return self.name
    
class Blog(models.Model):
    title = models.CharField(max_length=300)
    short_text = models.TextField(blank=True, null=True)
    text = HTMLField()
    image = models.ImageField(upload_to="blog_images/")
    read_time = models.DurationField(default=0)
    created_at = models.DateField(default=timezone.now)
    tags = models.ManyToManyField(BlogTag, related_name="blogs", blank=True)

    # meta
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return self.title

    
class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    text = models.TextField()
    image = models.ImageField(upload_to="client_images/")

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return self.name
    

class Category(models.Model):
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to="category_images/")

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        ordering = ("-id",)

    def __str__(self):
        return self.title
    
class SubCategory(models.Model):
    super_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories", blank=True, null=True)
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to="category_images/", blank=True, null=True)

    class Meta:
        verbose_name = "subcategory"
        verbose_name_plural = "subcategories"
        ordering = ("-id",)

    def __str__(self):
        return self.title

class Product(models.Model):
    category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, related_name="products", blank=True, null=True)
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=300)
    description = HTMLField(blank=True, null=True)
    price = models.FloatField(default=0)
    discount_percentage = models.FloatField(default=0)
    discount_price = models.FloatField(default=0)
    is_stock = models.BooleanField(default=True)
    is_bestseller = models.BooleanField(default=False)

    # meta
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    image = models.ImageField(upload_to="product_images/")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")

    class Meta:
        verbose_name = "product image"
        ordering = ("-id",)

    def __str__(self):
        return self.product.name + " " + str(self.id)
    
class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name="user_comments", blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_comments", blank=True, null=True)
    anonim_user = models.CharField(max_length=50, blank=True, null=True)
    content = HTMLField()
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return self.content
    
class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_favorites")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_favorites")

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return self.user.email + " " + self.product.name
    
class Contact(models.Model):
    number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=256, blank=True, null=True)

    class Meta:
        ordering = ("-id",)

class Message(models.Model):
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=256)
    message = models.TextField()

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return self.full_name


class BasketItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_basketitems")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_basketitems")
    quantity = models.IntegerField(default=0)

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return self.user.email + " " + self.product.name
    

class Promocode(models.Model):
    code = models.CharField(max_length=30)
    percentage = models.FloatField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return self.code
    
class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="orders")
    full_name = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=20)
    city = models.CharField(max_length=30)
    address = models.TextField()
    note = models.TextField(blank=True, null=True)
    is_agree = models.BooleanField(default=False)
    amount = models.FloatField(default=0)
    promocode = models.CharField(max_length=30, blank=True, null=True)
    promocode_percentage = models.FloatField(default=0)
    total_amount = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-id",)

    def save(self, *args, **kwargs):
        if self.id:
            orderitems = self.order_orderitems.all()
            amount = 0
            for orderitem in orderitems:
                amount += orderitem.product.price * orderitem.quantity
            self.amount = amount
            self.total_amount = amount - (amount * self.promocode_percentage / 100)
        return super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return self.full_name
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_orderitems")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_orderitems")
    quantity = models.IntegerField(default=0)

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return self.order.full_name + " " + self.product.name
