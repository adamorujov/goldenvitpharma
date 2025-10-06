from django.contrib import admin
from core.models import (
    CustomUser, SiteSettings, Banner, Service, BlogTag, Blog, Testimonial, Category, SubCategory, Product,
    ProductImage, Comment, Favorite, Contact, Message, BasketItem, Promocode, Order, OrderItem, ChatBot, 
    Action, SocialMediaAccount, News
)
from django.contrib.auth.models import Group
from modeltranslation.admin import TranslationAdmin


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name")
    search_fields = ("email",)
    readonly_fields = ("email",)
    


@admin.register(SiteSettings)
class SiteSettingsAdmin(TranslationAdmin):
    pass

@admin.register(Banner)
class BannerAdmin(TranslationAdmin):
    pass

@admin.register(Service)
class ServiceAdmin(TranslationAdmin):
    pass

@admin.register(BlogTag)
class BlogTagAdmin(TranslationAdmin):
    pass

@admin.register(Blog)
class BlogAdmin(TranslationAdmin):
    pass

@admin.register(Testimonial)
class TestimonialAdmin(TranslationAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    pass

@admin.register(SubCategory)
class SubCategoryAdmin(TranslationAdmin):
    pass

@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    pass

admin.site.register(ProductImage)
admin.site.register(Comment)
admin.site.register(Favorite)
admin.site.register(Contact)
admin.site.register(Message)
admin.site.register(BasketItem)
admin.site.register(Promocode)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.unregister(Group)
admin.site.register(ChatBot)
admin.site.register(Action)
admin.site.register(SocialMediaAccount)
admin.site.register(News)