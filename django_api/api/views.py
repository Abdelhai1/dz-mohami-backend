from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import AppointmentSerializer, CommentSerializer, LawyerCommentSerializer, LawyerProfileSerializer, LawyersSerializer, LoginSerializer, ReservationSerializer, UserSerializer,LawyerSerializer
from .models import Reservation, User,Lawyer,Appointment
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password
from rest_framework.parsers import JSONParser
from rest_framework.decorators import parser_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Lawyer
import json
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
# Create your views here.


@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List': '/user-list/',
        'Detail View': '/user-detail/<int:id>',
        'Create': '/user-create/',
        'Update': '/user-update/<int:id>',
        'Delete': '/user-delete/<int:id>',
    }
    
    return Response(api_urls);

#t3 get all users
@api_view(['GET'])
def showAllUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many =True)
    return Response(serializer.data)

#get user with id
@api_view(['GET'])
def showUser(request , pk):
    user = User.objects.get(id = pk)
    serializer = UserSerializer(user, many =False)
    return Response(serializer.data)

#create the user
@api_view(['POST'])
@parser_classes([JSONParser])
def createUser(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

#update the user
@api_view(['POST'])
def updateUser(request , pk):
    user = User.objects.get(id = pk)
    serializer = UserSerializer(instance=user,data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

#delete the user
@api_view(['GET'])
def deleteUser(request , pk):
    user = User.objects.get(id = pk)
    user.delete()
    return Response('user deleted successfully!')


#lawyer

@api_view(['GET'])
@parser_classes([JSONParser])
def showAllLawyers(request):
    fLawyers = Lawyer.objects.all()[:8]
    lawyers = Lawyer.objects.all()
    total_lawyers = lawyers.count()
    serializer = LawyersSerializer(fLawyers, many =True)
    return Response({
        'total_lawyers': total_lawyers,
        'lawyers': serializer.data,
    })

@api_view(['GET'])
@parser_classes([JSONParser])
def showAllLawyersPaginated(request,n):
    lawyers = Lawyer.objects.all()[8*(n-1):8+8*(n-1)]
    serializer = LawyersSerializer(lawyers, many =True)
    return Response(serializer.data)

class createLawyer(APIView):
    @parser_classes([JSONParser])
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            name = data.get('name')
            email = data.get('email')
            fname = data.get('fname')
            password = data.get('password')

            if name and email and password:
                # Hash the password before saving to the database
                hashed_password = urlsafe_base64_encode(str(password).encode('utf-8'))
                # Create the Lawyer instance
                lawyer = Lawyer.objects.create(name=name, email=email, password=hashed_password,fname= fname)


                response_data = {
                    'lawyer_id': lawyer.id,
                    'name': lawyer.name,
                    'email': lawyer.email,
                    # Include other user-related data as needed
                }

                return JsonResponse(response_data, status=201)
            else:
                return JsonResponse({'error': 'Name, email, and password are required'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)



#get lawyer with id
@api_view(['GET'])
@parser_classes([JSONParser])
def showLawyer(request,pk):
    p = int(urlsafe_base64_decode(pk))
    lawyer = Lawyer.objects.get(id =p)
    serializer = LawyerProfileSerializer(lawyer, many =False)
    return Response(serializer.data)


#delete lawyer with id
@api_view(['GET'])
def deleteLawyer(request , pk):
    p = str(urlsafe_base64_decode(pk))
    print(p)
    lawyer = Lawyer.objects.get(id = p[2:-1])
    lawyer.delete()

    return Response('lawyer deleted successfully!')


@api_view(['PUT'])
@parser_classes([JSONParser])
def updateLawyer(request, lawyer_id):
    try:
        lawyer = Lawyer.objects.get(id =lawyer_id)
    except Lawyer.DoesNotExist:
        return Response({'error': 'Lawyer not found'}, status=404)
    serializer = LawyerProfileSerializer(lawyer, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


#appointment

@api_view(['POST'])
def createAppointment(request):
    serializer = AppointmentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


#get all lawyer appointments
@api_view(['GET'])
def getLawyerAppointments(request, lawyer_id):
    try:
        p = str(urlsafe_base64_decode(lawyer_id))
        lawyer = Lawyer.objects.get(id=p[2:-1])
    except Lawyer.DoesNotExist:
        return Response({'error': 'Lawyer not found'}, status=404)

    appointments = Appointment.objects.filter(lawyer=lawyer)

    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)


#add a reservation
@api_view(['POST'])
def createReservation(request):
    try:
        user_id = request.data.get('user_id')
        lawyer_id = request.data.get('lawyer_id')
        date = request.data.get('date')
        time = request.data.get('time')
        details = request.data.get('details')

        user = User.objects.get(pk=user_id)
        lawyer = Lawyer.objects.get(pk=lawyer_id)

        reservation = Reservation.objects.create(
            user=user,
            lawyer=lawyer,
            date=date,
            time=time,
            details=details
        )

        serializer = ReservationSerializer(reservation)
        
        return Response(serializer.data, status=201)  # 201 Created
    except user.DoesNotExist:
        return Response({'error': 'user not found'}, status=404)
    except Lawyer.DoesNotExist:
        return Response({'error': 'Lawyer not found'}, status=404)
    except Exception as e:
        print(e)
        return Response({'error': 'Internal Server Error'}, status=500)
    
@api_view(['POST'])
def acceptReservation(request, reservation_id):
    try:
        
        reservation = Reservation.objects.get(pk=reservation_id)

        
        appointment = Appointment.objects.create(
            user=reservation.user,
            lawyer=reservation.lawyer,
            date=reservation.date,
            time=reservation.time,
            details=reservation.details
        )

        serializer = AppointmentSerializer(appointment)

        # Delete the accepted reservation
        reservation.delete()

        return Response(serializer.data, status=201)  # 201 Created
    except Reservation.DoesNotExist:
        return Response({'error': 'Reservation not found'}, status=404)
    except Exception as e:
        print(e)
        return Response({'error': 'Internal Server Error'}, status=500)


#delete the reservation

@api_view(['DELETE'])
def deleteReservation(request, reservation_id):
    try:
        reservation = Reservation.objects.get(pk=reservation_id)
        reservation.delete()
        return Response({'message': 'Reservation deleted successfully'}, status=204)  # 204 No Content
    except Reservation.DoesNotExist:
        return Response({'error': 'Reservation not found'}, status=404)
    except Exception as e:
        print(e)
        return Response({'error': 'Internal Server Error'}, status=500)
    

    


class LoginWithEmailAndPassword(APIView):
    @parser_classes([JSONParser])
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            email = data.get('email')
            password = data.get('password')
            
            if email and password:
                try:
                    lawyer = Lawyer.objects.get(email=email)
                except Lawyer.DoesNotExist:
                    lawyer = None
                p = str(urlsafe_base64_decode(lawyer.password))
                if lawyer and password== p[2:-1]:
                    # Authentication successful
                    hashed_token = urlsafe_base64_encode(str(lawyer.id).encode('utf-8'))
                    response_data = {
                        'auth_token': hashed_token,
                        'email': lawyer.email,
                        # Include other user-related data as needed
                    }
                    
                    response = Response(response_data)
                    response.set_cookie(key='auth_token', value=hashed_token,secure=True)
                    return response
                else:
                    # Authentication failed
                    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#comments

@api_view(['POST'])
def createComment(request):
    serializer = CommentSerializer(data=request.data)
    serializer2 = LawyerCommentSerializer(data=request.data+serializer.data)
    if serializer.is_valid() and serializer2.is_valid():
        serializer.save()
        serializer2.save()
        return Response(serializer.data+serializer2.data)
    return Response(serializer.errors, status=400)