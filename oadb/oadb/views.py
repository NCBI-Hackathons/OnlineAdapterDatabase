from django.contrib.auth import get_user_model
from django.views.generic import TemplateView
from . import serializers
from rest_framework import viewsets
# from rest_framework.views import APIView
# from rest_framework.schemas import SchemaGenerator
# from rest_framework.permissions import AllowAny
# from rest_framework.response import Response
# from rest_framework_swagger import renderers
from .models import Adapter, Kit, Database, Run
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.decorators import permission_classes
from django_filters import rest_framework as filters
from collections import OrderedDict


User = get_user_model()


class HomeView(TemplateView):
    template_name = 'oadb/index.html'


@permission_classes((IsAdminUser, ))
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('username', 'email',)


@permission_classes((IsAuthenticatedOrReadOnly, ))
class AdapterViewSet(viewsets.ModelViewSet):
    queryset = Adapter.objects.all()
    serializer_class = serializers.AdapterSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('barcode', 'index_sequence',)


@permission_classes((IsAuthenticatedOrReadOnly, ))
class AdapterKitViewSet(viewsets.ModelViewSet):
    queryset = Adapter.objects.select_related('kit').all()
    serializer_class = serializers.AdapterKitSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('barcode', 'index_sequence',)


@permission_classes((IsAuthenticatedOrReadOnly, ))
class KitViewSet(viewsets.ModelViewSet):
    queryset = Kit.objects.all()
    serializer_class = serializers.KitSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('vendor', 'kit', 'subkit',)


@permission_classes((IsAuthenticatedOrReadOnly, ))
class DatabaseViewSet(viewsets.ModelViewSet):
    queryset = Database.objects.all()
    serializer_class = serializers.DatabaseSerializer


@permission_classes((IsAuthenticatedOrReadOnly, ))
class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.all()
    serializer_class = serializers.RunSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('accession',)


@permission_classes((IsAuthenticatedOrReadOnly, ))
class RunAdapterViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.select_related('three_prime').select_related('five_prime').all()
    serializer_class = serializers.RunAdapterSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('accession',)
