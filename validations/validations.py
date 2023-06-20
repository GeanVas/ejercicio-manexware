def validate_string(s):
    if len(s) > 50:
        print("El nombre o apellido no puede tener más de 50 caracteres.")
        return False
    return True

def validate_age(age):
    try:
        age = int(age)
        if age < 0 or age > 120:
            print("La edad debe estar entre 5 y 120.")
            return False
    except ValueError:
        print("La edad debe ser un numero entero válido.")
        return False
    return True
