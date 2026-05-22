from db.connection import get_connection


class GamesRepository:
    def list_active_games(self):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id_juego, nombre, tipo, descripcion, apuesta_min, apuesta_max
                    FROM juegos
                    WHERE activo = TRUE
                    ORDER BY id_juego
                    """
                )
                return cur.fetchall()

    def start_session(self, user_id, game_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id_juego, nombre, tipo, activo
                    FROM juegos
                    WHERE id_juego = %s
                    """,
                    (game_id,),
                )
                game = cur.fetchone()
                if not game or not game["activo"]:
                    raise ValueError("Juego no disponible")
                cur.execute(
                    """
                    UPDATE sesiones_juego
                    SET estado = 'finalizada', fin = NOW()
                    WHERE id_usuario = %s AND id_juego = %s AND estado = 'activa'
                    """,
                    (user_id, game_id),
                )
                cur.execute(
                    """
                    INSERT INTO sesiones_juego (id_usuario, id_juego, estado)
                    VALUES (%s, %s, 'activa')
                    RETURNING id_sesion, inicio
                    """,
                    (user_id, game_id),
                )
                session = cur.fetchone()
                conn.commit()
                return game, session
