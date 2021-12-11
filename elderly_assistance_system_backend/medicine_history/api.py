from medicine_history.models import MedicineHistory
from rest_framework import viewsets, permissions
from .serializers import LeadSerializer

#Lead Viewset
class LeadViewSet (viewsets.ModelViewSet):
    queryset = MedicineHistory.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]

    serializer_class = LeadSerializer