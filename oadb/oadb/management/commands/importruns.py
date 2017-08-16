from django.core.management.base import BaseCommand, CommandError
import csv
from oadb.models import User, Kit, Adapter, Run, Database
import sys
from collections import namedtuple


CSV_COLUMNS = [
    'accession',
    'username',
    'database',
    'is_public',
    'five_prime',
    'three_prime',
    'platform',
]

CSV_COLUMN_ALIASES = {
    'owner': 'username',
    "5' adapter": 'five_prime',
    "3' adapter": 'three_prime',
}

CSV_BOOL_VALUES = {
    'yes': True,
    'no': False,
    'true': True,
    'false': False,
    't': True,
    '0': False,
    '1': True
}

RowData = namedtuple('RowData', CSV_COLUMNS)


class Command(BaseCommand):
    help = 'Imports kits and adapters from a CSV'

    def add_arguments(self, parser):
        parser.add_argument('csvfile', type=str,
                            help='Path to CSV file on the filesystem')
        parser.add_argument('--username', metavar='NAME', type=str, default=None,
                            help='Specify a user name for imported kits')
        parser.add_argument('--userid', metavar='ID', type=int, default=None,
                            help='Specify a user identifier for imported kits')
        parser.add_argument('--clear', action='store_true', default=False,
                            help='Clear database before submitting information')

    def build_header_map(self, rawrow):
        self.name2col = {}
        for i in range(0, len(rawrow)):
            colname = rawrow[i].lower()
            if colname in CSV_COLUMN_ALIASES:
                colname = CSV_COLUMN_ALIASES[colname]
            if colname not in CSV_COLUMNS:
                raise CommandError('%s: invalid column name' % colname)
            self.name2col[colname] = i
        if len(self.name2col.keys()) != len(CSV_COLUMNS):
            raise CommandError('csv is missing required columns')

    def parse_bool(self, dataval):
        v = dataval.strip().lower()
        if v not in CSV_BOOL_VALUES:
            raise CommandError('line %d: %s: incorrect boolean data')
        return CSV_BOOL_VALUES[v]

    def build_row_data(self, rawrow):
        if len(rawrow) < len(self.name2col):
            raise CommandError('line %d: too few columns' % self.rowcount)

        row = RowData(
            accession=rawrow[self.name2col['accession']],
            username=rawrow[self.name2col['username']],
            database=rawrow[self.name2col['database']],
            is_public=self.parse_bool(rawrow[self.name2col['is_public']]),
            five_prime=rawrow[self.name2col['five_prime']],
            three_prime=rawrow[self.name2col['three_prime']],
            platform=rawrow[self.name2col['platform']],
        )
        return row

    def import_csv(self, user, csvfile):
        kitreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        self.rowcount = 0
        self.nruns = 0
        for rawrow in kitreader:
            if self.rowcount == 0:
                self.build_header_map(rawrow)
            else:
                row = self.build_row_data(rawrow)
                three = None
                five = None
                database = None
                try:
                    three = Adapter.objects.get(
                        kit=row.five_prime,
                        version='').id
                    five = Adapter.objects.get(
                        kit=row.three_prime,
                        version='').id
                except Kit.DoesNotExist:
                    sys.stderr.write('line %d: unable to locate kits' % self.rowcount)

                try:
                    database = Adapter.objects.get(name=row.database)
                except:
                    sys.stderr.write('line %d: unable to locate database' % self.rowcount)

                Run.objects.create(
                    accession=row.accession,
                    database_id=database.id,
                    is_public=row.is_public,
                    user_id=user.id,
                    three_prime_id=three,
                    five_prime_id=five,
                    sequencing_instrument=row.platform,
                )

                printable_row = row[0:2] + row[4:]
                print(', '.join(printable_row))
            self.rowcount += 1

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

        with open(opts['csvfile'], 'r') as f:
            self.import_csv(user, f)
