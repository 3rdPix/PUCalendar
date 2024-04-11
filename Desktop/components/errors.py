import inspect

class NotImplemented(Exception):
    def __init__(self):
        stack = inspect.stack()
        caller_frame = stack[1]
        archivo = caller_frame.filename
        numero_linea = caller_frame.lineno
        super().__init__(f"La funcion en {archivo} linea {numero_linea} no ha sido implementada")
