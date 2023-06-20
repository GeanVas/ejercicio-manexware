from time import sleep
import psycopg2

from config import config
from validations import validations
from sanitize import sanitize

validate_string = validations.validate_string
validate_age = validations.validate_age
sanitize_string = sanitize.sanitize_string

def connect():
    try: 
        conn = psycopg2.connect(
            host        = config.DB_HOST,
            port        = config.DB_PORT,
            database    = config.DB_NAME,
            user        = config.DB_USER,
            password    = config.DB_PASSWORD
        )
        return conn
    except psycopg2.OperationalError as e:
        print("Ocurrió un error al conectarse a la base de datos.")
        print(e)
        exit()

def create_database():
    conn = connect()
    
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS estudiantes (id SERIAL PRIMARY KEY, nombre VARCHAR(50), apellido VARCHAR(50), edad INTEGER)")
    except psycopg2.OperationalError as e:
        print("Ocurrió un error al crear la tabla.")
        print(e)
    finally:
        conn.commit()
        cursor.close()
        conn.close()

def create_student():
    nombre = sanitize_string(input("Ingrese el nombre: "))
    if not validate_string(nombre):
        return
    
    apellido = sanitize_string(input("Ingrese el apellido: "))
    if not validate_string(apellido):
        return
    
    edad = input("Ingrese la edad: ")
    if not validate_age(edad):
        return

    conn = connect()
    
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO estudiantes (nombre, apellido, edad) VALUES (%s, %s, %s)", (nombre, apellido, edad))
    except psycopg2.OperationalError as e:
        print("Ocurrió un error al insertar el registro.")
        print(e)
    finally:
        conn.commit()
        cursor.close()
        conn.close()

def get_students():
    conn = connect()
    
    if not conn:
        return
    try:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM estudiantes")
        students = cursor.fetchall()

        for student in students:
            print(student)
    except psycopg2.OperationalError as e:
        print("Ocurrió un error al obtener los registros.")
        print(e)
    finally:
        cursor.close()
        conn.close()

def update_student():
    try:
        student_id = int(input("Ingrese el ID del estudiante a actualizar: "))
    except ValueError:
        print("El ID debe ser un número entero válido.")
        return

    nombre = sanitize_string(input("Ingrese el nuevo nombre: "))
    if not validate_string(nombre):
        return
    
    apellido = sanitize_string(input("Ingrese el nuevo apellido: "))
    if not validate_string(apellido):
        return
    
    edad = int(input("Ingrese la nueva edad: "))
    if not validate_age(edad):
        return

    conn = connect()
    
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE estudiantes SET nombre = %s, apellido = %s, edad = %s WHERE id = %s", (nombre, apellido, edad, student_id))
    except psycopg2.OperationalError as e:
        print("Ocurrió un error al actualizar el registro.")
        print(e)
    finally:
        conn.commit()
        cursor.close()
        conn.close()

def delete_student():
    try:
        student_id = int(input("Ingrese el ID del estudiante a eliminar: "))
    except ValueError:
        print("El ID debe ser un número entero válido.")
        return

    conn = connect()
    
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM estudiantes WHERE id = %s", (student_id,))
    except psycopg2.OperationalError as e:
        print("Ocurrió un error al eliminar el registro.")
        print(e)
    finally:
        conn.commit()
        cursor.close()
        conn.close()

while True:
    create_database()
    print("1. Crear registro")
    print("2. Leer registros")
    print("3. Actualizar registro")
    print("4. Eliminar registro")
    print("5. Salir")
    
    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        create_student()
    elif opcion == "2":
        get_students()
    elif opcion == "3":
        update_student()
    elif opcion == "4":
        delete_student()
    elif opcion == "5":
        break
    else:
        print("Opción inválida. Intente nuevamente.")
    sleep(1)
    print()