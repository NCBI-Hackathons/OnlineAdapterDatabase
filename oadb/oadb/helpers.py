from rest_framework import renderers
from rest_framework import pagination
import json
import time
from io import StringIO
import csv


class FastaAdapterKitRenderer(renderers.BaseRenderer):
    media_type = 'application/x-fasta'
    format = 'fasta'
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        when = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        sbuf = StringIO()
        sbuf.write(';AdapterBase Fasta results at %s\n' % when)
        sbuf.write(';Sequence format: oadb|<vendor>;<kit>;<subkit>;<version>|<barcode>\n')
        for result in data:
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
        
        for result in data:
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


