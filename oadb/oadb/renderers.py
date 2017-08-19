from rest_framework.renderers import BaseRenderer


class FastaRenderer(renderers.BaseRenderer):
    media_type = 'application/x-fasta'
    format = 'fna'
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        # what to do with this "data" - probably a JSON array
        return data


class CSVRenderer(renderers.BaseRenderer):
    media_type = 'text/csv'
    format = 'csv'
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        # what to do with this "data" - probably a JSON array
        return data

