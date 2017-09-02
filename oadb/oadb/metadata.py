from collections import OrderedDict
from rest_framework.metadata import SimpleMetadata


class OpenAPIMetadata(SimpleMetadata):

    def mutate_parameters(self, params):
        for name, props in params.items():
            if 'label' in props:
                props['title'] = props.pop('label')
            if 'required' in props:
                props.pop('required')
            if 'min_legnth' in props:
                props['minLength'] = props.pop('min_length')
            if 'max_length' in props:
                props['maxLength'] = props.pop('max_length')
            if props['type'] == 'choice':
                choices = props.pop('choices')
                types = list(set(type(c['value']) for c in choices))
                if len(types) == 1:
                    if types[0] == str:
                        props['type'] = 'string'
                    elif types[0] == int:
                        props['type'] = 'integer'
                props['enum'] = [c['value'] for c in choices]
                if 'default' not in props:
                    props['default'] = props['enum'][0]

    def required_parameters(self, params):
        return [name for name, props in params.items() if props.get('required', False)]

    def determine_metadata(self, request, view):
        drf = super().determine_metadata(request, view)
        openapi = OrderedDict()
        openapi['title'] = drf['name']
        openapi['type'] = 'object'
        params = drf['actions']['POST']
        openapi['required'] = self.required_parameters(params)
        self.mutate_parameters(params)
        openapi['properties'] = params
        return openapi
