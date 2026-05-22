INSERT INTO usuarios (rut, nombre, apellido, correo, password_hash, rol)
VALUES ('11111111-1', 'Demo', 'Jugador', 'demo@monticello.cl', 'demo123', 'jugador')
ON CONFLICT (correo) DO UPDATE SET password_hash = EXCLUDED.password_hash;

INSERT INTO billeteras (id_usuario, saldo)
SELECT id_usuario, 50000.00 FROM usuarios WHERE correo = 'demo@monticello.cl'
ON CONFLICT (id_usuario) DO NOTHING;

INSERT INTO juegos (nombre, tipo, descripcion, activo, apuesta_min, apuesta_max)
SELECT
    'Ruleta Europea',
    'ruleta',
    'Ruleta basica 0-36 para demostracion SOA',
    TRUE,
    100.00,
    500000.00
WHERE NOT EXISTS (SELECT 1 FROM juegos WHERE tipo = 'ruleta');

INSERT INTO juegos (nombre, tipo, descripcion, activo, apuesta_min, apuesta_max)
SELECT
    'Tragamonedas Clasica',
    'tragamonedas',
    'Slot demo para catalogo SOA',
    TRUE,
    100.00,
    50000.00
WHERE NOT EXISTS (SELECT 1 FROM juegos WHERE tipo = 'tragamonedas');

INSERT INTO juegos (nombre, tipo, descripcion, activo, apuesta_min, apuesta_max)
SELECT
    'Poker Grupal',
    'grupal',
    'Mesa grupal demo para catalogo SOA',
    TRUE,
    500.00,
    100000.00
WHERE NOT EXISTS (SELECT 1 FROM juegos WHERE tipo = 'grupal');
