from django.urls import include, path
from . import views

# DRF
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"groups", views.GroupViewSet)

urlpatterns = [
    path("signup/", views.SignUp.as_view(), name="signup"),
    path("profile/", views.user_update, name="profile"),
    # # DRF
    # path('', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
