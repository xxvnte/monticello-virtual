import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from db.connection import connect


def main():
    connection = connect()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT NOW() AS server_time")
            row = cursor.fetchone()
        print("Conexion a la base de datos exitosa.")
        print(f'Hora del servidor: {row["server_time"]}')
    except Exception as error:
        print(f"Error al conectar a la base de datos: {error}")
        raise
    finally:
        connection.close()


if __name__ == "__main__":
    main()
