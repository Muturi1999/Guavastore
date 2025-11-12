from rest_framework import viewsets, permissions
from .models import Coupon
from .serializers import CouponSerializer
from django.utils import timezone

class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all().order_by('-created_at')
    serializer_class = CouponSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Return only active and valid coupons
        now = timezone.now()
        return Coupon.objects.filter(
            is_active=True,
            valid_from__lte=now,
            valid_until__gte=now
        ).order_by('-created_at')
