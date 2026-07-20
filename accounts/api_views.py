from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer, ProfileSerializer

class RegisterAPIView(CreateAPIView):
    serializer_class=RegisterSerializer

class ProfileAPIView(RetrieveUpdateAPIView):
    serializer_class=ProfileSerializer
    permission_classes=[IsAuthenticated]

    def get_object(self):
        return self.request.user.profile
    
    