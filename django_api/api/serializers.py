from rest_framework import serializers
from .models import Comment, Reservation, User
from .models import Lawyer
from .models import Appointment



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','activated']
        #hna tqdr tshof kamel attribus t3 user tqdr tdir ('name','email')
        

class LawyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lawyer
        fields = ['id', 'name','fname','email','avocat_image','rating']

class LawyersWilayaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lawyer
        fields = ['id', 'name','fname','email','password','avocat_image','rating','wilaya']

class CitySerializer(serializers.Serializer):
    wilaya = serializers.CharField()

class MainScreenSerializer(serializers.Serializer):
    email = serializers.CharField()
    id = serializers.IntegerField()
    name = serializers.CharField()
    activated = serializers.BooleanField()
    
class LawyerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lawyer
        fields = ['id', 'name','fname','email','password','address','wilaya','latitude','longitude','rating','avocat_image','phone','description','social','experience_years','activated']

class LawyersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lawyer
        fields = ['id', 'name','fname','rating','avocat_image','description']


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'user', 'lawyer', 'date', 'time', 'details']
        
class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'user', 'appointment','lawyer', 'details']
        
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
class CommentSerializer(serializers.Serializer):
    class Meta:
        model = Comment
        fields = ['id','user','text','lawyer','rate']
    def create(self, validated_data):
        return Comment.objects.create(**validated_data)