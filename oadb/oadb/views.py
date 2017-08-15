from django.shortcuts import render
from django.contrib.auth.models import User, Group 
from .serializers import *
from rest_framework import viewsets
#from rest_framework.views import APIView
#from rest_framework.schemas import SchemaGenerator
#from rest_framework.permissions import AllowAny
#from rest_framework.response import Response
#from rest_framework_swagger import renderers
from .models import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer


class AdaptorViewSet(viewsets.ModelViewSet):
    queryset = Adaptor.objects.all()
    serializer_class = AdaptorSerializer


class KitViewSet(viewsets.ModelViewSet):
    queryset = Kit.objects.all()
    serializer_class = KitSerializer


class DatabaseViewSet(viewsets.ModelViewSet):
    queryset = Database.objects.all()
    serializer_class = DatabaseSerializer


class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.all()
    serializer_class = RunSerializer


# Swagger not here yet...
#
#class OpenAPIView(APIView):
#    """
#    Render the API swagger.json
#    """
#    permission_classes = (AllowAny,)
#    render_classes = (renderers.OpenAPIRenderer,)
#
#    def get(self, request):
#        generator = SchemaGenerator()
#        return Response(generator.get_schema(request))

