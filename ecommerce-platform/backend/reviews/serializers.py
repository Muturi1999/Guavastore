# from rest_framework import serializers
# from .models import Review, ReviewImage, ReviewHelpful

# class ReviewImageSerializer(serializers.ModelSerializer):
#     """Review image serializer"""
    
#     class Meta:
#         model = ReviewImage
#         fields = ['id', 'image', 'created_at']

# class ReviewSerializer(serializers.ModelSerializer):
#     """Review serializer"""
    
#     user_name = serializers.CharField(source='user.get_full_name', read_only=True)
#     user_avatar = serializers.CharField(source='user.profile.avatar', read_only=True)
#     images = ReviewImageSerializer(many=True, read_only=True)
#     is_helpful = serializers.SerializerMethodField()
    
#     class Meta:
#         model = Review
#         fields = [
#             'id', 'product', 'user', 'user_name', 'user_avatar',
#             'rating', 'title', 'comment', 'images',
#             'is_verified_purchase', 'is_approved', 'helpful_count',
#             'is_helpful', 'created_at', 'updated_at'
#         ]
#         read_only_fields = [
#             'id', 'user', 'is_verified_purchase', 'is_approved',
#             'helpful_count', 'created_at', 'updated_at'
#         ]
    
#     def get_is_helpful(self, obj):
#         request = self.context.get('request')
#         if request and request.user.is_authenticated:
#             return ReviewHelpful.objects.filter(
#                 review=obj,
#                 user=request.user
#             ).exists()
#         return False

# class ReviewCreateSerializer(serializers.ModelSerializer):
#     """Review creation serializer"""
    
#     images = serializers.ListField(
#         child=serializers.ImageField(),
#         write_only=True,
#         required=False
#     )
    
#     class Meta:
#         model = Review
#         fields = ['product', 'rating', 'title', 'comment', 'images']
    
#     def create(self, validated_data):
#         images_data = validated_data.pop('images', [])
#         review = Review.objects.create(**validated_data)
        
#         # Create review images
#         for image_data in images_data:
#             ReviewImage.objects.create(review=review, image=image_data)
        
#         return review
