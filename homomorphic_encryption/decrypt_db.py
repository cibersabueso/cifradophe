from phe import paillier
import sqlite3
import json

# Cargar las claves guardadas
with open('homomorphic_encryption/keys.json', 'r') as f:
    keys = json.load(f)
    public_key = paillier.PaillierPublicKey(n=int(keys['public_key']['n']))
    private_key = paillier.PaillierPrivateKey(public_key, int(keys['private_key']['p']), int(keys['private_key']['q']))

# Conectar a la base de datos SQLite
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Leer los datos cifrados
cursor.execute('SELECT name, age, encrypted_data FROM patients')
rows = cursor.fetchall()

# Descifrar los datos
for row in rows:
    encrypted_data_serialized = json.loads(row[2])
    encrypted_data = paillier.EncryptedNumber(public_key, int(encrypted_data_serialized['v']), int(encrypted_data_serialized['e']))
    decrypted_age = private_key.decrypt(encrypted_data)
    print(f"Nombre: {row[0]}, Edad: {row[1]}, Edad descifrada: {decrypted_age}")

# Cerrar conexión
conn.close()