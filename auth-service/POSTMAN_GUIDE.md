# 📮 Guía de Postman - Auth Service API

## 🚀 Importar colección en Postman

### Paso 1: Importar archivos
1. Abre Postman
2. Haz clic en **"Import"** (botón superior izquierdo)
3. Arrastra o selecciona estos archivos:
   - `Auth_Service_API.postman_collection.json` (Colección de APIs)
   - `Auth_Service_Environment.postman_environment.json` (Variables de entorno)

### Paso 2: Configurar entorno
1. En la esquina superior derecha, selecciona **"Auth Service Environment"**
2. Verifica que las variables estén configuradas:
   - `base_url`: http://localhost:8000
   - `test_email`: test@postman.com
   - `test_password`: testpass123

## 🧪 Orden de ejecución recomendado

### 1. Health Check ✅
- **Método:** GET
- **URL:** `{{base_url}}/api/health/`
- **Propósito:** Verificar que el servicio esté funcionando

### 2. Register User ✅
- **Método:** POST
- **URL:** `{{base_url}}/api/register/`
- **Body:** JSON con email, password y password_confirm
- **Propósito:** Crear un nuevo usuario

### 3. Login (Get Tokens) ✅
- **Método:** POST
- **URL:** `{{base_url}}/api/token/`
- **Body:** JSON con email y password
- **Propósito:** Obtener tokens JWT
- **Nota:** Los tokens se guardan automáticamente en variables de entorno

### 4. Get User Profile (Me) 🔒
- **Método:** GET
- **URL:** `{{base_url}}/api/me/`
- **Auth:** Bearer Token (usa `{{access_token}}`)
- **Propósito:** Obtener información del usuario autenticado

### 5. Refresh Token ✅
- **Método:** POST
- **URL:** `{{base_url}}/api/token/refresh/`
- **Body:** JSON con refresh token
- **Propósito:** Renovar el access token

## 🔧 Tests automáticos incluidos

Cada request incluye tests automáticos que verifican:

### Health Check
- ✅ Status code 200
- ✅ Service status = "healthy"
- ✅ Service name = "auth-service"

### Register User
- ✅ Status code 201
- ✅ Mensaje de éxito
- ✅ Usuario creado con email e ID

### Login
- ✅ Status code 200
- ✅ Tokens access y refresh recibidos
- ✅ Tokens guardados en variables automáticamente

### Get User Profile
- ✅ Status code 200
- ✅ Datos del usuario (email, id, is_active, created_at)

### Refresh Token
- ✅ Status code 200
- ✅ Nuevo access token recibido
- ✅ Token actualizado automáticamente

## ❌ Tests de errores incluidos

### Register User - Duplicate Email
- ✅ Status code 400
- ✅ Error de email duplicado

### Login - Invalid Credentials
- ✅ Status code 401
- ✅ Error de credenciales inválidas

### Access Protected Endpoint - No Token
- ✅ Status code 401
- ✅ Error de autenticación requerida

## 🔄 Flujo completo de pruebas

1. **Health Check** → Verificar servicio
2. **Register User** → Crear usuario de prueba
3. **Login** → Obtener tokens JWT
4. **Get User Profile** → Usar token para acceder a endpoint protegido
5. **Refresh Token** → Renovar access token
6. **Error Tests** → Probar casos de error

## 📊 Variables de entorno

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `base_url` | URL base del servicio | http://localhost:8000 |
| `test_email` | Email para pruebas | test@postman.com |
| `test_password` | Password para pruebas | testpass123 |
| `access_token` | Token JWT de acceso | (se llena automáticamente) |
| `refresh_token` | Token JWT de refresh | (se llena automáticamente) |

## 🎯 Consejos para las pruebas

1. **Ejecuta en orden:** Primero Health Check, luego Register, después Login
2. **Revisa los tests:** Cada request tiene tests automáticos en la pestaña "Tests"
3. **Verifica variables:** Los tokens se guardan automáticamente después del login
4. **Prueba errores:** Ejecuta los tests de error para verificar validaciones
5. **Cambia datos:** Puedes modificar el email y password en las variables de entorno

## 🚨 Solución de problemas

### Error de conexión
- Verifica que los contenedores estén corriendo: `docker ps`
- Verifica que el servicio responda: `curl http://localhost:8000/api/health/`

### Error 500 en endpoints
- Revisa logs del contenedor: `docker-compose logs auth-service`
- Verifica que las migraciones estén aplicadas

### Token expirado
- Ejecuta el endpoint "Refresh Token" para obtener un nuevo access token
- O ejecuta "Login" nuevamente para obtener tokens frescos

## 📱 Ejemplo de respuestas

### Health Check
```json
{
  "status": "healthy",
  "service": "auth-service",
  "version": "1.0.0"
}
```

### Register User
```json
{
  "message": "Usuario creado exitosamente",
  "user": {
    "id": 1,
    "email": "test@postman.com",
    "is_active": true,
    "created_at": "2025-10-31T17:30:00Z",
    "updated_at": "2025-10-31T17:30:00Z"
  }
}
```

### Login
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```