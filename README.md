# Microservices Lab

Laboratorio de microservicios con PostgreSQL, Redis y servicios de autenticación.

## 🚀 Inicio Rápido

### Prerrequisitos

- [Docker](https://www.docker.com/get-started) instalado
- [Docker Compose](https://docs.docker.com/compose/install/) instalado
- Git

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd microservices-lab-yordy
```

### 2. Levantar los servicios

```bash
# Levantar todos los contenedores en segundo plano
docker-compose up -d
```

### 3. Verificar que los servicios estén corriendo

```bash
# Ver contenedores activos
docker ps
```

Deberías ver 3 contenedores corriendo:
- `db_postgres` - Base de datos PostgreSQL (puerto 5432)
- `cache_redis` - Cache Redis (puerto 6379)
- `auth_service` - Servicio de autenticación

### 4. Probar las conexiones

```bash
# Ejecutar test de conexión dentro del contenedor
docker exec -it auth_service python test_connection.py
```

Si todo está configurado correctamente, verás:
```
🎉 ¡Todas las conexiones funcionan correctamente!
```

## 📋 Servicios Disponibles

### PostgreSQL
- **Puerto:** 5432
- **Base de datos:** main_db
- **Usuario:** devuser
- **Password:** devpass

### Redis
- **Puerto:** 6379
- **Sin autenticación**

### Auth Service
- Contenedor con Python 3.11
- Dependencias: psycopg2-binary, redis
- Script de pruebas incluido

## 🛠️ Comandos Útiles

### Gestión de contenedores

```bash
# Levantar servicios
docker-compose up -d

# Ver logs de todos los servicios
docker-compose logs

# Ver logs de un servicio específico
docker-compose logs postgres

# Parar todos los servicios
docker-compose down

# Parar y eliminar volúmenes
docker-compose down -v

# Reconstruir imágenes
docker-compose build --no-cache
```

### Acceso a contenedores

```bash
# Acceder al contenedor de auth-service
docker exec -it auth_service bash

# Acceder a PostgreSQL
docker exec -it db_postgres psql -U devuser -d main_db

# Acceder a Redis CLI
docker exec -it cache_redis redis-cli
```

### Desarrollo

```bash
# Ejecutar tests de conexión
docker exec -it auth_service python test_connection.py

# Instalar nuevas dependencias en auth-service
docker exec -it auth_service pip install <paquete>

# Ver variables de entorno del auth-service
docker exec -it auth_service env
```

## 🔧 Configuración

### Variables de entorno

El servicio `auth-service` usa las siguientes variables de entorno:

```env
# PostgreSQL
DB_HOST=postgres
DB_PORT=5432
DB_NAME=main_db
DB_USER=devuser
DB_PASSWORD=devpass

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=
```

### Estructura del proyecto

```
microservices-lab-yordy/
├── auth-service/
│   ├── Dockerfile
│   ├── test_connection.py
│   └── requirements-test.txt
├── reverse-proxy/
│   └── README.md
├── docker-compose.yml
├── .gitignore
└── README.md
```

## 🐛 Solución de Problemas

### Los contenedores no inician

```bash
# Verificar logs
docker-compose logs

# Limpiar y reiniciar
docker-compose down -v
docker-compose up -d
```

### Error de conexión a la base de datos

```bash
# Verificar que PostgreSQL esté corriendo
docker exec -it db_postgres pg_isready -U devuser

# Verificar logs de PostgreSQL
docker-compose logs postgres
```

### Error de conexión a Redis

```bash
# Verificar que Redis esté corriendo
docker exec -it cache_redis redis-cli ping

# Verificar logs de Redis
docker-compose logs redis
```

### Reconstruir el servicio auth-service

```bash
# Si modificas el Dockerfile o requirements
docker-compose build auth-service
docker-compose up -d auth-service
```

## 📝 Notas de Desarrollo

- Los datos de PostgreSQL se persisten en un volumen Docker (`pgdata`)
- El contenedor `auth-service` se mantiene corriendo con `tail -f /dev/null`
- Las dependencias de Python se instalan automáticamente al construir la imagen
- Los servicios están en la misma red Docker y pueden comunicarse por nombre

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request