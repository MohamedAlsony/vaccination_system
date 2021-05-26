from rest_framework import serializers
from .models import *

class SaveDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildVaccine
        fields = '__all__'

class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = '__all__'

class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = '__all__'