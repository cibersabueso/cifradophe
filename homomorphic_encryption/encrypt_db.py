from phe import paillier
import sqlite3
import json

# Generar claves públicas y privadas
public_key, private_key = paillier.generate_paillier_keypair()

# Datos de ejemplo para cifrar
patients = [
    {"name": "Alice", "age": 29},
    {"name": "Bob", "age": 34}
]

# Conectar a la base de datos SQLite
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Cifrar y almacenar los datos
for patient in patients:
    encrypted_data = public_key.encrypt(patient['age'])
    encrypted_data_serialized = json.dumps({'v': encrypted_data.ciphertext(), 'e': encrypted_data.exponent})
    cursor.execute('INSERT INTO patients (name, age, encrypted_data) VALUES (?, ?, ?)',
                   (patient['name'], patient['age'], encrypted_data_serialized))

# Guardar cambios y cerrar conexión
conn.commit()
conn.close()

# Guardar las claves para su uso posterior
with open('homomorphic_encryption/keys.json', 'w') as f:
    json.dump({
        'public_key': {'n': public_key.n},
        'private_key': {'p': private_key.p, 'q': private_key.q}
    }, f)