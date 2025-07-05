from dj_rest_auth.views import PasswordResetConfirmView
from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path

from users.views.auth_view import GoogleLogin, GoogleLoginCallback
from users.views.email import CustomConfirmEmailAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.main.urls', namespace='main')),
    path('', include('users.urls', namespace='users')),
    path('', include('product.urls', namespace='product')),
    path('', include('order.urls', namespace='order')),

    # auth
    path('api/v1/auth/', include('dj_rest_auth.urls')),
    re_path(
        r'^api/v1/auth/registration/account-confirm-email/(?P<key>[-:\w]+)/$',
        CustomConfirmEmailAPIView.as_view(),
        name='account_confirm_email'
    ),
    path('api/v1/auth/registration/', include('dj_rest_auth.registration.urls')),

    # google auth
    path('api/v1/auth/google/', GoogleLogin.as_view(), name='google_login'),
    path(
        "api/v1/auth/google/callback/",
        GoogleLoginCallback.as_view(),
        name="google_login_callback",
    ),

    # api v1
    path('api/v1/', include('product.api_urls', namespace='api-product')),
    path('api/v1/', include('order.api_urls', namespace='api-order')),
    path('api/v1/', include('wishlist.api_urls', namespace='api-wishlist')),
    path('api/v1/', include('review.api_urls', namespace='api-review')),
]

if settings.DEBUG:
    from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
    from django.conf.urls.static import static

    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
        path('silk/', include('silk.urls', namespace='silk')),
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
        path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
