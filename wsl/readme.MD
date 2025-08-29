# Conectar PostgreSQL en WSL con DBeaver en Windows

Este documento describe cómo configurar **PostgreSQL en WSL2** para poder acceder desde **DBeaver en Windows**.

---

## 1. Verificar que PostgreSQL esté corriendo en WSL

En la terminal de WSL:
```bash
sudo service postgresql status
```

Debe aparecer como **active**.

---

## 2. Configurar PostgreSQL para aceptar conexiones externas

### 2.1 Habilitar `listen_addresses`
Editar el archivo de configuración:
```bash
sudo nano /etc/postgresql/14/main/postgresql.conf
```

Buscar la línea:
```
#listen_addresses = 'localhost'
```

Cambiarla a:
```
listen_addresses = '*'
```

---

### 2.2 Autorizar la IP de Windows en `pg_hba.conf`
Primero, obtener la IP de Windows para WSL:

En **PowerShell (Windows)**:
```powershell
Get-NetIPAddress -InterfaceAlias "vEthernet (WSL (Hyper-V firewall))" -AddressFamily IPv4 | Select-Object IPAddress
```

Ejemplo de salida:
```
IPAddress
---------
172.30.64.1
```

Esa es la IP que usa Windows para hablar con WSL.

Ahora, en WSL:
```bash
sudo nano /etc/postgresql/14/main/pg_hba.conf
```

Agregar al final:
```
host    all    all    172.30.64.1/32    md5
```

---

## 3. Reiniciar PostgreSQL
En WSL:
```bash
sudo service postgresql restart
```

Verificar que esté escuchando en todas las interfaces:
```bash
sudo ss -lntp '( sport = :5432 )'
```

La salida debe incluir:
```
0.0.0.0:5432
```

---

## 4. Probar conectividad desde Windows

En PowerShell:
```powershell
Test-NetConnection 172.30.78.87 -Port 5432
```

> `172.30.78.87` es la IP de **WSL** (se obtiene con `wsl hostname -I`).  

Si `TcpTestSucceeded : True`, ya hay conexión.

---

## 5. Conexión en DBeaver

En DBeaver crear nueva conexión PostgreSQL con:
- **Host**: `172.30.78.87` (IP de WSL)
- **Port**: `5432`
- **Database**: tu base de datos
- **User/Password**: tus credenciales de PostgreSQL

---

## 6. Posibles errores comunes

### 🔴 `Connection refused`
- PostgreSQL no está corriendo.
- `listen_addresses` sigue en `localhost`.

### 🔴 `no pg_hba.conf entry`
- No agregaste la línea con la IP de Windows en `pg_hba.conf`.

### 🔴 `password authentication failed`
- Usuario o contraseña incorrectos.
- Crear usuario/contraseña en WSL:
  ```bash
  sudo -u postgres psql
  ALTER USER <usuario> WITH PASSWORD '<password>';
  ```

### 🔴 Se cuelga al conectar
- Firewall de Windows bloqueando el puerto 5432.

---

## 7. Opción alternativa: conectar con `localhost` usando portproxy

Si preferís no depender de la IP de WSL (que puede cambiar), podés mapear el puerto 5432 de Windows hacia WSL:

En PowerShell (Administrador):
```powershell
netsh interface portproxy add v4tov4 listenport=5432 listenaddress=127.0.0.1 connectport=5432 connectaddress=172.30.78.87
```

Luego en DBeaver solo usás:
- **Host**: `localhost`
- **Port**: `5432`

> Nota: Si la IP de WSL cambia, hay que borrar y volver a crear el portproxy:
```powershell
netsh interface portproxy delete v4tov4 listenport=5432 listenaddress=127.0.0.1
```

---

✅ Con esto tenés PostgreSQL en WSL accesible desde Windows y listo para usar en DBeaver.
