# Django automatically looks for any customized commands inside this folder
# the file name indicates the name of the customized commands
import os
from pathlib import Path

from django.core.management import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help ="Populates the database with collections and products"

    def handle(self, *args, **options):
        print("Populating the database...")
        cur_dir = os.path.dirname(__file__)
        file_path = os.path.join(cur_dir, 'seed.sql')
        sql = Path(file_path).read_text()
        with connection.cursor() as cursor:
            cursor.execute(sql)
