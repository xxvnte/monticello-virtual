from db.connection import get_connection
from db.password_hasher import hash_password, verify_password


class AuthRepository:
    def login(self, email, password):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id_usuario, nombre, apellido, correo, rol, activo, password_hash
                    FROM usuarios
                    WHERE correo = %s
                    """,
                    (email,),
                )
                user = cur.fetchone()
                if not user or not verify_password(password, user["password_hash"]):
                    return None
                return {
                    "id_usuario": user["id_usuario"],
                    "nombre": user["nombre"],
                    "apellido": user["apellido"],
                    "correo": user["correo"],
                    "rol": user["rol"],
                    "activo": user["activo"],
                }

    def register(self, rut, nombre, apellido, email, password):
        password_digest = hash_password(password)
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO usuarios (rut, nombre, apellido, correo, password_hash)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id_usuario, nombre, apellido, correo, rol
                    """,
                    (rut, nombre, apellido, email, password_digest),
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
