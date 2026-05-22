from db.connection import get_connection


class HistoryRepository:
    def list_user_history(self, user_id, limit=20):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT t.id_transaccion, t.tipo, t.monto, t.saldo_anterior,
                           t.saldo_posterior, t.descripcion, t.timestamp,
                           a.id_apuesta, a.resultado, a.monto_apostado
                    FROM transacciones t
                    JOIN billeteras b ON b.id_billetera = t.id_billetera
                    LEFT JOIN apuestas a ON a.id_apuesta = t.id_apuesta
                    WHERE b.id_usuario = %s
                    ORDER BY t.timestamp DESC
                    LIMIT %s
                    """,
                    (user_id, limit),
                )
                rows = cur.fetchall()
                return [
                    {
                        "id_transaccion": row["id_transaccion"],
                        "tipo": row["tipo"],
                        "monto": float(row["monto"]),
                        "saldo_anterior": float(row["saldo_anterior"]),
                        "saldo_posterior": float(row["saldo_posterior"]),
                        "descripcion": row["descripcion"],
                        "timestamp": row["timestamp"].isoformat(),
                        "id_apuesta": row["id_apuesta"],
                        "resultado_apuesta": row["resultado"],
                        "monto_apostado": (
                            float(row["monto_apostado"])
                            if row["monto_apostado"] is not None
                            else None
                        ),
                    }
                    for row in rows
                ]
