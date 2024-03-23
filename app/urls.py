from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from django.urls import path, include
from . import views

from .views import UserViewSet, VoterViewSet, CandidateViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'voters', VoterViewSet)
router.register(r'candidates', CandidateViewSet)


urlpatterns = [
    path("login/", views.login, name="login"),
    path("register/", views.reg, name="reg"),
    path("logout/", views.logout, name="logout"),
    path("", views.home, name="home"),
    path("update", views.update, name="update"),
    path("vote/<candidate_id>/", views.vote, name="vote"),
    path("api/", include(router.urls)),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
