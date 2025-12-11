from rest_framework import serializers
from home.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=50, write_only=True)
    phone = serializers.CharField(max_length=15, required=False, allow_null=True, allow_blank=True)
    
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'password', 'email', 'role', 'phone', 'date_joined', 'last_login']
        read_only_fields = ['id', 'date_joined', 'last_login']
    
    def create(self, validated_data):
        # Remove phone if present (we don't want it during signup)
        validated_data.pop('phone', None)
        
        password = validated_data.pop('password')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data.get('role', 'guest'),
            password=password
        )
        return user
    
    def update(self, instance, validated_data):
        # Remove password from validated_data if present
        # (handle password separately in the view)
        validated_data.pop('password', None)
        
        # Update allowed fields
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.username = validated_data.get('username', instance.username)
        instance.phone = validated_data.get('phone', instance.phone)
        # role can be updated if needed
        instance.role = validated_data.get('role', instance.role)
        
        instance.save()
        return instance