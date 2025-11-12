# # from django.urls import path
# # from .views import (
# #     ProductReviewListView, ReviewCreateView,
# #     ReviewUpdateView, ReviewDeleteView,
# #     ReviewHelpfulView, UserReviewListView
# # )

# # app_name = 'reviews'

# # urlpatterns = [
# #     # Product reviews
# #     path('products/<int:product_id>/', ProductReviewListView.as_view(), name='product_reviews'),
    
# #     # Review CRUD
# #     path('create/', ReviewCreateView.as_view(), name='review_create'),
# #     path('<int:pk>/update/', ReviewUpdateView.as_view(), name='review_update'),
# #     path('<int:pk>/delete/', ReviewDeleteView.as_view(), name='review_delete'),
# #     path('<int:pk>/helpful/', ReviewHelpfulView.as_view(), name='review_helpful'),
    
# #     # User reviews
# #     path('my-reviews/', UserReviewListView.as_view(), name='user_reviews'),
# # ]
# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.ReviewListView.as_view(), name='review-list'),
# ]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.placeholder_view, name='review-list'),
]
