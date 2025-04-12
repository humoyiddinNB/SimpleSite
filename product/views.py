from django.shortcuts import render
from .models import Post
from .serializers import PostSerializers
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication

class Posts(generics.GenericAPIView):
    permission_classes = permissions.IsAuthenticated,
    authentication_classes = TokenAuthentication,
    def get(self, requests):
        posts = Post.objects.all()
        serializer = PostSerializers(posts, many=True)
        return Response({
            'data' : serializer.data
        })

class ProductCreate(generics.CreateAPIView):
    serializer_class = PostSerializers
    queryset = Posts