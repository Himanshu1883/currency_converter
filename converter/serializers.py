from rest_framework import serializers
from .models import ConversionLog

class ConversionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversionLog
        fields = '__all__'
        read_only_fields = ['user', 'converted_amount', 'rate', 'timestamp']

