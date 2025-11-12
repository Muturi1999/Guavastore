from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import Address, UserProfile

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    """User profile serializer"""
    
    class Meta:
        model = UserProfile
        fields = [
            'avatar', 'bio', 'date_of_birth', 'gender',
            'newsletter_subscribed', 'currency', 'language'
        ]

class AddressSerializer(serializers.ModelSerializer):
    """Address serializer"""
    
    class Meta:
        model = Address
        fields = [
            'id', 'address_type', 'full_name', 'phone',
            'address_line1', 'address_line2', 'city', 'county',
            'postal_code', 'country', 'is_default', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

class UserSerializer(serializers.ModelSerializer):
    """User serializer"""
    
    profile = UserProfileSerializer(required=False)
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'full_name',
            'phone', 'is_verified', 'profile', 'date_joined'
        ]
        read_only_fields = ['id', 'is_verified', 'date_joined']

class RegisterSerializer(serializers.ModelSerializer):
    """User registration serializer"""
    
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = [
            'email', 'password', 'password2',
            'first_name', 'last_name', 'phone'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        
        # Create profile
        UserProfile.objects.create(user=user)
        
        return user

class ChangePasswordSerializer(serializers.Serializer):
    """Change password serializer"""
    
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(
        required=True, 
        write_only=True,
        validators=[validate_password]
    )
    new_password2 = serializers.CharField(required=True, write_only=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError(
                {"new_password": "Password fields didn't match."}
            )
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

class UserUpdateSerializer(serializers.ModelSerializer):
    """User update serializer"""
    
    profile = UserProfileSerializer(required=False)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'profile']
    
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        
        # Update user fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update profile if provided
        if profile_data:
            profile = instance.profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
        
        return instance