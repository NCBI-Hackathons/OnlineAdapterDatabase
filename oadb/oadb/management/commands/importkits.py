from django.core.management.base import BaseCommand, CommandError
import csv
from oadb.models import Kit, Adaptor


class Command(BaseCommand):
    help = 'Imports kits and adapters from a CSV'

    def add_arguments(self, parser):
        parser.add_argument('csvfile', type=str,
                            help='Path to CSV file on the filesystem')

    def handle(self, *args, **opts):

        if 'csvfile' not in opts:
            raise CommandError('the csvfile is required')

        with open(opts['csvfile'], 'r') as f:
            kitreader = csv.reader(f, delimiter=',', quotechar='"')
            for row in kitreader:
                print(', '.join(row))
