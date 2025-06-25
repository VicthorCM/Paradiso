from rest_framework import serializers
from .models import Comentario

class SerializadorComentario(serializers.ModelSerializer):

    class Meta: 
        model = Comentario
        fields = '__all__'

   