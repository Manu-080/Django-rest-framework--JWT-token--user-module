from django.shortcuts import render, get_object_or_404

# rest frame work
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import BasicAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
# Create your views here.

class UsersView(APIView): # view all users
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        print(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class UserView(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]

    def get_object(self, pk):
        try:
            return User.objects.get(id=pk)
        except User.DoesNotExist:
            return None
        
    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def delete(self, request,pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
       
# class RegisterView(APIView): # Signup

#     def post(self, request):
#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class RegisterView(generics.CreateAPIView): # SIGNUP

    serializer_class = RegisterSerializer


class LoginView(generics.GenericAPIView): # LOGIN 

    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True) # raise exception  if not serilaizer.is_valid()
        user = serializer.validated_data['user']
        #print("Authenticated user:", user)  # Debug
        refresh = RefreshToken.for_user(user)
        print(request.user)
        return Response({'Refresh':str(refresh), 'access':str(refresh.access_token)}, status=status.HTTP_200_OK)
    

class UserProfile(APIView): # DASHBOARD
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        print(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class Logout(APIView):
    permission_classes =[IsAuthenticated]
    authentication_classes = [JWTAuthentication]


    def post(self, request):
        print(self.http_method_names)
        try:
            refresh_token = request.data.get('refresh_token') # Get the the refresh token not access token
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({'message':'logout successfull'}, status=status.HTTP_205_RESET_CONTENT)
            else:
                return Response({'message':'refresh_token is required'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'message':'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

