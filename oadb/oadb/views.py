from django.contrib.auth import get_user_model
from django.views.generic import TemplateView
from . import serializers
from rest_framework import viewsets
from .models import Adapter, AdapterKit, Kit, Database, Run
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.decorators import permission_classes
from rest_framework import renderers
from django_filters import rest_framework as filters
from collections import OrderedDict

from . import helpers


User = get_user_model()


class HomeView(TemplateView):
    template_name = 'oadb/index.html'


class AdminView(TemplateView):
    template_name = 'oadb/admin.html'


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


class AdapterKitViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AdapterKit.objects.all()
    serializer_class = serializers.AdapterKitFlatSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('vendor', 'kit', 'subkit', 'barcode', 'version', 'index_type')

    renderer_classes = (
        renderers.JSONRenderer,
        helpers.CSVAdapterKitRenderer,
        helpers.FastaAdapterKitRenderer,
        renderers.BrowsableAPIRenderer
    )

    @property
    def paginator(self):
        renderer = self.request.accepted_renderer
        if renderer.format=='fasta' or renderer.format=='csv':
            return None
        else:
            return super(AdapterKitViewSet, self).paginator

    def finalize_response(self, req, resp, *args, **kwargs):
        resp = super(AdapterKitViewSet, self).finalize_response(req, resp, *args, **kwargs)
        if resp.accepted_renderer.format == 'fasta':
            resp['content-disposition'] = 'attachment; filename=adapterkits.fasta'
        elif resp.accepted_renderer.format == 'csv':
            resp['content-disposition'] = 'attachment; filename=adapterkits.csv'
        return resp


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
