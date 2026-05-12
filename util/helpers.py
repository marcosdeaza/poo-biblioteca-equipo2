import os

def limpiar():
    os.system('cls' if os.name == 'nt' else 'clear')

def pedir_int(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Error: escribe un numero entero.")

def pedir_float(mensaje):
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Error: escribe un numero valido.")

def confirmar(mensaje):
    while True:
        respuesta = input(mensaje + " (s/n): ").strip().lower()
        if respuesta == 's':
            return True
        elif respuesta == 'n':
            return False
        else:
            print("Escribe s o n.")

def separador(titulo=""):
    print("\n" + "=" * 40)
    if titulo:
        print(f"  {titulo}")
        print("=" * 40)
