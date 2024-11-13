import random
from sqlite3 import IntegrityError, OperationalError
import time
from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy import create_engine, Column, Integer, String
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
import bcrypt  # Para encriptar la nueva contraseña



# Initialize Flask app and CORS
api = Flask(__name__)
CORS(api, resources={r"/api/*": {"origins": "*"}})

from sqlalchemy import create_engine
engine = create_engine('sqlite:///database.db', connect_args={'timeout': 15})
Session = sessionmaker(bind=engine)
engine = create_engine("sqlite:///database.db", connect_args={"timeout": 10})


# Configure SQLite database
DATABASE_URL = "sqlite:///C:/SQLite/database.db" # SQLite database file
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define usuarios model based on your existing usuarioss structure

class Gatito(Base):
    __tablename__ = "gatitos"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    breed = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    birthdate = Column(String, nullable=True)  # Adjust as needed
    description = Column(String, nullable=True)

     # Convert model to dictionary for JSON serialization
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'breed': self.breed,
            'age': self.age,
            'birthdate': self.birthdate,
            'description': self.description
        }

class Profile(Base):
    __tablename__ = "Profiles"
    
    ID = Column(Integer, primary_key=True, index=True)
    NOMBRE = Column(String, nullable=False)
    RUT = Column(String, nullable=False)
    CORREO = Column(String, unique=True, nullable=False)
    CONTRASENA = Column(String, nullable=False)
    TIPO_PERFIL = Column(Integer, nullable=False)
    DIRECCION = Column(String)
    REGION = Column(String)
    COMUNA = Column(String)

    def to_dict(self):
        return {
            'ID': self.ID,
            'NOMBRE': self.NOMBRE,
            'RUT': self.RUT,
            'CORREO': self.CORREO,
            'CONTRASENA': self.CONTRASENA,  # Asegúrate de que quieres incluir esta información sensible.
            'TIPO_PERFIL': self.TIPO_PERFIL,
            'DIRECCION': self.DIRECCION,
            'REGION': self.REGION,
            'COMUNA': self.COMUNA
        }

# Create tables
Base.metadata.create_all(bind=engine)


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Update existing endpoints to interact with SQLite via SQLAlchemy
# Get all gatitos (GET)
@api.route('/api/gatitos', methods=['GET'])
def get_gatitos():
    db = next(get_db())
    gatitos = db.query(Gatito).all()
    gatitos_dict = [
        {
            "id": gatito.id,
            "name": gatito.name,
            "breed": gatito.breed,
            "age": gatito.age,
            "birthdate": gatito.birthdate,
            "description": gatito.description
        }
        for gatito in gatitos
    ]
    return jsonify(gatitos_dict)
# Get a gatito by ID (GET)
@api.route('/api/gatitos/<int:gatitos_id>', methods=['GET'])
def get_gatito(gatitos_id):
    db = next(get_db())
    gatito = db.query(Gatito).filter(Gatito.id == gatitos_id).first()
    if gatito:
        return jsonify(gatito.__dict__)
    else:
        return jsonify({"message": "Gatito no encontrado"}), 404

@api.route('/api/gatitos', methods=['POST'])
def add_gatito():
    db = next(get_db())
    new_gatito_data = request.json
    new_gatito = Gatito(**new_gatito_data)
    
    try:
        db.add(new_gatito)
        db.commit()  # Asegúrate de que el commit esté aquí
        db.refresh(new_gatito)
        return jsonify({"message": "Gatito agregado correctamente", "gatito": new_gatito.to_dict()}), 201
    except Exception as e:
        db.rollback()
        return jsonify({"message": "Error al agregar el gatito", "error": str(e)}), 500
    finally:
        db.close()


@api.route('/api/gatitos/<int:id>', methods=['PUT'])
def update_gatito_endpoint(id):
    db = next(get_db())
    updated_data = request.json
    
    for attempt in range(5):  # Intenta hasta 5 veces
        try:
            gatito = db.query(Gatito).filter_by(id=id).first()
            if gatito:
                for key, value in updated_data.items():
                    setattr(gatito, key, value)
                db.commit()
                return jsonify({"message": "Gatito actualizado correctamente"}), 200
            else:
                return jsonify({"error": "Gatito no encontrado"}), 404
        except sqlalchemy.exc.OperationalError as e:
            if "database is locked" in str(e):
                time.sleep(1)  # Espera un segundo antes de reintentar
                continue
            else:
                db.rollback()
                return jsonify({"error": "Error al actualizar el gatito"}), 500
        finally:
            db.close()

# Delete a gatito (DELETE)
@api.route('/api/gatitos/<int:gatitos_id>', methods=['DELETE'])
def delete_gatito(gatitos_id):
    db = next(get_db())
    gatito = db.query(Gatito).filter(Gatito.id == gatitos_id).first()
    if gatito:
        db.delete(gatito)
        db.commit()
        return jsonify({"message": "Gatito eliminado correctamente"})
    else:
        return jsonify({"message": "Gatito no encontrado"}), 404

# Get all profiles (GET)
@api.route('/api/usuarios', methods=['GET'])
def get_profiles():
    db = next(get_db())
    profiles = db.query(Profile).all()
    return jsonify([profile.to_dict() for profile in profiles])


# Get a profile by ID (GET)
@api.route('/api/usuarios/<int:profile_id>', methods=['GET'])
def get_profile(profile_id):
    db = next(get_db())
    profile = db.query(Profile).filter(Profile.ID == profile_id).first()
    if profile:
        return jsonify(profile.to_dict())
    else:
        return jsonify({"message": "Perfil no encontrado"}), 404

# Add a new profile (POST)
@api.route('/api/usuarios', methods=['POST'])
def add_profile():
    db = next(get_db())
    new_profile_data = request.json
    new_profile = Profile(**new_profile_data)
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    
    # Convertir el objeto en un diccionario excluyendo atributos no serializables
    profile_dict = {column.name: getattr(new_profile, column.name) for column in Profile.__table__.columns}
    
    return jsonify({"message": "Perfil agregado correctamente", "profile": profile_dict}), 201

# Update an existing profile (PUT)
@api.route('/api/usuarios/recover-password', methods=['PUT'])
def recover_password():
    data = request.json
    correo = data.get('correo')
    new_password = data.get('new_password')
    
    if not correo or not new_password:
        return jsonify({"message": "Correo y nueva contraseña son requeridos", "success": False}), 400
    
    db = next(get_db())
    try:
        # Busca el perfil basado en el correo
        profile = db.query(Profile).filter(Profile.CORREO == correo).first()
        
        if profile:
            # Actualiza la contraseña del perfil encontrado
            profile.CONTRASENA = new_password
            db.commit()
            db.refresh(profile)
            return jsonify({"message": "Contraseña actualizada correctamente", "success": True})
        else:
            return jsonify({"message": "Correo no encontrado", "success": False}), 404
    finally:
        db.close()

    return jsonify({"message": "Error al actualizar la contraseña", "success": False}), 500

# Delete a profile (DELETE)
@api.route('/api/usuarios/<int:profile_id>', methods=['DELETE'])
def delete_profile(profile_id):
    db = next(get_db())
    profile = db.query(Profile).filter(Profile.ID == profile_id).first()
    if profile:
        db.delete(profile)
        db.commit()
        return jsonify({"message": "Perfil eliminado correctamente"})
    else:
        return jsonify({"message": "Perfil no encontrado"}), 404

# Validate a user by email and password (POST)
@api.route('/api/usuarios/validar', methods=['POST'])
def validate_user():
    db = next(get_db())
    data = request.json
    correo = data.get('CORREO')
    contrasena = data.get('CONTRASENA')
    
    profile = db.query(Profile).filter(Profile.CORREO == correo, Profile.CONTRASENA == contrasena).first()
    if profile:
     return jsonify({"user": profile.to_dict()})
    else:
        return jsonify({"message": "Usuario no encontrado"}), 404





if __name__ == '__main__':
    api.run(host='0.0.0.0', port=5000, debug=True)
