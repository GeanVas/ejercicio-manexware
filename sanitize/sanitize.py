import re


def sanitize_string(string):
    return re.sub(r"[^\w\sáéíóúÁÉÍÓÚüÜñÑ]", "", string)