from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'dob', 'password', 'created_at', 'modified_at')
        read_only_fields = ('id', 'created_at', 'modified_at')
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            dob=validated_data['dob'],
            password=validated_data['password']
        )
        return user