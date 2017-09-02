from collections import OrderedDict
from rest_framework.metadata import BaseMetadata


class OpenAPIMetadata(BaseMetadata):

    def determine_metadata(self, request, view):
        metadata = OrderedDict()
        metadata['swagger'] = '2.0'
        metadata['info'] = OrderedDict()
        metadata['info']['title'] = view.get_view_name()
        metadata['info']['description'] = view.get_view_description()
        metadata['info']['version'] = ''
        metadata['produces'] = [parser.media_type for parser in view.parser_classes]
        metadata['consumes'] = [renderer.media_type for renderer in view.renderer_classes]
        if hasattr('view', 'get_serializer'):
            paths = self.determine_paths(request, view)
            if paths:
                metadata['paths'] = paths
        return metadata

    def determine_paths(self, request, view):
        paths = {}
        for method in {'PUT', 'POST'} & set(view.allowed_methods):
            paths[request.path] = {}
            paths[request.path][method] = {}
        return paths
