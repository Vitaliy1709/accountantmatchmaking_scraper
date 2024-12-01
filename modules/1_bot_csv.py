"""
    Загружает все посткоды в базу данных
"""

import csv
from django.db import IntegrityError

from load_django import *
from parser_app.models import *


file_path = "./../files/australian_postcodes.csv"

try:
    with open(file_path, mode="r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        added_count = 0
        skipped_count = 0

        for row in reader:
            postcode = row.get("postcode")
            city = row.get("suburb")
            state = row.get("state")


            if not postcode or not city or not state:
                print(f"Пропущена строка из-за отсутствия данных: {row}")
                skipped_count += 1
                continue

            try:
                location, created = Location.objects.get_or_create(
                    postcode=postcode,
                    city=city,
                    state=state,
                    defaults={"status": "Done"},
                )
                if created:
                    added_count += 1
            except IntegrityError as e:
                print(f"Ошибка при добавлении записи {row}: {e}")
                skipped_count += 1

        print(f"Успешно добавлено {added_count} записей.")
        print(f"Пропущено {skipped_count} строк.")

except FileNotFoundError:
    print("CSV файл не найден. Проверьте путь.")
except Exception as e:
    print(f"Произошла ошибка: {e}")