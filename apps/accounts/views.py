from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from .models import UserProfile
from .serializers import UserProfileSerializer, RegisterSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "Registration successful"},
            status=status.HTTP_201_CREATED
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_profile(self):
        user = self.request.user

        profile = UserProfile.objects.filter(user=user).first()
        if profile:
            return profile

        profile = UserProfile.objects.create(
            user=user,
            name=user.username,
            email=user.email or f"{user.username}_{user.id}@aethercart.local",
            role="customer"
        )

        return profile

    def get_queryset(self):
        profile = self.get_profile()
        return UserProfile.objects.filter(id=profile.id)

    def list(self, request, *args, **kwargs):
        profile = self.get_profile()
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        profile = self.get_profile()

        serializer = self.get_serializer(
            profile,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        profile = self.get_profile()

        serializer = self.get_serializer(
            profile,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)