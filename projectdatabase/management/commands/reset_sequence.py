# your_app/management/commands/reset_sequence.py

from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Resets the sequence of the specified table to the current max ID'

    def add_arguments(self, parser):
        parser.add_argument('table', type=str, help='The name of the table to reset the sequence for')

    def handle(self, *args, **kwargs):
        table = kwargs['table']
        with connection.cursor() as cursor:
            cursor.execute(f"""
                SELECT setval(
                    pg_get_serial_sequence('{table}', 'id'),
                    coalesce((SELECT MAX(id) FROM {table}), 1),
                    false
                )
            """)
            self.stdout.write(self.style.SUCCESS(f'Successfully reset sequence for {table}'))
