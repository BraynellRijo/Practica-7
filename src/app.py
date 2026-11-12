import os
import time
import mysql.connector
from flask import Flask

app = Flask(__name__)

def conectar_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "db"),
        database=os.getenv("DB_NAME", "hola_db"),
        user=os.getenv("DB_USER", "hola_user"),
        password=os.getenv("DB_PASSWORD", "hola_pass")
    )

@app.route("/")
def inicio():
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()

        # Crear tabla si no existe
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS visitas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Registrar una visita
        cursor.execute("INSERT INTO visitas () VALUES ()")
        conexion.commit()

        # Consultar total de visitas
        cursor.execute("SELECT COUNT(*) FROM visitas")
        total = cursor.fetchone()[0]

        cursor.close()
        conexion.close()

        return f"""
            <h1>Hola Mundo</h1>
            <h2>Conexion con MySQL exitosa</h2>
            <p>Total de visitas: {total}</p>
        """

    except mysql.connector.Error as error:
        return f"Error de conexion con MySQL: {error}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
