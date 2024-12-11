from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from rest_framework import viewsets, permissions
from .serializers import UserSerializer, RegisterSerializer, TicketSerializer

from .models import Ticket

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            access_token = response.data['access']
            refresh_token = response.data['refresh']
            # Set cookies
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=False,
                samesite='Lax',
            )
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=False,
                samesite='Lax',
            )
        return response

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            access_token = response.data['access']
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=False,
                samesite='Lax',
            )
        return response

class LogoutView(APIView):
    def post(self, request):
        response = Response(status=204)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response

class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            response = Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)

            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=False,
                samesite='Lax',
            )
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=False,
                samesite='Lax',
            )
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "employee":
            return Ticket.objects.all().order_by("-created_at")  # Employees see all tickets
        elif user.role == "client":
            return Ticket.objects.filter(created_by=user).order_by("-created_at")  # Clients see their tickets
        return Ticket.objects.none()

    def perform_create(self, serializer):
        # Ensure that created_by is always set to the logged-in user
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        user = self.request.user
        if user.role == "employee":
            allowed_fields = ['status', 'response']
            for field in self.request.data.keys():
                if field not in allowed_fields:
                    raise PermissionDenied(f"Employees can only update the following fields: {allowed_fields}")
            serializer.save()
        elif user.role == "client":
            raise PermissionDenied("Clients cannot update tickets.")
        else:
            raise PermissionDenied("Unauthorized access.")


class TicketDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Ticket.objects.get(pk=pk)
        except Ticket.DoesNotExist:
            return None

    def delete(self, request, pk):
        ticket = self.get_object(pk)
        if not ticket:
            return Response({"error": "Ticket not found"}, status=status.HTTP_404_NOT_FOUND)

        # Customers can delete only their own tickets
        if request.user.role == 'client' and ticket.created_by != request.user:
            return Response({"error": "You can only delete your own tickets"}, status=status.HTTP_403_FORBIDDEN)

        # Employees can delete any ticket
        if request.user.role == 'employee' or ticket.created_by == request.user:
            ticket.delete()
            return Response({"message": "Ticket deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        return Response({"error": "Unauthorized action"}, status=status.HTTP_403_FORBIDDEN)