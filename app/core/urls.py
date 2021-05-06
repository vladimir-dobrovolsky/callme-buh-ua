"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include, re_path
from django.conf import settings
from django.contrib.flatpages import views
from orders import payments

from home.views import home_page


urlpatterns = [
    path("", home_page, name="home"),
    path("admin/", admin.site.urls),
    path("accounts/", include("users.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("pay-package/<int:id>", payments.pay_package, name="pay_package"),
    re_path("pay-back/(?P<order_id>.{36})/", payments.pay_back, name="pay_back"),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls)),] + urlpatterns

    from django.conf import settings
    from django.conf.urls.static import static

    urlpatterns = urlpatterns + static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

urlpatterns += [
    path("<path:url>", views.flatpage),
]
