"""
URL configuration for goldenvitpharmaproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf.urls.i18n import i18n_patterns

# from dj_rest_auth.views import LoginView
# from dj_rest_auth.jwt_auth import get_refresh_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/core/', include('core.api.urls')),
    path('i18n/', include('django.conf.urls.i18n')),

    # path('auth/', include('dj_rest_auth.urls')),  # login/logout/password reset
    # path('auth/registration/', include('dj_rest_auth.registration.urls')),  # registration
    # path('auth/social/', include('allauth.socialaccount.urls')),  # social login

    path('accounts/', include('allauth.urls')),

    # path('auth/', include('dj_rest_auth.urls')),  # login/logout/password reset
    # path('auth/registration/', include('dj_rest_auth.registration.urls')),  # registration
    path('auth/social/', include('allauth.socialaccount.urls')),  # social login callbacks

    path("auth/", include("dj_rest_auth.urls")),
    path("auth/registration/", include("dj_rest_auth.registration.urls")),
    # path("auth/social/", include("dj_rest_auth.social_urls")),

    path("api/v1/auth/", include("dj_rest_auth.urls")),

    # path('auth/login/', LoginView.as_view(), name='rest_login'),
    # path('auth/token/refresh/', get_refresh_view().as_view(), name='token_refresh')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
