# Microservices Lab - Auth Service

🧭 **DÍA 2 — Ejercicio 2: BACKEND Microservicio Backend Auth (Django + DRF + JWT + PostgreSQL + Redis)**

Laboratorio de microservicios con Django REST Framework, autenticación JWT, PostgreSQL y Redis.

## 🎯 Objetivo

Construir un microservicio de autenticación completamente independiente que maneje usuarios, login y tokens JWT, corriendo en su propio contenedor Docker.

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

### 3. Ejecutar migraciones (primera vez)

```bash
# Crear y aplicar migraciones
docker exec -it auth_service python manage.py makemigrations
docker exec -it auth_service python manage.py migrate
```

### 4. Crear superusuario (opcional)

```bash
docker exec -it auth_service python manage.py createsuperuser
```

### 5. Verificar que los servicios estén corriendo

```bash
# Ver contenedores activos
docker ps

# Probar health check
curl http://localhost:8000/api/health/
```

Deberías ver 3 contenedores corriendo:
- `db_postgres` - Base de datos PostgreSQL (puerto 5432)
- `cache_redis` - Cache Redis (puerto 6379)
- `auth_service` - Servicio de autenticación Django (puerto 8000)

## 📋 Servicios Disponibles

### PostgreSQL
- **Puerto:** 5432
- **Base de datos:** main_db
- **Usuario:** devuser
- **Password:** devpass

### Redis
- **Puerto:** 6379
- **Sin autenticación**
- **Usado para:** Cache y sesiones

### Auth Service (Django)
- **Puerto:** 8000
- **Framework:** Django 5.0 + Django REST Framework
- **Autenticación:** JWT (Simple JWT)
- **Base de datos:** PostgreSQL
- **Cache:** Redis

## 🔗 API Endpoints

### Health Check
- `GET /api/health/` - Verificar estado del servicio

### Autenticación
- `POST /api/register/` - Registrar nuevo usuario
- `POST /api/token/` - Obtener tokens JWT (login)
- `POST /api/token/refresh/` - Renovar token de acceso

### Usuario
- `GET /api/me/` - Obtener información del usuario autenticado (requiere JWT)

## 🧪 Ejemplos de uso con cURL

### 1. Registrar usuario
```bash
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@test.com",
    "password": "password123",
    "password_confirm": "password123"
  }'
```

### 2. Obtener tokens (Login)
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@test.com",
    "password": "password123"
  }'
```

### 3. Acceder a endpoint protegido
```bash
curl -X GET http://localhost:8000/api/me/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 4. Renovar token
```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "YOUR_REFRESH_TOKEN"
  }'
```

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

### Desarrollo Django

```bash
# Ejecutar tests de conexión
docker exec -it auth_service python test_connection.py

# Acceder al shell de Django
docker exec -it auth_service python manage.py shell

# Ver logs del servicio
docker-compose logs auth-service

# Ejecutar comandos de Django
docker exec -it auth_service python manage.py <comando>

# Crear migraciones
docker exec -it auth_service python manage.py makemigrations

# Aplicar migraciones
docker exec -it auth_service python manage.py migrate

# Crear superusuario
docker exec -it auth_service python manage.py createsuperuser

# Acceder al admin de Django
# http://localhost:8000/admin/
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
│   ├── auth_service/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── users/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── apps.py
│   ├── Dockerfile
│   ├── manage.py
│   ├── requirements.txt
│   └── test_connection.py
├── reverse-proxy/
│   └── README.md
├── docker-compose.yml
├── .gitignore
└── README.md
```

## 🧩 Conceptos implementados

- ✅ **Autenticación basada en JWT** (JSON Web Tokens)
- ✅ **Estructura de servicio Django aislado**
- ✅ **Configuración con variables de entorno**
- ✅ **Cache y sesiones con Redis**
- ✅ **Modelo de usuario personalizado**
- ✅ **API REST con Django REST Framework**
- ✅ **Comunicación segura entre servicios**

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
- El servicio Django corre con Gunicorn en producción
- JWT tokens tienen duración de 60 minutos (access) y 1 día (refresh)
- CORS configurado para desarrollo (localhost:3000)
- Modelo de usuario personalizado usando email como username
- Redis usado para cache de Django
- Las dependencias se instalan automáticamente al construir la imagen

## 📦 Entregables del Día 2

- ✅ **Código funcional del microservicio** - Django + DRF + JWT
- ✅ **Dockerfile y docker-compose.yml actualizados** - Puerto 8000 expuesto
- ✅ **Contenedor funcionando** - Auth service en puerto 8000
- ✅ **Endpoints implementados** - Register, Login, Refresh, Me, Health
- ✅ **README actualizado** - Documentación completa de endpoints

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request