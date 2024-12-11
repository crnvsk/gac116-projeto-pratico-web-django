from django.urls import path, include
from django.http import HttpResponse

from .views import CustomTokenObtainPairView, CustomTokenRefreshView, UserInfoView, LogoutView, RegisterView, TicketViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'tickets', TicketViewSet, basename='ticket')

urlpatterns = [
    path('', include(router.urls)),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('me/', UserInfoView.as_view(), name='user_info'),
]