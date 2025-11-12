
# from django.db import models
# from django.conf import settings
# from django.core.validators import MinValueValidator, MaxValueValidator
# from products.models import Product

# class Review(models.Model):
#     """Product review model"""
    
#     product = models.ForeignKey(
#         Product,
#         on_delete=models.CASCADE,
#         related_name='reviews'
#     )
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name='reviews'
#     )
#     order = models.ForeignKey(
#         'orders.Order',
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name='reviews'
#     )
    
#     # Review content
#     rating = models.IntegerField(
#         validators=[MinValueValidator(1), MaxValueValidator(5)]
#     )
#     title = models.CharField(max_length=200)
#     comment = models.TextField()
    
#     # Verification
#     is_verified_purchase = models.BooleanField(default=False)
    
#     # Status
#     is_approved = models.BooleanField(default=True)
    
#     # Helpful votes
#     helpful_count = models.IntegerField(default=0)
    
#     # Timestamps
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         unique_together = ['product', 'user']
#         ordering = ['-created_at']
#         indexes = [
#             models.Index(fields=['product', 'is_approved']),
#         ]
    
#     def __str__(self):
#         return f"{self.user.email} - {self.product.name} ({self.rating}★)"
    
#     def save(self, *args, **kwargs):
#         is_new = self.pk is None
#         super().save(*args, **kwargs)
        
#         # Update product rating
#         if is_new:
#             self.update_product_rating()
    
#     def update_product_rating(self):
#         """Update product's average rating and review count"""
#         from django.db.models import Avg, Count
        
#         stats = Review.objects.filter(
#             product=self.product,
#             is_approved=True
#         ).aggregate(
#             avg_rating=Avg('rating'),
#             count=Count('id')
#         )
        
#         self.product.average_rating = stats['avg_rating'] or 0
#         self.product.review_count = stats['count']
#         self.product.save(update_fields=['average_rating', 'review_count'])

# class ReviewImage(models.Model):
#     """Review images"""
    
#     review = models.ForeignKey(
#         Review,
#         on_delete=models.CASCADE,
#         related_name='images'
#     )
#     image = models.ImageField(upload_to='reviews/')
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     class Meta:
#         ordering = ['created_at']
    
#     def __str__(self):
#         return f"Image for review {self.review.id}"

# class ReviewHelpful(models.Model):
#     """Track helpful votes for reviews"""
    
#     review = models.ForeignKey(
#         Review,
#         on_delete=models.CASCADE,
#         related_name='helpful_votes'
#     )
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE
#     )
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     class Meta:
#         unique_together = ['review', 'user']
#         ordering = ['-created_at']
    
#     def __str__(self):
#         return f"{self.user.email} found review {self.review.id} helpful"