from rest_framework import serializers
from medicine_history.models import MedicineHistory

#Lead Serializer
class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineHistory
        fields = '__all__'
