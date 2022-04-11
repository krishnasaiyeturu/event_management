
from functools import partial
from django.db import transaction
from event.api.serializers import CustomerSerializer, MainUserSerializer,EventTypeSerializer,VenueSerializer
from event.models import Customer, EventType, Venue
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
from datetime import datetime, date, timedelta

from django.db import connections

from django.db import connection

cursor = connections['default'].cursor()



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
                return Response({'errors':'password and confirm password should be same'}, status=HTTP_400_BAD_REQUEST)
            user_data = {}
            user_data['username'] = data['email']
            user_data['email'] = data['email']
            user_data['password'] = data['password']
            
            if len(MainUser.objects.raw('SELECT * FROM auth_user WHERE email = %s', [data['email']]))>0:
                return Response({'errors': 'Entered Email ID already Exist'}, status=HTTP_400_BAD_REQUEST)
            main_user_serializer = MainUserSerializer(data=user_data)
            if main_user_serializer.is_valid():
                cursor.execute("INSERT INTO auth_user(username,email,password,is_superuser,first_name,last_name,is_staff,is_active,date_joined) VALUES( %s , %s , %s,%s,%s,%s,%s,%s,%s)", [data['email'], data['email'], data['password'],0,'','',0,1,datetime.now()])
         
            else:
                raise NotFound(main_user_serializer.errors)
            db_user = MainUser.objects.raw('SELECT * FROM auth_user WHERE email = %s', [data['email']])
     
            data['user'] = db_user[0].id
            customer_serializer = CustomerSerializer(data=data)
            if customer_serializer.is_valid():
                cursor.execute("INSERT INTO event_customer(name,contact,email,street,city,state,user_id) VALUES( %s , %s , %s,%s,%s,%s,%s)", [data['name'], data['contact'], data['email'], data['street'], data['city'], data['state'], db_user[0].id])
                get_user=MainUser.objects.get(email=data['email'])
                get_user.set_password(data['password'])
                get_user.save()
                return Response({'sucess':'Customer Created Successfully'},status=HTTP_200_OK)
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
                # main_user = Customer.objects.filter(user=user)
                # if main_user.exists():
                main_user = Customer.objects.raw('SELECT * FROM event_customer WHERE email = %s', [data['email']])
                if len(main_user)>0:
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



class EventAPIView(APIView):

    def get(self, request, *args, **kwargs):
        # print('id' in request.query_params)
        if 'id' in request.query_params:
            event_list = EventType.objects.raw('SELECT * FROM event_eventtype WHERE id = %s', [request.query_params['id']])
            return Response(EventTypeSerializer(event_list, many=True).data, status=HTTP_200_OK)
        else:    
            event_list = EventType.objects.raw('SELECT * FROM event_eventtype')
            return Response(EventTypeSerializer(event_list, many=True).data, status=HTTP_200_OK)

    def post(self,request,*args,**kwargs):
        data = request.data	
        event_serializer = EventTypeSerializer(data=data)
        if event_serializer.is_valid():
            cursor.execute("INSERT INTO event_eventtype(name) VALUES( %s )", [data['name']])
            return Response({'sucess':'Event Type Created Successfully'},status=HTTP_200_OK)
        else:
            raise NotFound(event_serializer.errors)	

    def put(self,request,*args,**kwargs):
        data = request.data	
        event_pk = EventType.objects.get(pk=request.data['id'])
        event_serializer = EventTypeSerializer(event_pk, data=request.data, partial=True)
        if event_serializer.is_valid():
            cursor.execute("UPDATE event_eventtype SET name= %s WHERE id = %s", [data['name'],data['id']])
            return Response({'sucess':'Event Type Updated Successfully'},status=HTTP_200_OK)
        else:
            raise NotFound(event_serializer.errors)	


class VenueAPIView(APIView):
    
    def get(self, request, *args, **kwargs):
        # print('id' in request.query_params)
        if 'id' in request.query_params:
            event_list = Venue.objects.raw('SELECT * FROM event_venue WHERE id = %s', [request.query_params['id']])
            return Response(VenueSerializer(event_list, many=True).data, status=HTTP_200_OK)
        else:    
            event_list = Venue.objects.raw('SELECT * FROM event_venue')
            return Response(VenueSerializer(event_list, many=True).data, status=HTTP_200_OK)

    def post(self,request,*args,**kwargs):
        data = request.data	
        event_serializer = VenueSerializer(data=data)
        if event_serializer.is_valid():
            cursor.execute("INSERT INTO event_venue(name,street,city,state,price_per_day,people_accomodate) VALUES( %s,%s,%s,%s,%s,%s )", [data['name'],data['street'],data['city'],data['state'],data['price_per_day'],data['people_accomodate']])
            return Response({'sucess':'Venue Created Successfully'},status=HTTP_200_OK)
        else:
            raise NotFound(event_serializer.errors)	

    def put(self,request,*args,**kwargs):
        data = request.data	
        event_pk = EventType.objects.get(pk=request.data['id'])
        event_serializer = VenueSerializer(event_pk, data=request.data, partial=True)
        if event_serializer.is_valid():
            cursor.execute("UPDATE event_venue SET name= %s,street=%s,city=%s,state=%s,price_per_day=%s,people_accomodate=%s WHERE id = %s", [data['name'],data['street'],data['city'],data['state'],data['price_per_day'],data['people_accomodate'],data['id']])
            return Response({'sucess':'Venue Updated Successfully'},status=HTTP_200_OK)
        else:
            raise NotFound(event_serializer.errors)

     