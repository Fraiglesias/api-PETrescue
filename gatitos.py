import sqlite3
DATABASE_URL = "C:/SQLite/database.db"

# Sample data for insertion
gatito_data = [
    {"name": "Mittens", "breed": "British Shorthair", "age": 4, "birthdate": "2019-02-11", "description": "Un gatito británico de pelaje corto, amable y cariñoso."},
    {"name": "Pumpkin", "breed": "Tabby", "age": 2, "birthdate": "2021-10-29", "description": "Un juguetón gatito atigrado que ama cazar sombras."},
    {"name": "Smokey", "breed": "Russian Blue", "age": 3, "birthdate": "2020-08-15", "description": "Un silencioso y elegante gatito ruso de pelaje azul."},
    {"name": "Luna", "breed": "Sphynx", "age": 1, "birthdate": "2022-04-05", "description": "Una gatita curiosa y sin pelo, muy sociable y activa."},
    {"name": "Oscar", "breed": "Bengal", "age": 5, "birthdate": "2018-07-21", "description": "Un bengalí aventurero que disfruta trepar y explorar."},
    {"name": "Milo", "breed": "Ragdoll", "age": 3, "birthdate": "2020-01-13", "description": "Un gatito dócil y amoroso que disfruta estar en brazos."},
    {"name": "Ziggy", "breed": "Scottish Fold", "age": 2, "birthdate": "2021-05-30", "description": "Un Scottish Fold de orejas dobladas, siempre observador."},
    {"name": "Nala", "breed": "Calico", "age": 4, "birthdate": "2019-11-12", "description": "Una gatita calico de pelaje colorido y personalidad única."},
    {"name": "Felix", "breed": "Bombay", "age": 3, "birthdate": "2020-03-17", "description": "Un gatito negro de mirada intensa y carácter juguetón."},
    {"name": "Simba", "breed": "Abyssinian", "age": 2, "birthdate": "2021-06-24", "description": "Un gatito abisinio enérgico que ama correr y explorar."}
]

# Connect to the database
conn = sqlite3.connect(DATABASE_URL)
cursor = conn.cursor()

# Insert each record from `gatito_data` into the table
for gatito in gatito_data:
    cursor.execute("""
        INSERT INTO gatitos (name, breed, age, birthdate, description)
        VALUES (:name, :breed, :age, :birthdate, :description)
    """, gatito)

# Commit the changes and close the connection
conn.commit()
conn.close()
