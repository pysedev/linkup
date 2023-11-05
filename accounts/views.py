from rest_framework.views import APIView
from accounts.serializers import EmailSerializer, UserVerifySerializer, UserSerializer, ProfileSerializer
from rest_framework.response import Response
from rest_framework import status
from accounts.models import User, Profile
from utility.permissions import IsOwnerOrReadOnly


class UserCreateView(APIView):
    def post(self, request):
        info = EmailSerializer(data=request.data)
        if info.is_valid():
            user = User.objects.is_exist_user(email=info.validated_data['email'])
            if user:
                if user.is_active:
                    return Response({"error": "user with this email already exists."},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                user = User.objects.create_user(email=info.validated_data['email'])
            User.objects.save_send_verify_code(user)
            return Response({"data": "user created and verify code sent to your email"},
                            status=status.HTTP_201_CREATED)
        return Response(info.errors, status=status.HTTP_400_BAD_REQUEST)


class UserVerifyView(APIView):
    def post(self, request):
        info = UserVerifySerializer(data=request.data)
        if info.is_valid():
            result = User.objects.check_verify_code(**info.validated_data)
            return Response(result, status=status.HTTP_202_ACCEPTED)
        return Response(info.errors, status=status.HTTP_400_BAD_REQUEST)


class UserChangePasswordView(APIView):
    def post(self, request):
        info = EmailSerializer(data=request.data)
        if info.is_valid():
            user = User.objects.is_exist_user(email=info.validated_data['email'])
            if user and user.is_active:
                User.objects.save_send_verify_code(user)
                return Response({"data": "verify code sent to your email"}, status=status.HTTP_202_ACCEPTED)
            return Response({"error": "user whit this email not exist"}, status=status.HTTP_202_ACCEPTED)
        return Response(info.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDeleteView(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    def delete(self, request, pk):
        user = User.objects.is_exist_user(pk=pk)
        if user:
            self.check_object_permissions(request, user)
            user.is_active = False
            user.save()
            Profile.objects.get(user=user).delete()
            return Response({"result": "user deactivated"}, status=status.HTTP_202_ACCEPTED)
        return Response({"error": "id"}, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    def get(self, request, pk):
        user = User.objects.is_exist_user(pk=pk)
        if user:
            return Response(UserSerializer(instance=user).data, status=status.HTTP_200_OK)
        return Response({"error": "id"}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    def get(self, request, pk):
        try:
            profile = Profile.objects.get(id=pk)
            if not profile.user.is_active:
                return Response({"error": "user not exist"}, status=status.HTTP_400_BAD_REQUEST)
            info = ProfileSerializer(instance=profile)
            return Response(info.data, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({"error": "profile not exist"}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            profile = Profile.objects.get(id=pk)
            if not profile.user.is_active:
                return Response({"error": "user not exist"}, status=status.HTTP_400_BAD_REQUEST)
            info = ProfileSerializer(instance=profile, data=request.data, partial=True)
            if info.is_valid():
                self.check_object_permissions(request, profile.user)
                info.save()
                return Response(info.data, status=status.HTTP_202_ACCEPTED)
            return Response(info.errors, status=status.HTTP_400_BAD_REQUEST)
        except Profile.DoesNotExist:
            return Response({"error": "profile not exist"}, status=status.HTTP_400_BAD_REQUEST)
