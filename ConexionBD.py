import mysql.connector
from mysql.connector import Error

def conectar_bd():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="LigaHandball"
        )
        if conexion.is_connected():
            return conexion
    except Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None