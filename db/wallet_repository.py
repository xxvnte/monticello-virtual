from db.connection import get_connection


class WalletRepository:
    def get_wallet(self, user_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT b.id_billetera, b.saldo, b.moneda, u.activo
                    FROM billeteras b
                    JOIN usuarios u ON u.id_usuario = b.id_usuario
                    WHERE b.id_usuario = %s
                    """,
                    (user_id,),
                )
                return cur.fetchone()

    def apply_movement(self, user_id, movement_type, amount):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT b.id_billetera, b.saldo, b.moneda, u.activo
                    FROM billeteras b
                    JOIN usuarios u ON u.id_usuario = b.id_usuario
                    WHERE b.id_usuario = %s
                    FOR UPDATE
                    """,
                    (user_id,),
                )
                wallet = cur.fetchone()
                if not wallet or not wallet["activo"]:
                    raise ValueError("Usuario no encontrado o inactivo")
                balance = float(wallet["saldo"])
                if movement_type == "retiro" and balance < amount:
                    raise ValueError("Saldo insuficiente")
                if amount <= 0:
                    raise ValueError("El monto debe ser mayor a cero")
                if movement_type == "deposito":
                    new_balance = balance + amount
                    description = "Deposito en billetera"
                else:
                    new_balance = balance - amount
                    description = "Retiro de billetera"
                cur.execute(
                    """
                    UPDATE billeteras SET saldo = %s WHERE id_billetera = %s
                    """,
                    (new_balance, wallet["id_billetera"]),
                )
                cur.execute(
                    """
                    INSERT INTO transacciones (
                        id_billetera, tipo, monto, saldo_anterior, saldo_posterior, descripcion
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        wallet["id_billetera"],
                        movement_type,
                        amount,
                        balance,
                        new_balance,
                        description,
                    ),
                )
                conn.commit()
                return {
                    "balance": new_balance,
                    "currency": wallet["moneda"],
                    "transaction_type": movement_type,
                }
