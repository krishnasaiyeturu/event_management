
from functools import partial
from django.db import transaction
from event.api.serializers import CustomerSerializer, EstimatedPriceSerializer, EventManagerSerializer, EventSerializer, MainUserSerializer,EventTypeSerializer,VenueSerializer
from event.models import Customer, EstimatedPrice, Event, EventManager, EventType, Venue
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
                print(main_user,len(main_user))
                if len(main_user)>0:
                    auth_login(request,user)
                    db_user = CustomerSerializer(Customer.objects.get(user__username=email))
                    return Response(db_user.data,status=HTTP_200_OK)
                else:
                    auth_login(request,user)
                    db_user = EventManagerSerializer(EventManager.objects.get(user__username=email))
                    return Response(db_user.data,status=HTTP_200_OK)
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

     


class EstimatedPriceAPIView(APIView):
    
    def get(self, request, *args, **kwargs):
        data = request.query_params
        if 'id' in request.query_params:
            event_list = EstimatedPrice.objects.raw('SELECT * FROM event_estimatedprice WHERE id = %s', [request.query_params['id']])
            return Response(EstimatedPriceSerializer(event_list, many=True).data, status=HTTP_200_OK)
        else:    
            event_list = EstimatedPrice.objects.raw("SELECT event_estimatedprice.id, event_estimatedprice.event_type_id,event_estimatedprice.venue_id, event_estimatedprice.no_of_participants, event_estimatedprice.estimation_price FROM event_estimatedprice WHERE (event_estimatedprice.event_type_id =  %s AND event_estimatedprice.venue_id =  %s)", [data['event_type'],data['venue']])
            # event_list = EstimatedPrice.objects.filter(event_type=data['event_type'],venue=data['venue'])
            # print(event_list.query)
            return Response(EstimatedPriceSerializer(event_list, many=True).data, status=HTTP_200_OK)

    def post(self,request,*args,**kwargs):
        data = request.data	
        event_serializer = EstimatedPriceSerializer(data=data)
        if event_serializer.is_valid():
            cursor.execute("INSERT INTO event_estimatedprice(no_of_participants,estimation_price,event_type_id,venue_id) VALUES( %s,%s,%s,%s )", [data['no_of_participants'],data['estimation_price'],data['event_type'],data['venue']])
            return Response({'sucess':'Price Created Successfully'},status=HTTP_200_OK)
        else:
            raise NotFound(event_serializer.errors)


    def put(self,request,*args,**kwargs):
        data = request.data	
        price_pk = EstimatedPrice.objects.get(pk=request.data['id'])
        price_serializer = EstimatedPriceSerializer(price_pk, data=request.data, partial=True)
        if price_serializer.is_valid():
            cursor.execute("UPDATE event_estimatedprice SET no_of_participants= %s,estimation_price=%s WHERE id = %s", [data['no_of_participants'],data['estimation_price'],data['id']])
            return Response({'sucess':'Price Updated Successfully'},status=HTTP_200_OK)
        else:
            raise NotFound(price_serializer.errors)	





class EventsAPIView(APIView):
    
    def get(self, request, *args, **kwargs):
        data = request.query_params
        # if 'id' in request.query_params:
        #     event_list = Event.objects.raw('SELECT * FROM event_event WHERE id = %s', [request.query_params['id']])
        #     return Response(EventSerializer(event_list, many=True).data, status=HTTP_200_OK)
        # else:    
        #     event_list = Event.objects.raw("SELECT event_estimatedprice.id, event_estimatedprice.event_type_id,event_estimatedprice.venue_id, event_estimatedprice.no_of_participants, event_estimatedprice.estimation_price FROM event_estimatedprice WHERE (event_estimatedprice.event_type_id =  %s AND event_estimatedprice.venue_id =  %s)", [data['event_type'],data['venue']])
        #     # event_list = EstimatedPrice.objects.filter(event_type=data['event_type'],venue=data['venue'])
        #     # print(event_list.query)
        if 'customer' in request.query_params:
            event_list =Event.objects.raw("SELECT event_event.id, event_event.date_of_event, event_event.no_of_participants, event_event.customer_id, event_event.event_type_id, event_event.venue_id, event_event.status, event_event.duration, event_event.estimation_price FROM event_event INNER JOIN event_customer ON (event_event.customer_id = event_customer.id) WHERE event_customer.user_id = %s",[request.user.pk])
            # event_list = Event.objects.filter(customer__user=request.user.pk)
            print(event_list.query)
            return Response(EventSerializer(event_list, many=True).data, status=HTTP_200_OK)
        if 'status' in request.query_params:
            event_list = Event.objects.raw("SELECT event_event.id, event_event.date_of_event, event_event.no_of_participants, event_event.customer_id, event_event.event_type_id, event_event.venue_id, event_event.status, event_event.duration, event_event.estimation_price FROM event_event WHERE event_event.status = %s",[data['status']])
            # event_list = Event.objects.filter(status=data['status'])
            print(event_list.query)
            return Response(EventSerializer(event_list, many=True).data, status=HTTP_200_OK)
        else:
            event_list = Event.objects.raw("SELECT `event_event`.`id`, `event_event`.`date_of_event`, `event_event`.`no_of_participants`, `event_event`.`customer_id`, `event_event`.`event_type_id`, `event_event`.`venue_id`, `event_event`.`status`, `event_event`.`duration`, `event_event`.`estimation_price` FROM `event_event`")
            # event_list = Event.objects.all()
            print(event_list.query)
            return Response(EventSerializer(event_list, many=True).data, status=HTTP_200_OK)


    def post(self,request,*args,**kwargs):
        data = request.data	
        data._mutable = True
        try:
            customer = Customer.objects.get(user = request.user.pk)
        except Customer.DoesNotExist:
            return Response([{'error': 'Kindly Login As User'}], status=HTTP_400_BAD_REQUEST)
        data['customer'] = customer.pk
        event_serializer = EventSerializer(data=data)
        if event_serializer.is_valid():
            cursor.execute("INSERT INTO event_event(date_of_event,no_of_participants,duration,estimation_price,customer_id,event_type_id,venue_id,status) VALUES( %s,%s,%s,%s, %s,%s,%s,%s )", [data['date_of_event'],data['no_of_participants'],data['duration'],data['estimation_price'],data['customer'],data['event_type'],data['venue'],'Requested'])
            return Response({'sucess':'Event Created Successfully'},status=HTTP_200_OK)
        else:
            raise NotFound(event_serializer.errors)

    
    def put(self,request,*args,**kwargs):
        data = request.data	
        price_pk = Event.objects.get(pk=request.data['id'])
        price_serializer = EventSerializer(price_pk, data=request.data, partial=True)
        if price_serializer.is_valid():
            cursor.execute("UPDATE event_event SET status= %s WHERE id = %s", [data['status'],data['id']])
            return Response({'sucess':'Price Updated Successfully'},status=HTTP_200_OK)
        else:
            raise NotFound(price_serializer.errors)	