# Guía de uso - Casino Monticello Virtual

Instrucciones para probar cada funcionalidad del proyecto desde la consola.

## Antes de jugar

### 1. Dependencias y base de datos

```bash
pip install -r requirements.txt
```

Copia `.env.example` a `.env` y define `DB_PASSWORD` (Supabase).

```bash
python db/test_connection.py
python db/init_database.py
```

### 2. Levantar el sistema (orden obligatorio)

**Terminal 1 - Bus SOA**

```bash
cd soa
python soa_bus.py
```

Debe aparecer: `Bus SOA (ESB) escuchando en localhost:5000`

**Terminales 2 a 6 - Servicios** (desde la raíz `monticello-virtual/`)

```bash
python services/auth_service.py
python services/wallet_service.py
python services/games_service.py
python services/roulette_service.py
python services/history_service.py
```

Cada uno debe registrar su nombre en el bus: `auths`, `walle`, `juego`, `histo`, `rulet`.

**Terminal 7 en adelante - Clientes** (elige el que quieras probar)

```bash
python client/auth_client.py
python client/wallet_client.py
python client/games_client.py
python client/roulette_client.py
python client/history_client.py
```

Si un cliente responde `servicio no registrado`, falta levantar ese servicio o el bus.

### 3. Usuario de prueba (semilla)

| Campo         | Valor                |
| ------------- | -------------------- |
| Correo        | `demo@monticello.cl` |
| Contraseña    | `demo123`            |
| ID de usuario | `1`                  |
| Saldo inicial | $50.000 CLP          |

---

## Cliente de autenticación (`auth_client`)

Servicio en bus: `auths`

```bash
python client/auth_client.py
```

### Comandos

| Comando          | Ejemplo                                                  |
| ---------------- | -------------------------------------------------------- |
| Login            | `login demo@monticello.cl demo123`                       |
| Registro         | `registro 22222222-2 Maria Lopez maria@test.cl clave456` |
| Ver sesión local | `usuario`                                                |
| Ayuda            | `ayuda`                                                  |
| Salir            | `salir`                                                  |

### Ejemplo de sesión

```
Auth> login demo@monticello.cl demo123
Autenticacion exitosa
Usuario activo: id 1

Auth> usuario
Usuario activo: id 1
```

Tras un registro exitoso, el cliente guarda el `user_id` devuelto para la sesión de consola.

---

## Cliente de billetera (`wallet_client`)

Servicio en bus: `walle`

```bash
python client/wallet_client.py
```

### Comandos

| Comando         | Ejemplo                                |
| --------------- | -------------------------------------- |
| Consultar saldo | `saldo` o `saldo 1`                    |
| Depositar       | `depositar 10000` o `depositar 5000 1` |
| Retirar         | `retirar 2000` o `retirar 1000 1`      |
| Ayuda           | `ayuda`                                |
| Salir           | `salir`                                |

Si no indicas `user_id`, usa el usuario `1` por defecto.

### Ejemplo de sesión

```
Billetera> saldo
Saldo consultado
Saldo: 50000.0 CLP

Billetera> depositar 10000
Monto depositado correctamente

Billetera> retirar 5000
Monto retirado correctamente

Billetera> saldo
Saldo: 55000.0 CLP
```

---

## Cliente de juegos (`games_client`)

Servicio en bus: `juego`

```bash
python client/games_client.py
```

### Comandos

| Comando                 | Ejemplo                     |
| ----------------------- | --------------------------- |
| Listar catálogo         | `listar`                    |
| Iniciar sesión de juego | `iniciar 1` o `iniciar 1 1` |
| Ayuda                   | `ayuda`                     |
| Salir                   | `salir`                     |

El `id_juego` lo ves en la lista (`listar`). Tras `init_database`, suele haber ruleta, tragamonedas y juego grupal.

### Ejemplo de sesión

```
Juegos> listar

Catalogo de juegos activos
  [1] Ruleta Europea (ruleta) $100.0-$500000.0
  [2] Tragamonedas Clasica (tragamonedas) $100.0-$50000.0
  [3] Poker Grupal (grupal) $500.0-$100000.0

Juegos> iniciar 1
Sesion iniciada en Ruleta Europea
```

---

## Cliente de ruleta (`roulette_client`)

Servicios en bus: `rulet` (apuestas) y `walle` (saldo)

```bash
python client/roulette_client.py
```

### Comandos

| Comando                 | Ejemplo                |
| ----------------------- | ---------------------- |
| Saldo (vía billetera)   | `saldo`                |
| Apostar color / paridad | `apostar rojo 1000`    |
|                         | `apostar negro 500`    |
|                         | `apostar par 2000`     |
|                         | `apostar impar 1500`   |
| Apostar número 0–36     | `apostar numero 7 500` |
| Ayuda                   | `ayuda`                |
| Salir                   | `salir`                |

Apuestas simples (rojo, negro, par, impar): pago 1:1. Número exacto: pago 35:1. El `0` es verde y no gana en rojo/negro/par/impar.

### Ejemplo de sesión

```
Ruleta> saldo

Saldo consultado
Saldo: 55000.0 CLP

Ruleta> apostar rojo 1000

Numero 32 (rojo). ganaste.
Saldo actual: 56000.0
Numero: 32 | Color: rojo | Premio: 1000.0

Ruleta> apostar numero 7 500

Numero 14 (negro). perdiste.
Saldo actual: 55500.0
Numero: 14 | Color: negro | Premio: 0
```

---

## Cliente de historial (`history_client`)

Servicio en bus: `histo`

```bash
python client/history_client.py
```

### Comandos

| Comando              | Ejemplo       |
| -------------------- | ------------- |
| Listar movimientos   | `listar`      |
| Con usuario y límite | `listar 1 10` |
| Ayuda                | `ayuda`       |
| Salir                | `salir`       |

Muestra depósitos, retiros, apuestas y premios del usuario.

### Ejemplo de sesión

```
Historial> listar 1 5

Historial obtenido
  #12 premio $1000.0 -> saldo 56000.0 (2026-05-22T...)
  #11 apuesta $1000.0 -> saldo 55000.0 (2026-05-22T...)
  #10 deposito $10000.0 -> saldo 60000.0 (2026-05-22T...)
```

---

## Recorrido completo para demo

Orden para mostrar todo el sistema:

1. **Auth** - `login demo@monticello.cl demo123`
2. **Juegos** - `listar` -> `iniciar 1`
3. **Billetera** - `saldo` -> `depositar 5000`
4. **Ruleta** - `saldo` -> `apostar rojo 1000`
5. **Historial** - `listar 1 10`

En el panel SQL de Supabase se pueden revisar `apuestas` y `transacciones`.

---

## Ejemplo del profesor (solo de referencia)

Los archivos `soa/soa_client.py` y `soa/soa_service.py` son el ejemplo original con el servicio `servi`. No forman parte de la demo del proyecto de casino, pero usan el mismo protocolo que `soa_lib.py`.

Para probar solo el ejemplo:

```bash
cd soa
python soa_bus.py
```

En otra terminal: `python soa_service.py`. En otra: `python soa_client.py` e ingresa segundos de espera (ej. `3`).
