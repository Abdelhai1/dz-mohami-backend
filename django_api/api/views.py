from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import AppointmentSerializer, LoginSerializer, ReservationSerializer, UserSerializer,LawyerSerializer
from .models import Reservation, User,Lawyer,Appointment
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
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

#delete the user
@api_view(['GET'])
def deleteUser(request , pk):
    user = User.objects.get(id = pk)
    user.delete()
    return Response('user deleted successfully!')


#t3 l avocat

@api_view(['GET'])
def showAllLawyers(request):
    lawyers = Lawyer.objects.all()
    serializer = LawyerSerializer(lawyers, many =True)
    return Response(serializer.data)

@api_view(['POST'])
def createLawyer(request):
    serializer = LawyerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['GET'])
def deleteLawyer(request , pk):
    
    lawyer = Lawyer.objects.get(id = pk)
    user = User.objects.get(id = lawyer.id)
    lawyer.delete()
    user.delete()
    return Response('lawyer deleted successfully!')


@api_view(['PUT'])
def updateLawyer(request, lawyer_id):
    try:
        lawyer = Lawyer.objects.get(pk=lawyer_id)
    except Lawyer.DoesNotExist:
        return Response({'error': 'Lawyer not found'}, status=404)

    serializer = LawyerSerializer(lawyer, data=request.data, partial=True)
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
        lawyer = Lawyer.objects.get(pk=lawyer_id)
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
    
    
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        # Authenticate the user
        user = authenticate(request, email=email, password=password)

        if user:
            # User is authenticated, create or get the token
            token, created = Token.objects.get_or_create(user=user)

            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)