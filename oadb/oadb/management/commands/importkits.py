from django.core.management.base import BaseCommand, CommandError
import csv
from oadb.models import User, Kit, Adapter, Run
import re
from collections import namedtuple

CSV_COLUMNS = [
    'kit', 'subkit', 'barcode',
    'index_seq', 'index',
    'adapter_seq', 'version',
    'manufacturer', 'model_range', 'status'
]

RowData = namedtuple('RowData', CSV_COLUMNS)


class Command(BaseCommand):
    help = 'Imports kits and adapters from a CSV'
    output_transaction = True

    def add_arguments(self, parser):
        parser.add_argument('csvfile', type=str,
                            help='Path to CSV file on the filesystem')
        parser.add_argument('--username', metavar='NAME', type=str, default=None,
                            help='Specify a user name for imported kits')
        parser.add_argument('--userid', metavar='ID', type=int, default=None,
                            help='Specify a user identifier for imported kits')
        parser.add_argument('--format', metavar='FORMAT', default='scott',
                            choices=['scott', 'chaim'],
                            help='Specify format of input CSV')
        parser.add_argument('--clear', action='store_true', default=False,
                            help='Clear database before submitting information')

    def build_header_map(self, rawrow):
        self.name2col = {}
        for i in range(0, len(rawrow)):
            colname = rawrow[i]
            if colname not in CSV_COLUMNS:
                raise CommandError('%s: invalid column name' % colname)
            self.name2col[colname] = i
        if len(self.name2col.keys()) != len(CSV_COLUMNS):
            raise CommandError('csv is missing required columns')

    def build_row_data(self, rawrow):
        if len(rawrow) < len(self.name2col):
            raise CommandError('line %d: too few columns' % self.rowcount)
        statusval = rawrow[self.name2col['status']]
        if len(statusval) == 0:
            statusval = '0'
        row = RowData(
            kit=re.sub('_', ' ', rawrow[self.name2col['kit']]).strip(),
            subkit=re.sub('_', ' ', rawrow[self.name2col['subkit']]).strip(),
            barcode=rawrow[self.name2col['barcode']],
            index_seq=rawrow[self.name2col['index_seq']],
            index=rawrow[self.name2col['index']],
            adapter_seq=rawrow[self.name2col['adapter_seq']],
            version=rawrow[self.name2col['version']],
            manufacturer=rawrow[self.name2col['manufacturer']],
            model_range=rawrow[self.name2col['model_range']],
            status=statusval,
        )
        return row

    def import_csv(self, user, csvfile):
        kitreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        self.rowcount = 0
        self.nkits = 0
        self.nadapters = 0
        self.kit2useq = {}
        for rawrow in kitreader:
            if self.rowcount == 0:
                self.build_header_map(rawrow)
            else:
                row = self.build_row_data(rawrow)
                # kit = re.sub('_', ' ', row.kit).strip()
                # subkit = re.sub('_', ' ', row.subkit).strip()
                try:
                    kit = Kit.objects.get(
                        vendor=row.manufacturer,
                        kit=row.kit,
                        subkit=row.subkit,
                        version=row.version)
                except Kit.DoesNotExist:
                    kit = Kit.objects.create(
                        vendor=row.manufacturer,
                        kit=row.kit,
                        subkit=row.subkit,
                        version=row.version,
                        status=int(row.status),
                        user_id=user.id,
                    )
                    self.nkits += 1
                if row.barcode == 'universal':
                    self.kit2useq[kit.id] = row.index_seq
                else:
                    Adapter.objects.create(
                        barcode=row.barcode,
                        index_sequence=row.index_seq,
                        index_type=row.index,
                        full_sequence=row.adapter_seq,
                        kit_id=kit.id,
                        user_id=user.id,
                    )
                    self.nadapters += 1
                print(', '.join(row))
            self.rowcount += 1
        # Update all objects with the universal sequence
        for kit, universal_seq in self.kit2useq.items():
            Adapter.objects.filter(kit_id=kit).update(
                universal_sequence=universal_seq
            )

    def import_chaim_csv(self, user, csvfile):
        kitreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        self.rowcount = 0
        self.nkits = 0
        self.nadapters = 0
        for rawrow in kitreader:
            oldname, fullseq = rawrow
            vendor = 'illumina'
            status = 3
            try:
                kit = Kit.objects.get(
                    vendor=vendor,
                    kit=oldname,
                    subkit='',
                    version='')
            except Kit.DoesNotExist:
                kit = Kit.objects.create(
                    vendor=vendor,
                    kit=oldname,
                    subkit='',
                    version='',
                    user_id=user.id)
                self.nkits += 1
            Adapter.objects.create(
                barcode=oldname,
                index_sequence='',
                index_type='i5',
                full_sequence=fullseq,
                kit_id=kit.id,
                user_id=user.id,
            )
            self.nadapters += 1
            self.rowcount += 1
            print(', '.join(rawrow))
        print('Imported %d kits and %d adapters' % (self.nkits, self.nadapters))

    def handle(self, *args, **opts):

        user = None
        if opts['username'] is not None:
            user = User.objects.get(username=opts['username'])
        elif opts['userid'] is not None:
            user = User.objects.get(id=opts['userid'])
        else:
            raise CommandError('Either username or userid is required')

        if opts['clear']:
            Run.objects.all().delete()
            Adapter.objects.all().delete()
            Kit.objects.all().delete()

        with open(opts['csvfile'], 'r') as f:
            if opts['format'] == 'chaim':
                self.import_chaim_csv(user, f)
            else:
                self.import_csv(user, f)
