from db.connection import get_connection


class AuthRepository:
    def login(self, email, password):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id_usuario, nombre, apellido, correo, rol, activo
                    FROM usuarios
                    WHERE correo = %s AND password_hash = %s
                    """,
                    (email, password),
                )
                return cur.fetchone()

    def register(self, rut, nombre, apellido, email, password):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO usuarios (rut, nombre, apellido, correo, password_hash)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id_usuario, nombre, apellido, correo, rol
                    """,
                    (rut, nombre, apellido, email, password),
                )
                user = cur.fetchone()
                cur.execute(
                    """
                    INSERT INTO billeteras (id_usuario, saldo)
                    VALUES (%s, 0.00)
                    RETURNING id_billetera
                    """,
                    (user["id_usuario"],),
                )
                wallet = cur.fetchone()
                conn.commit()
                return user, wallet["id_billetera"]
