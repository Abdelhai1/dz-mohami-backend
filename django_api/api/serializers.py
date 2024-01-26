from rest_framework import serializers
from .models import Comment, Reservation, User
from .models import Lawyer
from .models import Appointment
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email']
        #hna tqdr tshof kamel attribus t3 user tqdr tdir ('name','email')
        

class LawyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lawyer
        fields = ['id', 'name','fname','email','password']


    def create(self, validated_data):
        # Hash the password before saving
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class LawyerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lawyer
        fields = ['id', 'name','fname','email','password','address','wilaya','latitude','longitude','rating','avocat_image','phone','description','social','experience_years']


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
    
class CommentSerializer(serializers.Serializer):
    class Meta:
        model = Comment
        fields = ['id','user_name','text','rate']
        
class LawyerCommentSerializer(serializers.Serializer):
    class Meta:
        model = Comment
        fields = ['id','lawyer','comment']