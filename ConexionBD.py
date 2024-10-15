import tkinter as tk
from tkinter import messagebox
import mysql.connector

mydb = mysql.connector.connect(
        host="localhost",
        user="root", #PONER SU PROPIO USUARIO
        password="", #PONER SU PROPIA CLAVE
        database="LigaHandball")
mycursor = mydb.cursor()


