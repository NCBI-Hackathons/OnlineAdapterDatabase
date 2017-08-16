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
from collections import OrderedDict


User = get_user_model()


class HomeView(TemplateView):
    template_name = 'oadb/index.html'


@permission_classes((IsAdminUser, ))
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = serializers.UserSerializer

@permission_classes((IsAuthenticatedOrReadOnly, ))
class AdapterViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = Adapter.objects.all()
        pk = self.request.query_params.get('kit_id', '')
        name = self.request.query_params.get('kit', '')
        barcode = self.request.query_params.get('barcode', '')
        index_type = self.request.query_params.get('index_type', '')
        un_seq = self.request.query_params.get('universal_sequence', '')

        if pk:
            queryset.filter(kit_id=pk)
        if name:
            queryset.filter(kit=name)
        if barcode:
            queryset.filter(barcode=barcode)
        if index_type:
            queryset.filter(index_type=index_type)
        if un_seq:
            queryset.filter(universal_sequence=un_seq) 
        
        return queryset
    serializer_class = serializers.AdapterSerializer

@permission_classes((IsAuthenticatedOrReadOnly, ))
class KitViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.KitSerializer

    def get_queryset(self):
        queryset = Kit.objects.all()

        kit = self.request.query_params.get('kit', '')
        subkit = self.request.query_params.get('subkit', '')
        vendor = self.request.query_params.get('vendor', '')

        if kit:
            queryset = queryset.filter(kit=kit)
        if subkit:
            queryset = queryset.filter(subkit=subkit)
        if vendor:
            vendor = queryset.filter(vendor=vendor)

        return queryset


@permission_classes((IsAuthenticatedOrReadOnly, ))
class DatabaseViewSet(viewsets.ModelViewSet):
    queryset = Database.objects.all()
    serializer_class = serializers.DatabaseSerializer

@permission_classes((IsAuthenticatedOrReadOnly, ))
class RunViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = Run.objects.all()
        accession_id = self.request.query_params.get('accession_id', '')
        accession = self.request.query_params.get('accession', '')
        if accession_id:
            queryset = queryset.filter(three_prime_id=accession_id) | queryset.filter(five_prime_id=accession_id)
        if accession:
            queryset.filter(accession=accession)
        return queryset
    serializer_class = serializers.RunSerializer
