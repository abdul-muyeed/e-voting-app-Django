from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from .models import Voter, Candidate, Poll

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action

from app.models import Voter, Candidate, Poll
from django.contrib.auth.models import User
from .serializers import UserSerializer, VoterSerializer, CandidateSerializer


# Create your views here.

def login(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("/")
        else:
            return HttpResponse("Login Failed")

    return render(request, "login.html")


def reg(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        print(username, email, password)
        data = User.objects.create_user(username, email, password)
        data.save()
        return HttpResponse("Data Saved")

    return render(request, "register.html")


def logout(request):
    if not request.user.is_authenticated:
        return redirect("login")

    auth_logout(request)
    return redirect("login")


@login_required
def home(request):
    voter = Voter.objects.filter(user=request.user).exists()
    if not voter:
        return render(request, "home.html")
    try:
        poll = Poll.objects.latest('updated_at')
    except ObjectDoesNotExist:
        poll = None

    try:
        candidate = Candidate.objects.all()
    except ObjectDoesNotExist:
        candidate = None



    voter = Voter.objects.get(user=request.user)
    data = {'fname': voter.first_name, 'lname': voter.last_name, 'nid': voter.nid, 'image': voter.image,
            'status': voter.status, 'email': request.user.email, 'voted': voter.voted,
            'poll_title': poll.title if poll else '', 'candidates': candidate}
    return render(request, "home.html", data)


def update(request):
    if request.method == "POST":
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        nid = request.POST.get("nid")
        image = request.FILES.get("image")
        print("username", username, "first_name", first_name, "last_name", last_name, "nid", nid,
              "image", image)
        # return HttpResponse("Data Updated")
        # return HttpResponse("Data Updated")
        user = User.objects.get(username=request.user)
        if user is not None:
            # image_ext = image.name.split(".")[-1]
            # image.name = f"{username}.{image_ext}"
            voter = Voter.objects.filter(user=request.user).exists()
            print(voter)
            if not voter:
                Voter.objects.create(user=request.user, first_name=first_name, last_name=last_name, nid=nid,
                                     image=image, status=True)
            else:
                voter = Voter.objects.get(user=user)
                Voter.objects.update(first_name=first_name, last_name=last_name, nid=nid, image=image)

        return HttpResponse("Data Updated")
    voter = Voter.objects.filter(user=request.user).exists()
    if voter is False:
        return render(request, "update.html")
    voter = Voter.objects.get(user=request.user)
    data = {'username': request.user.username, 'fname': voter.first_name, 'lname': voter.last_name, 'nid': voter.nid,
            'image': voter.image, 'status': voter.status, 'email': request.user.email}

    return render(request, "update.html", data)


def vote(request, candidate_id):
    try:
        candidate = Candidate.objects.get(id=candidate_id)
        voter = Voter.objects.get(user=request.user)
    except Candidate.DoesNotExist:
        return HttpResponse("Candidate does not exist", status=404)

    voter.voted = True
    voter.save()
    # Increment the vote count by 1
    candidate.votes += 1
    candidate.save()

    return redirect("/")


# API

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['get'])
    def get_user(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user)
            return JsonResponse(serializer.data)
        except User.DoesNotExist:
            return HttpResponse(status=404)

        pass


class VoterViewSet(viewsets.ModelViewSet):
    queryset = Voter.objects.all()
    serializer_class = VoterSerializer

    @action(detail=True, methods=['get'])
    def get_voter(self, request, pk=None):
        try:
            voter = Voter.objects.get(pk=pk)
            serializer = VoterSerializer(voter)
            return JsonResponse(serializer.data)
        except Voter.DoesNotExist:
            return HttpResponse(status=404)

        pass


class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

    @action(detail=True, methods=['get'])
    def get_candidate(self, request, pk=None):
        try:
            candidate = Candidate.objects.get(pk=pk)
            serializer = CandidateSerializer(candidate)
            return JsonResponse(serializer.data)
        except Candidate.DoesNotExist:
            return HttpResponse(status=404)

        pass
