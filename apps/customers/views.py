from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.customers.models import CustomerProfile
from apps.customers.serializers import CustomerProfileSerializer


class CustomerProfileViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CustomerProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
