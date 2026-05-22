import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from db.connection import connect

BASE_DIR = os.path.dirname(__file__)


def run_sql_file(cursor, filename):
    path = os.path.join(BASE_DIR, filename)
    with open(path, "r", encoding="utf-8") as file:
        cursor.execute(file.read())


def main():
    connection = connect()
    connection.autocommit = True
    try:
        with connection.cursor() as cursor:
            run_sql_file(cursor, "schema.sql")
            run_sql_file(cursor, "seed.sql")
        print("Base de datos inicializada correctamente.")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
