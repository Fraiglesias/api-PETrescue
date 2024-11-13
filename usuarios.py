import sqlite3
DATABASE_URL = "C:/SQLite/database.db"
# Sample data for insertion
profile_data = [
    {
        "NOMBRE": "Usuario de Prueba",
        "RUT": "12345678-9",
        "CORREO": "prueba@ejemplo.com",
        "CONTRASENA": "1234",
        "TIPO_PERFIL": 1,
        "DIRECCION": "Calle Falsa 123",
        "REGION": "Región Metropolitana",
        "COMUNA": "Santiago"
    },
    {
        "NOMBRE": "Ana Perez",
        "RUT": "23456789-0",
        "CORREO": "ana.perez@ejemplo.com",
        "CONTRASENA": "abcd1234",
        "TIPO_PERFIL": 2,
        "DIRECCION": "Avenida Siempre Viva 456",
        "REGION": "Región de Valparaíso",
        "COMUNA": "Valparaíso"
    },
    {
        "NOMBRE": "Carlos Lopez",
        "RUT": "34567890-1",
        "CORREO": "carlos.lopez@ejemplo.com",
        "CONTRASENA": "efgh5678",
        "TIPO_PERFIL": 3,
        "DIRECCION": "Calle Principal 789",
        "REGION": "Región del Biobío",
        "COMUNA": "Concepción"
    },
    {
        "NOMBRE": "Maria Gonzalez",
        "RUT": "45678901-2",
        "CORREO": "maria.gonzalez@ejemplo.com",
        "CONTRASENA": "ijkl9101",
        "TIPO_PERFIL": 4,
        "DIRECCION": "Pasaje Central 1011",
        "REGION": "Región de la Araucanía",
        "COMUNA": "Temuco"
    },
    {
        "NOMBRE": "Jorge Martinez",
        "RUT": "56789012-3",
        "CORREO": "jorge.martinez@ejemplo.com",
        "CONTRASENA": "mnop1213",
        "TIPO_PERFIL": 5,
        "DIRECCION": "Camino Real 1213",
        "REGION": "Región de Los Lagos",
        "COMUNA": "Puerto Montt"
    }
]

# Connect to the database
conn = sqlite3.connect(DATABASE_URL)
cursor = conn.cursor()

# Insert each record from `profile_data` into the table
for profile in profile_data:
    cursor.execute("""
        INSERT INTO profiles (NOMBRE, RUT, CORREO, CONTRASENA, TIPO_PERFIL, DIRECCION, REGION, COMUNA)
        VALUES (:NOMBRE, :RUT, :CORREO, :CONTRASENA, :TIPO_PERFIL, :DIRECCION, :REGION, :COMUNA)
    """, profile)

# Commit the changes and close the connection
conn.commit()
conn.close()
