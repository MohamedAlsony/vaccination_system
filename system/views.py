from django.shortcuts import render
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import *

@api_view(['POST',])
@permission_classes((AllowAny,))
def parent_view(request):
    if request.method == 'POST':
        serializer = ParentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

@api_view(['POST',])
@permission_classes((AllowAny,))
def child_view(request):
    if request.method == 'POST':
        serializer = ChildSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


@api_view(['POST',])
@permission_classes((AllowAny,))
def save_data(request):
    if request.method == 'POST':
        data = request.data.copy()
        data['child'] = Child.objects.get(name='c1').pk
        data['vaccine'] = [Vaccine.objects.get(name='v1').pk]
        serializer = SaveDataSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)