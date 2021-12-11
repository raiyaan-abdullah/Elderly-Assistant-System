from rest_framework import serializers
from medicine.models import Medicine

#Lead Serializer
class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = '__all__'
