CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario SERIAL PRIMARY KEY,
    rut VARCHAR(12) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    correo VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    rol VARCHAR(20) NOT NULL DEFAULT 'jugador',
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_registro TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS billeteras (
    id_billetera SERIAL PRIMARY KEY,
    id_usuario INTEGER UNIQUE NOT NULL REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    saldo NUMERIC(12,2) NOT NULL DEFAULT 0.00,
    moneda CHAR(3) NOT NULL DEFAULT 'CLP',
    fecha_creacion TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT saldo_no_negativo CHECK (saldo >= 0)
);

CREATE TABLE IF NOT EXISTS juegos (
    id_juego SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    descripcion TEXT,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    rtp NUMERIC(5,2),
    apuesta_min NUMERIC(10,2) NOT NULL DEFAULT 100.00,
    apuesta_max NUMERIC(10,2) NOT NULL DEFAULT 1000000.00,
    fecha_creacion TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS sesiones_juego (
    id_sesion SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL REFERENCES usuarios(id_usuario),
    id_juego INTEGER NOT NULL REFERENCES juegos(id_juego),
    inicio TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    fin TIMESTAMPTZ,
    estado VARCHAR(20) NOT NULL DEFAULT 'activa'
);

CREATE TABLE IF NOT EXISTS apuestas (
    id_apuesta SERIAL PRIMARY KEY,
    id_sesion INTEGER NOT NULL REFERENCES sesiones_juego(id_sesion),
    monto_apostado NUMERIC(12,2) NOT NULL,
    resultado VARCHAR(20) NOT NULL,
    monto_ganado NUMERIC(12,2) NOT NULL DEFAULT 0.00,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    detalle_json JSONB,
    CONSTRAINT monto_positivo CHECK (monto_apostado > 0)
);

CREATE TABLE IF NOT EXISTS transacciones (
    id_transaccion SERIAL PRIMARY KEY,
    id_billetera INTEGER NOT NULL REFERENCES billeteras(id_billetera),
    tipo VARCHAR(20) NOT NULL,
    monto NUMERIC(12,2) NOT NULL,
    saldo_anterior NUMERIC(12,2) NOT NULL,
    saldo_posterior NUMERIC(12,2) NOT NULL,
    id_apuesta INTEGER REFERENCES apuestas(id_apuesta),
    descripcion TEXT,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
