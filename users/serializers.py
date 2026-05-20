from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile


from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile


class UserSerializer(serializers.ModelSerializer):

    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'password', 'role']

    def create(self, validated_data):

        username = validated_data.pop('username')
        password = validated_data.pop('password')

        # ✅ CHECK username already exists
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({
                "username": "Username already exists"
            })

        # ✅ CREATE USER
        user = User.objects.create_user(
            username=username,
            password=password
        )

        # ✅ CREATE PROFILE
        profile = UserProfile.objects.create(
            user=user,
            **validated_data
        )

        return profile




# from rest_framework import serializers
# from .models import UserProfile
# from django.contrib.auth.models import User


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=UserProfile
#         fields=['id','user','role']
# class UserSerializer(serializers.ModelSerializer):
#     # user = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())
#     user = User.objects.get(username="admin")  

#     UserProfile.objects.create(
#     user=user,
#     role="admin"
# )

    # class Meta:
    #     model = UserProfile
    #     fields = ['id', 'user', 'role']