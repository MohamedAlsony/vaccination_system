
from django.db.models import Q
from django.shortcuts import render
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import *
from datetime import date
from django.core.mail import EmailMessage
import requests

@api_view(['POST',])
@permission_classes((AllowAny,))
def parent_view(request):
    if request.method == 'POST':
        serializer = ParentSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data = serializer.data.copy()
            data['response'] = 'success'
            return Response(data= data)
        data = serializer.errors.copy()

        if 'email' in data:
            data['error_msg'] = 'this email already in use'
        elif 'nationalid' in data:
            data['error_msg'] = 'incorrect national ID'
        else:
            s = ''
            for i in data:
                s += f'invalid {i}, ' + ''.join(data[i])
            data['error_msg'] = s
        data['response'] = 'error'
        return Response(data=data)

@api_view(['POST',])
@permission_classes((AllowAny,))
def child_view(request):
    if request.method == 'POST':
        data = request.data.copy()
        parent = Parent.objects.filter(Q(email=request.data.get('parent')) & Q(password=request.data.get('password')))
        if parent.count()==0:
            return Response(data={'response':'error', 'error_msg':'invalid parent data'})
        data['parent'] = parent[0].id
        z = request.data.get('date_of_birth').split('-')
        child_date = date(year = int(z[0]), month= int(z[1]), day=int(z[2]))
        x = date.today() - child_date
        d = x.days
        y = d / 365
        if d < 0 or (y > 12):
            data = {'response': 'error', 'error_msg': 'The age of this child is not appropriate'}
            return Response(data=data)
        serializer = ChildSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data.copy()
            data['response'] = 'success'
            return Response(data= data)
        data = serializer.errors.copy()
        #data['response'] = 'error'
        if 'nationalid' in data:
            data['error_msg'] = 'incorrect national ID'
        else:
            s = ''
            for i in data:
                s+= f'invalid {i}, ' + ''.join(data[i])
            data['error_msg'] = s
        data['response'] = 'error'
        return Response(data= data)


@api_view(['POST',])
@permission_classes((AllowAny,))
def save_data(request):
    if request.method == 'POST':
        data = request.data.copy()
        serializer = SaveDataSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

@api_view(['POST',])
@permission_classes((AllowAny,))
def child_vaccine_view(request):
    data = request.data.copy()
    parent = data['parent']
    try:
        parent = Parent.objects.get(email=parent)
    except Parent.DoesNotExist:
        data = {'response':'this parent name Does Not Exist!'}
        return Response(data)
    child = parent.child_set.all()
    if len(child) == 0:
        data = {'response':'this parent has no registered child!'}
        return Response(data=data)
    if request.method=='POST':
        child_vaccine = {}
        child_vaccine_api = {}
        vaccine = Vaccine.objects.all()
        for c in child:
            age = date.today() - c.date_of_birth
            age = int(age.days/365)

            for v in vaccine:
                vacs = vaccine.filter(Q(child_age_from__lte = age) & Q(child_age_to__gte = age))
                child_vaccine[c.name] = "avalible vaccine: " + ",".join(str(x) for x in vacs)
                child_vaccine_api[c.id] = [int(x.id) for x in vacs]
                if len(vacs) == 0: child_vaccine[c.name]='this child have no available vaccine right now!'
        email_subject = 'Child Vaccination system,'
        email_body = f"""hi {parent.name},
updated at: {date.today()}
{'-'*40}
your children data:
child name -> avalible vaccine(s):
"""
        for i in child:
            if i.name not in child_vaccine:
                child_vaccine[i.name] = 'this child have no available vaccine right now!'
        for key in child_vaccine:
            email_body += f"{key} -> {child_vaccine[key]}\n"
        to_account = [str(parent.email)]
        email = EmailMessage(email_subject,email_body,to=to_account)
        email.send()
        for key in child_vaccine_api:
            child_vaccine_api_dict = {}
            child_vaccine_api_dict['child'] = key
            child_vaccine_api_dict['vaccine'] = child_vaccine_api[key]
            serializer = SaveDataSerializer(data=child_vaccine_api_dict)
            if serializer.is_valid():
                serializer.save()
        return Response(data= {"response":"succeeded"})
    return Response(data= {"response":"error"})

@api_view(['GET',])
@permission_classes((AllowAny,))
def seen_by_parent_view(request, parent, vaccine):
    if request.method == 'GET':
        data = {}
        data['parent'] = parent
        data['vaccine'] = vaccine
        data['seen'] = True
        serializer = SeenByParentSerializer(data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'Done!'})
        return Response(serializer.errors)