from rest_framework import serializers
from .models import Mac, Erorr


class MacSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mac
        fields = '__all__'


class ErorrSerializer(serializers.ModelSerializer):
    class Meta:
        model = Erorr
        fields = '__all__'


