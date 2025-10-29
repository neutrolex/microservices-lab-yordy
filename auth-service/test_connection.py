#!/usr/bin/env python3
"""
Script para probar conexiones a PostgreSQL y Redis
usando variables de entorno.
"""

import os
import sys
import psycopg2
import redis
from psycopg2 import OperationalError
from redis.exceptions import ConnectionError as RedisConnectionError


def test_postgresql_connection():
    """Prueba la conexión a PostgreSQL"""
    print("🔍 Probando conexión a PostgreSQL...")
    
    try:
        # Obtener variables de entorno
        db_host = os.getenv('DB_HOST', 'localhost')
        db_port = os.getenv('DB_PORT', '5432')
        db_name = os.getenv('DB_NAME', 'authdb')
        db_user = os.getenv('DB_USER', 'postgres')
        db_password = os.getenv('DB_PASSWORD', 'password')
        
        print(f"  Host: {db_host}")
        print(f"  Puerto: {db_port}")
        print(f"  Base de datos: {db_name}")
        print(f"  Usuario: {db_user}")
        
        # Intentar conexión
        connection = psycopg2.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user,
            password=db_password
        )
        
        # Probar consulta simple
        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        
        print(f"✅ PostgreSQL conectado exitosamente!")
        print(f"  Versión: {db_version[0]}")
        
        cursor.close()
        connection.close()
        return True
        
    except OperationalError as e:
        print(f"❌ Error conectando a PostgreSQL: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado con PostgreSQL: {e}")
        return False


def test_redis_connection():
    """Prueba la conexión a Redis"""
    print("\n🔍 Probando conexión a Redis...")
    
    try:
        # Obtener variables de entorno
        redis_host = os.getenv('REDIS_HOST', 'localhost')
        redis_port = int(os.getenv('REDIS_PORT', '6379'))
        redis_password = os.getenv('REDIS_PASSWORD', None)
        
        print(f"  Host: {redis_host}")
        print(f"  Puerto: {redis_port}")
        print(f"  Password: {'***' if redis_password else 'No configurado'}")
        
        # Intentar conexión
        r = redis.Redis(
            host=redis_host,
            port=redis_port,
            password=redis_password,
            decode_responses=True
        )
        
        # Probar ping
        response = r.ping()
        if response:
            print("✅ Redis conectado exitosamente!")
            
            # Obtener información del servidor
            info = r.info()
            print(f"  Versión: {info.get('redis_version', 'N/A')}")
            print(f"  Modo: {info.get('redis_mode', 'N/A')}")
            
            return True
        else:
            print("❌ Redis no respondió al ping")
            return False
            
    except RedisConnectionError as e:
        print(f"❌ Error conectando a Redis: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado con Redis: {e}")
        return False


def main():
    """Función principal"""
    print("🚀 Iniciando pruebas de conexión...\n")
    
    # Mostrar variables de entorno relevantes
    print("📋 Variables de entorno detectadas:")
    env_vars = [
        'DB_HOST', 'DB_PORT', 'DB_NAME', 'DB_USER', 'DB_PASSWORD',
        'REDIS_HOST', 'REDIS_PORT', 'REDIS_PASSWORD'
    ]
    
    for var in env_vars:
        value = os.getenv(var, 'No configurado')
        if 'PASSWORD' in var and value != 'No configurado':
            value = '***'
        print(f"  {var}: {value}")
    
    print("\n" + "="*50)
    
    # Ejecutar pruebas
    postgres_ok = test_postgresql_connection()
    redis_ok = test_redis_connection()
    
    print("\n" + "="*50)
    print("📊 Resumen de pruebas:")
    print(f"  PostgreSQL: {'✅ OK' if postgres_ok else '❌ FALLO'}")
    print(f"  Redis: {'✅ OK' if redis_ok else '❌ FALLO'}")
    
    if postgres_ok and redis_ok:
        print("\n🎉 ¡Todas las conexiones funcionan correctamente!")
        sys.exit(0)
    else:
        print("\n⚠️  Algunas conexiones fallaron. Revisa la configuración.")
        sys.exit(1)


if __name__ == "__main__":
    main()