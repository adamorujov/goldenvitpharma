from modeltranslation.translator import register, TranslationOptions
from .models import (
    SiteSettings, Banner, Service, BlogTag, Blog, Testimonial, Category, SubCategory, Product, News, Action, CustomUser
)

@register(SiteSettings)
class SiteSettingsTranslationOptions(TranslationOptions):
    fields = ('meta_description', 'meta_keywords', 'slogan', 'poster_title1', 'poster_text1', 'poster_title2', 'poster_text2', 'who_we_are', 'our_goal')

@register(Banner)
class BannerTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(Service)
class ServiceTranslationOptions(TranslationOptions):
    fields = ('title', 'text')

@register(BlogTag)
class BlogTagTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Blog)
class BlogTranslationOptions(TranslationOptions):
    fields = ('title', 'short_text', 'text', 'meta_description', 'meta_keywords')

@register(Testimonial)
class TestimonialTranslationOptions(TranslationOptions):
    fields = ('name', 'text')

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(SubCategory)
class SubCategoryTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'meta_description', 'meta_keywords')

@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'content')

@register(Action)
class ActionTranslationOptions(TranslationOptions):
    fields = ('title', 'content')