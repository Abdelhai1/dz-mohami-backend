from rest_framework import serializers
from .models import Reservation, User
from .models import Lawyer
from .models import Appointment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email','address']
        #hna tqdr tshof kamel attribus t3 user tqdr tdir ('name','email')
        
class LawyerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Lawyer
        fields = ['id', 'user', 'number', 'specialization', 'experience_years']
        


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'user', 'lawyer', 'date', 'time', 'details']
        
class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'user', 'lawyer', 'date', 'time', 'details']
        
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)