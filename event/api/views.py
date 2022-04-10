
from django.db import transaction
from event.api.serializers import CustomerSerializer, MainUserSerializer
from event.models import Customer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.exceptions import NotFound
from django.contrib.auth.models import User as MainUser

from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from rest_framework import generics,viewsets
from rest_framework.generics import ListAPIView
from rest_framework.permissions import *
from rest_framework.exceptions import NotFound, bad_request





class CustomerAddAPIView(APIView):
    permission_classes = [AllowAny,]
    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            print('Django User-', request.user)
            data = request.data
            print('Django data-', data)
            data._mutable = True
            # data['created_by'] = request.user.pk
            if data['password'] != data['confirm_password']:
                return Response({'password':'password and confirm password should be same'}, status=HTTP_400_BAD_REQUEST)
            user_data = {}
            user_data['username'] = data['email']
            user_data['email'] = data['email']
            user_data['password'] = data['password']
            if MainUser.objects.filter(email=data['email']).exists():
                return Response({'errors': 'Entered Email ID already Exist'}, status=HTTP_400_BAD_REQUEST)
            main_user_serializer = MainUserSerializer(data=user_data)
            if main_user_serializer.is_valid():
                main_user_serializer.save()
            else:
                raise NotFound(main_user_serializer.errors)
            db_user = MainUser.objects.get(username=data['email'])
            db_user.set_password(data['password'])
            db_user.save()
            data['user'] = db_user.pk
            customer_serializer = CustomerSerializer(data=data)
            if customer_serializer.is_valid():
                customer_serializer.save()
                return Response(customer_serializer.data)
            else:
                raise NotFound(customer_serializer.errors)



class LoginAPIView(APIView):
    permission_classes = [AllowAny,]
    def post(self,request,*args,**kwargs):
        data = request.data		
        print ("dataaaa",data)
        email = data['email']
        password = data['password']
        user = authenticate(username=email, password=password)
        print ("dataaaa",user)
        if user is not None:
            if user.is_active:
                main_user = Customer.objects.filter(user=user)
                if main_user.exists():
                    auth_login(request,user)
                    db_user = CustomerSerializer(Customer.objects.get(user__username=email))
                    return Response(db_user.data,status=HTTP_200_OK)
                else:
                    return Response({'error':'Not Assigned Any Web Features'},status=HTTP_400_BAD_REQUEST)
            else:
                print("The username and password were incorrect.")
                return Response({'error':'User not active'},status=HTTP_400_BAD_REQUEST)
        else:
            print("The username and password were incorrect.111111")
            return Response({'login_response':'Username and password were incorrect'},status=HTTP_400_BAD_REQUEST)
