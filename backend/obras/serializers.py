
from rest_framework import serializers
from .models import Obra


class ObraSerializer(serializers.ModelSerializer):
    poster = serializers.ImageField()

    class Meta:
        model = Obra
        fields = '__all__'


