import json

from db.connection import get_connection


class RouletteRepository:
    def get_user_wallet(self, user_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT b.id_billetera, b.saldo, u.activo
                    FROM billeteras b
                    JOIN usuarios u ON u.id_usuario = b.id_usuario
                    WHERE b.id_usuario = %s
                    """,
                    (user_id,),
                )
                return cur.fetchone()

    def get_ruleta_game(self):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id_juego, apuesta_min, apuesta_max
                    FROM juegos
                    WHERE tipo = 'ruleta' AND activo = TRUE
                    ORDER BY id_juego
                    LIMIT 1
                    """
                )
                return cur.fetchone()

    def _get_or_create_session(self, cur, user_id, game_id):
        cur.execute(
            """
            SELECT id_sesion
            FROM sesiones_juego
            WHERE id_usuario = %s AND id_juego = %s AND estado = 'activa'
            ORDER BY id_sesion DESC
            LIMIT 1
            """,
            (user_id, game_id),
        )
        row = cur.fetchone()
        if row:
            return row["id_sesion"]
        cur.execute(
            """
            INSERT INTO sesiones_juego (id_usuario, id_juego, estado)
            VALUES (%s, %s, 'activa')
            RETURNING id_sesion
            """,
            (user_id, game_id),
        )
        created = cur.fetchone()
        return created["id_sesion"]

    def process_spin(self, user_id, amount, won, prize, spin_detail):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT b.id_billetera, b.saldo
                    FROM billeteras b
                    WHERE b.id_usuario = %s
                    FOR UPDATE
                    """,
                    (user_id,),
                )
                wallet = cur.fetchone()
                if not wallet:
                    raise ValueError("Billetera no encontrada")
                balance = float(wallet["saldo"])
                if balance < amount:
                    raise ValueError("Saldo insuficiente")
                cur.execute(
                    """
                    SELECT id_juego, apuesta_min, apuesta_max
                    FROM juegos
                    WHERE tipo = 'ruleta' AND activo = TRUE
                    ORDER BY id_juego
                    LIMIT 1
                    """
                )
                game = cur.fetchone()
                if not game:
                    raise ValueError("Juego de ruleta no disponible")
                session_id = self._get_or_create_session(cur, user_id, game["id_juego"])
                balance_after_bet = balance - amount
                cur.execute(
                    """
                    UPDATE billeteras SET saldo = %s WHERE id_billetera = %s
                    """,
                    (balance_after_bet, wallet["id_billetera"]),
                )
                result_label = "ganada" if won else "perdida"
                cur.execute(
                    """
                    INSERT INTO apuestas (id_sesion, monto_apostado, resultado, monto_ganado, detalle_json)
                    VALUES (%s, %s, %s, %s, %s::jsonb)
                    RETURNING id_apuesta
                    """,
                    (
                        session_id,
                        amount,
                        result_label,
                        prize,
                        json.dumps(spin_detail, ensure_ascii=False),
                    ),
                )
                bet_row = cur.fetchone()
                bet_id = bet_row["id_apuesta"]
                cur.execute(
                    """
                    INSERT INTO transacciones (
                        id_billetera, tipo, monto, saldo_anterior, saldo_posterior, id_apuesta, descripcion
                    )
                    VALUES (%s, 'apuesta', %s, %s, %s, %s, %s)
                    """,
                    (
                        wallet["id_billetera"],
                        amount,
                        balance,
                        balance_after_bet,
                        bet_id,
                        "Apuesta ruleta",
                    ),
                )
                final_balance = balance_after_bet
                if won and prize > 0:
                    final_balance = balance_after_bet + prize
                    cur.execute(
                        """
                        UPDATE billeteras SET saldo = %s WHERE id_billetera = %s
                        """,
                        (final_balance, wallet["id_billetera"]),
                    )
                    cur.execute(
                        """
                        INSERT INTO transacciones (
                            id_billetera, tipo, monto, saldo_anterior, saldo_posterior, id_apuesta, descripcion
                        )
                        VALUES (%s, 'premio', %s, %s, %s, %s, %s)
                        """,
                        (
                            wallet["id_billetera"],
                            prize,
                            balance_after_bet,
                            final_balance,
                            bet_id,
                            "Premio ruleta",
                        ),
                    )
                conn.commit()
                return {
                    "bet_id": bet_id,
                    "session_id": session_id,
                    "balance": final_balance,
                }
