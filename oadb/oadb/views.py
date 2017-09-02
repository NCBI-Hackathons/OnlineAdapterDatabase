from django.contrib.auth import get_user_model
from django.views.generic import TemplateView
from . import serializers
from .models import Adapter, AdapterKit, Kit, Database, Run
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.decorators import permission_classes
from rest_framework import viewsets, renderers, response, schemas
from django_filters import rest_framework as filters
from openapi_codec import OpenAPICodec
from .metadata import OpenAPIMetadata


from . import helpers


User = get_user_model()

generator = schemas.SchemaGenerator(title='AdapterBase API')


class HomeView(TemplateView):
    template_name = 'oadb/index.html'


class AdminView(TemplateView):
    template_name = 'oadb/admin.html'


class CustomOpenAPIRenderer(renderers.BaseRenderer):
    """
    An OpenAPI renderer that depends only on openapi_codec rather than on django-rest-swagger
    """
    media_type = 'application/openapi+json'
    format = 'openapi'

    def render(self, data, media_type=None, renderer_context=None):
        codec = OpenAPICodec()
        return codec.encode(data)


class SchemaViewSet(viewsets.ViewSet):
    """
    Return the schema in OpenAPI format
    """
    base_name = 'schema'
    renderer_classes = [CustomOpenAPIRenderer, renderers.JSONRenderer, renderers.BrowsableAPIRenderer]

    def list(self, request, format=None):
        schema = generator.get_schema()
        return response.Response(schema)


@permission_classes((IsAdminUser, ))
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('username', 'email',)


#@permission_classes((IsAuthenticatedOrReadOnly, ))
class AdapterViewSet(viewsets.ModelViewSet):
    queryset = Adapter.objects.all()
    serializer_class = serializers.AdapterSerializer
    metadata_class = OpenAPIMetadata
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('barcode', 'index_sequence',)


class KitAdapterViewSet(viewsets.ModelViewSet):
    queryset = Kit.objects.all().prefetch_related('adapters')
    serializer_class = serializers.KitAdapterSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    metedata_class = OpenAPIMetadata
    field_fields = ('id', 'vendor', 'kit', 'subkit',)


class DownloadViewSet(viewsets.ReadOnlyModelViewSet):
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
            return super().paginator

    def finalize_response(self, req, resp, *args, **kwargs):
        resp = super().finalize_response(req, resp, *args, **kwargs)
        if resp.accepted_renderer.format == 'fasta':
            resp['content-disposition'] = 'attachment; filename=adapterkits.fasta'
        elif resp.accepted_renderer.format == 'csv':
            resp['content-disposition'] = 'attachment; filename=adapterkits.csv'
        return resp


#@permission_classes((IsAuthenticatedOrReadOnly, ))
class KitViewSet(viewsets.ModelViewSet):
    queryset = Kit.objects.all()
    serializer_class = serializers.KitSerializer
    metadata_class = OpenAPIMetadata
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
