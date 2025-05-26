from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('dj_rest_auth.urls')),
    path("api/auth/", include("accounts.urls")),
    # path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    path("api/auth/", include("allauth.socialaccount.urls")),
    path('accounts/', include('allauth.urls')),
    path('api/books/', include('books.urls')), # Added books app urls, added trailing slash
]
