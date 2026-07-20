from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer, ProfileSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(summary="Register user", description="Create a new user account")
class RegisterAPIView(CreateAPIView):
    serializer_class=RegisterSerializer

@extend_schema(summary="User profile", description="Get or update current user profile")
class ProfileAPIView(RetrieveUpdateAPIView):
    serializer_class=ProfileSerializer
    permission_classes=[IsAuthenticated]

    def get_object(self):
        return self.request.user.profile
    
    