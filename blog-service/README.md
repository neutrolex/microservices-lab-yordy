# 📝 Blog Service - Microservicio de Blog

🧭 **DÍA 3 — Ejercicio: Blog Service Stack (Django + DRF + PostgreSQL + Redis + Docker)**

Microservicio independiente que expone posts y categorías con paginación, búsqueda y caché.

## 🎯 Objetivo

Construir un microservicio de blog completamente independiente que maneje posts, categorías y autores, con funcionalidades de búsqueda, paginación y cache, preparado para integración futura con Auth Service.

## 🚀 Características Implementadas

### ✅ **Modelos**
- **Category** (id, name, slug, is_active)
- **Author** (id, display_name, email) 
- **Post** (id, title, slug, body, author, category, status, published_at, views)

### ✅ **Endpoints Públicos**
- `GET /api/categories/` → Lista categorías activas (con cache)
- `GET /api/posts/` → Lista posts con búsqueda y paginación
- `GET /api/posts/{id|slug}/` → Detalle de post (con cache e incremento de vistas)

### ✅ **Funcionalidades**
- **Paginación:** 10 posts por página
- **Búsqueda:** Por título y contenido (`?search=término`)
- **Filtros:** Por categoría y autor (`?category=1&author=2`)
- **Cache Redis:** Categorías (2 min) y detalles de post (1 min)
- **Observabilidad:** Health check y logging JSON estructurado

### ✅ **Preparación Futura**
- Middleware de Authorization header (para integración con Auth Service)
- Estructura preparada para endpoints privados

## 🔗 API Endpoints

### Health & Status
- `GET /healthz/` - Health check (DB + Redis)

### Categorías
- `GET /api/categories/` - Listar categorías activas

### Posts
- `GET /api/posts/` - Listar posts publicados
- `GET /api/posts/?search=término` - Buscar posts
- `GET /api/posts/?page=2` - Paginación
- `GET /api/posts/?category=1` - Filtrar por categoría
- `GET /api/posts/?author=1` - Filtrar por autor
- `GET /api/posts/{id}/` - Detalle por ID
- `GET /api/posts/{slug}/` - Detalle por slug

## 🧪 Datos de Prueba

El servicio incluye un comando de seed que carga:
- **5 categorías:** Technology, Programming, Web Development, Data Science, DevOps
- **3 autores:** John Doe, Jane Smith, Mike Johnson  
- **30 posts:** 26 publicados + 4 borradores

```bash
# Ejecutar seed
docker exec -it blog_service python manage.py seed_blog
```

## 📦 Uso con Postman

### Importar Colección
1. Importa `Blog_Service_API.postman_collection.json`
2. Importa `Blog_Service_Environment.postman_environment.json`
3. Selecciona el entorno "Blog Service Environment"

### Endpoints de Prueba
- **Get Categories** - Lista todas las categorías
- **Get Posts** - Lista posts con paginación
- **Get Posts with Search** - Busca "django"
- **Get Posts with Pagination** - Página 2
- **Get Posts by Category** - Filtra por categoría
- **Get Post Detail by ID** - Detalle del post #1
- **Get Post Detail by Slug** - Detalle por slug
- **Test Authorization Header** - Prueba middleware de auth

## 🏗️ Arquitectura

```
blog-service/
├── blog_service/          # Proyecto Django
│   ├── settings.py       # Configuración (DB, Redis, DRF)
│   ├── urls.py          # URLs principales
│   └── wsgi.py          # WSGI para Gunicorn
├── core/                # Utilidades
│   ├── middleware.py    # Logging + Auth header
│   ├── views.py         # Health check
│   └── urls.py          # URLs de core
├── categories/          # App de categorías
│   ├── models.py        # Modelo Category
│   ├── views.py         # ViewSet con cache
│   └── serializers.py   # Serializers DRF
├── authors/             # App de autores
│   ├── models.py        # Modelo Author
│   └── admin.py         # Admin interface
├── posts/               # App de posts
│   ├── models.py        # Modelo Post
│   ├── views.py         # ViewSet con búsqueda/paginación
│   ├── serializers.py   # Serializers para lista/detalle
│   └── management/      # Comando seed_blog
├── requirements.txt     # Dependencias
├── Dockerfile          # Imagen Docker
└── openapi.yaml        # Contrato API
```

## 🔧 Configuración

### Variables de Entorno
```env
DEBUG=1
DB_HOST=postgres
DB_NAME=main_db
DB_USER=devuser
DB_PASS=devpass
REDIS_HOST=redis
REDIS_PORT=6379
```

### Dependencias
- Django 5.0
- Django REST Framework 3.15
- django-filter (búsqueda y filtros)
- django-redis (cache)
- python-slugify (URLs amigables)
- psycopg2-binary (PostgreSQL)
- gunicorn (servidor WSGI)

## 🚀 Comandos de Desarrollo

```bash
# Ejecutar migraciones
docker exec -it blog_service python manage.py migrate

# Cargar datos de prueba
docker exec -it blog_service python manage.py seed_blog

# Acceder al shell de Django
docker exec -it blog_service python manage.py shell

# Ver logs
docker-compose logs blog-service

# Acceder al admin (crear superuser primero)
docker exec -it blog_service python manage.py createsuperuser
# http://localhost:8001/admin/
```

## 📊 Ejemplos de Respuestas

### GET /api/categories/
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Technology",
      "slug": "technology"
    }
  ]
}
```

### GET /api/posts/
```json
{
  "count": 26,
  "next": "http://localhost:8001/api/posts/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Getting Started with Django REST Framework",
      "slug": "getting-started-with-django-rest-framework",
      "excerpt": "Django REST Framework is a powerful toolkit...",
      "author": {
        "id": 1,
        "display_name": "John Doe"
      },
      "category": {
        "id": 2,
        "name": "Programming",
        "slug": "programming"
      },
      "published_at": "2025-10-31T17:40:00Z",
      "views": 0
    }
  ]
}
```

### GET /api/posts/1/
```json
{
  "id": 1,
  "title": "Getting Started with Django REST Framework",
  "slug": "getting-started-with-django-rest-framework",
  "body": "Django REST Framework is a powerful toolkit for building Web APIs...",
  "author": {
    "id": 1,
    "display_name": "John Doe"
  },
  "category": {
    "id": 2,
    "name": "Programming",
    "slug": "programming"
  },
  "published_at": "2025-10-31T17:40:00Z",
  "views": 1,
  "created_at": "2025-10-31T17:40:00Z",
  "updated_at": "2025-10-31T17:40:00Z"
}
```

## 🎯 Funcionalidades Destacadas

### Cache Inteligente
- **Categorías:** Cache de 2 minutos (raramente cambian)
- **Post Detail:** Cache de 1 minuto (balance entre performance y actualización)

### Búsqueda Avanzada
- Búsqueda full-text en título y contenido
- Filtros por categoría y autor
- Paginación automática

### Logging Estructurado
- Logs JSON con método, path, status, duración
- Middleware de logging para todas las requests
- Preparado para agregación de logs

### Preparación para Auth
- Middleware que detecta headers Authorization
- Estructura lista para endpoints privados
- Logging de tokens para debugging futuro

## 🔮 Próximos Pasos (Día 4)

- Integración con Auth Service para validación JWT
- Endpoints privados para crear/editar posts
- Middleware de autorización completo
- Tests automatizados