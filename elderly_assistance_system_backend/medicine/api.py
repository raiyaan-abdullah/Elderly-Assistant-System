from medicine.models import Medicine
from rest_framework import viewsets, permissions
from .serializers import LeadSerializer

#Lead Viewset
class LeadViewSet (viewsets.ModelViewSet):
    queryset = Medicine.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]

    serializer_class = LeadSerializer