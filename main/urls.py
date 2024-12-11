from django.urls import path
from django.http import HttpResponse
from .views import CustomTokenObtainPairView, CustomTokenRefreshView, UserInfoView, LogoutView, RegisterView

def hello_world(request):
    return HttpResponse("Hello, World!")

urlpatterns = [
    path('', hello_world, name='hello_world'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('me/', UserInfoView.as_view(), name='user_info'),
]