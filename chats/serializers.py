from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(many=False, slug_field='username', queryset=Profile.objects.all())
    receiver = serializers.SlugRelatedField(many=False, slug_field='username', queryset=Profile.objects.all())

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'message', 'timestamp']
