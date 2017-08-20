from rest_framework import renderers
import json
import time
from io import StringIO
import csv


class FastaAdapterKitRenderer(renderers.BaseRenderer):
    media_type = 'application/x-fasta'
    format = 'fasta'
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        count = data['count']
        when = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        sbuf = StringIO()
        sbuf.write(';AdapterBase Fasta %d total results at %s\n' % (count, when))
        if data['next']:
            sbuf.write(';Next %s\n' % data['next'])
        if data['previous']:
            sbuf.write(';Previous %s\n' % data['previous'])
        for result in data['results']:
            sbuf.write('>oadb|%s;%s;%s;%s|%s\n' % (
                result['vendor'],
                result['kit'],
                result['subkit'],
                result['version'],
                result['barcode']
            ))
            sbuf.write(result['full_sequence']+'\n\n')
        return sbuf.getvalue().encode(self.charset)


class CSVAdapterKitRenderer(renderers.BaseRenderer):
    media_type = 'text/csv'
    format = 'csv'
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        sbuf = StringIO()
        writer = csv.writer(sbuf, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow((
            'Vendor', 
            'Kit',
            'Subkit',
            'Version',
            'Barcode',
            'Index Sequence',
            'Full Sequence',
        ))
        
        for result in data['results']:
            writer.writerow((
                result['vendor'],
                result['kit'],
                result['subkit'],
                result['version'],
                result['barcode'],
                result['index_sequence'],
                result['full_sequence']
            ))
        return sbuf.getvalue().encode(self.charset)
