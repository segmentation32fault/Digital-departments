from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Post, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content']


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        # extra_kwargs = {'password', {'write_only': True}}

    def save(self):
        user = User(username=self.validated_data['username'], email=self.validated_data['email'])
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match'})

        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
