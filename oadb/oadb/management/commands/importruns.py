from django.core.management.base import BaseCommand, CommandError
import csv
from oadb.models import User, Kit, Adaptor
import re


class Command(BaseCommand):
    help = 'Imports kits and adapters from a CSV'

    def add_arguments(self, parser):
        parser.add_argument('csvfile', type=str,
                            help='Path to CSV file on the filesystem')
        parser.add_argument('--username', metavar='NAME', type=str, default=None,
                            help='Specify a user name for imported kits')
        parser.add_argument('--userid', metavar='ID', type=int, default=None,
                            help='Specify a user identifier for imported kits')

    def handle(self, *args, **opts):

        user = None
        if opts['username'] is not None:
            user = User.objects.get(username=opts['username'])
        elif opts['userid'] is not None:
            user = User.objects.get(id=opts['userid'])
        else:
            raise CommandError('Either username or userid is required')

        with open(opts['csvfile'], 'r') as f:
            kitreader = csv.reader(f, delimiter=',', quotechar='"')
            rowcount = 0
            for row in kitreader:
                if rowcount > 0:
                    kitname = re.sub('_', ' ', row[0]).strip()
                    try:
                        kit = Kit.objects.get(name=kitname)
                    except Kit.DoesNotExist:
                        kit = Kit.objects.create(name=kitname, user_id=user.id)
                    Adaptor.objects.create(
                        barcode=row[1],
                        sequence=row[2],
                        kit_id=kit.id,
                        user_id=user.id,
                    )
                    print(', '.join(row))
                rowcount += 1
