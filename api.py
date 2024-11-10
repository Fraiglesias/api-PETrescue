import random
from flask import Flask, jsonify, render_template, request
import datetime
from flask_cors import CORS

# Importar transbank solo si es necesario
# from transbank.error.transbank_error import TransbankError
# from transbank.webpay.webpay_plus.transaction import Transaction

api = Flask(__name__)
CORS(api, resources={r"/api/*": {"origins": "*"}})

def get_current_datetime():
    return datetime.datetime.utcnow().isoformat()

# Base de datos simulada de productos (lista de diccionarios)
gatitos = [
    {
        "id": 1,
        "name": "Mittens",
        "breed": "British Shorthair",
        "age": 4,
        "birthdate": "2019-02-11",
        "description": "Un gatito británico de pelaje corto, amable y cariñoso."
    },
    {
        "id": 2,
        "name": "Pumpkin",
        "breed": "Tabby",
        "age": 2,
        "birthdate": "2021-10-29",
        "description": "Un juguetón gatito atigrado que ama cazar sombras."
    },
    {
        "id": 3,
        "name": "Smokey",
        "breed": "Russian Blue",
        "age": 3,
        "birthdate": "2020-08-15",
        "description": "Un silencioso y elegante gatito ruso de pelaje azul."
    },
    {
        "id": 4,
        "name": "Luna",
        "breed": "Sphynx",
        "age": 1,
        "birthdate": "2022-04-05",
        "description": "Una gatita curiosa y sin pelo, muy sociable y activa."
    },
    {
        "id": 5,
        "name": "Oscar",
        "breed": "Bengal",
        "age": 5,
        "birthdate": "2018-07-21",
        "description": "Un bengalí aventurero que disfruta trepar y explorar."
    },
    {
        "id": 6,
        "name": "Milo",
        "breed": "Ragdoll",
        "age": 3,
        "birthdate": "2020-01-13",
        "description": "Un gatito dócil y amoroso que disfruta estar en brazos."
    },
    {
        "id": 7,
        "name": "Ziggy",
        "breed": "Scottish Fold",
        "age": 2,
        "birthdate": "2021-05-30",
        "description": "Un Scottish Fold de orejas dobladas, siempre observador."
    },
    {
        "id": 8,
        "name": "Nala",
        "breed": "Calico",
        "age": 4,
        "birthdate": "2019-11-12",
        "description": "Una gatita calico de pelaje colorido y personalidad única."
    },
    {
        "id": 9,
        "name": "Felix",
        "breed": "Bombay",
        "age": 3,
        "birthdate": "2020-03-17",
        "description": "Un gatito negro de mirada intensa y carácter juguetón."
    },
    {
        "id": 10,
        "name": "Simba",
        "breed": "Abyssinian",
        "age": 2,
        "birthdate": "2021-06-24",
        "description": "Un gatito abisinio enérgico que ama correr y explorar."
    }
]
# Base de datos simulada de perfiles (lista de diccionarios)
usuarios = [
    {
        "ID": 1,
        "NOMBRE": "Usuario de Prueba",
        "RUT": "12345678-9",
        "CORREO": "prueba@ejemplo.com",
        "CONTRASENA": "1234",
        "TIPO_PERFIL": 1,
        "DIRECCIÓN": "Calle Falsa 123",
        "REGIÓN": "Región Metropolitana",
        "COMUNA": "Santiago"
    },
    {
        "ID": 2,
        "NOMBRE": "Ana Perez",
        "RUT": "23456789-0",
        "CORREO": "ana.perez@ejemplo.com",
        "CONTRASENA": "abcd1234",
        "TIPO_PERFIL": 2,
        "DIRECCIÓN": "Avenida Siempre Viva 456",
        "REGIÓN": "Región de Valparaíso",
        "COMUNA": "Valparaíso"
    },
    {
        "ID": 3,
        "NOMBRE": "Carlos Lopez",
        "RUT": "34567890-1",
        "CORREO": "carlos.lopez@ejemplo.com",
        "CONTRASENA": "efgh5678",
        "TIPO_PERFIL": 3,
        "DIRECCIÓN": "Calle Principal 789",
        "REGIÓN": "Región del Biobío",
        "COMUNA": "Concepción"
    },
    {
        "ID": 4,
        "NOMBRE": "Maria Gonzalez",
        "RUT": "45678901-2",
        "CORREO": "maria.gonzalez@ejemplo.com",
        "CONTRASENA": "ijkl9101",
        "TIPO_PERFIL": 4,
        "DIRECCIÓN": "Pasaje Central 1011",
        "REGIÓN": "Región de la Araucanía",
        "COMUNA": "Temuco"
    },
    {
        "ID": 5,
        "NOMBRE": "Jorge Martinez",
        "RUT": "56789012-3",
        "CORREO": "jorge.martinez@ejemplo.com",
        "CONTRASENA": "mnop1213",
        "TIPO_PERFIL": 5,
        "DIRECCIÓN": "Camino Real 1213",
        "REGIÓN": "Región de Los Lagos",
        "COMUNA": "Puerto Montt"
    }
]



# Obtener todos los gatitos (GET)
@api.route('/api/gatitos', methods=['GET'])
def get_products():
    return jsonify(gatitos)

# Obtener un gatito por ID (GET)
@api.route('/api/gatitos/<int:gatitos_id>', methods=['GET'])
def get_product(gatitos_id):
    product = next((item for item in gatitos if item["id"] == gatitos_id), None)
    if product:
        return jsonify(product)
    else:
        return jsonify({"message": "Gatito no encontrado"}), 404

# Agregar un nuevo gatito (POST)
@api.route('/api/gatitos', methods=['POST'])
def add_product():
    new_product = request.json
    new_product["id"] = max(gatito["id"] for gatito in gatitos) + 1  # Asigna un nuevo ID automáticamente
    gatitos.append(new_product)
    return jsonify({"message": "Gatito agregado correctamente", "gatito": new_product}), 201

# Actualizar un gatito existente (PUT)
@api.route('/api/gatitos/<int:gatitos_id>', methods=['PUT'])
def update_product(gatitos_id):
    global gatitos
    product = next((item for item in gatitos if item["id"] == gatitos_id), None)
    if product:
        updated_gatitos = request.json
        product.update(updated_gatitos)
        return jsonify({"message": "Gatito actualizado correctamente", "gatito": product})
    else:
        return jsonify({"message": "Gatito no encontrado"}), 404

# Eliminar un gatito (DELETE)
@api.route('/api/gatitos/<int:gatitos_id>', methods=['DELETE'])
def delete_product(gatitos_id):
    global gatitos
    gatitos = [item for item in gatitos if item["id"] != gatitos_id]
    return jsonify({"message": "Gatito eliminado correctamente", "gatitos": gatitos})


# Ruta de inicio de sesión
@api.route('/api/usuarios', methods=['POST'])
def login():
    data = request.json
    correo = data.get('CORREO')
    contrasena = data.get('CONTRASENA')
    
    user = next((profile for profile in usuarios if profile["CORREO"] == correo and profile["CONTRASENA"] == contrasena), None)
    
    if user:
        return jsonify({"message": "Inicio de sesión exitoso", "user": user}), 200
    else:
        return jsonify({"message": "Error en inicio de sesión. Verifica tus credenciales."}), 401


# Ruta para registrar una nueva cuenta (POST)
# Agregar un nuevo perfil (POST)
@api.route('/api/usuarios', methods=['PUT'])
def add_profile():
    new_profile = request.json
    
    # Asigna un nuevo ID automáticamente
    new_profile["ID"] = max(profile["ID"] for profile in usuarios) + 1 if usuarios else 1
    
    # Añade el nuevo perfil a la lista de perfiles
    usuarios.append(new_profile)
    
    # Devuelve un mensaje de éxito junto con el perfil creado
    return jsonify({"message": "Perfil agregado correctamente", "usuarios": new_profile}), 201

# Ruta para recuperar contraseña (POST)
@api.route('/api/usuarios', methods=['POST'])
def recover_password():
    data = request.json
    correo = data.get('CORREO')
    
    # Buscar usuario por correo
    user = next((profile for profile in usuarios if profile["CORREO"] == correo), None)
    
    if user:
        # En una aplicación real, aquí se enviaría la contraseña al correo electrónico
        return jsonify({"message": "Contraseña recuperada con éxito", "password": user["CONTRASENA"]}), 200
    else:
        return jsonify({"message": "Correo no encontrado"}), 404

@api.route('/api/test', methods=['GET'])
def test():
    return jsonify({"message": "Ruta de prueba funcionando correctamente"})

@api.route('/api/usuarios', methods=['GET'])
def get_products2():
    return jsonify(usuarios)

if __name__ == '__main__':
    api.run(host='0.0.0.0', port=5000, debug=True)