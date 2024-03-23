from rest_framework import serializers
from app.models import Voter, Candidate, Poll
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class VoterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voter
        fields = "__all__"

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = "__all__"