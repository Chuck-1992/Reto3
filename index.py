# ******************************************************************************************
# Calculadora Avanzada
# Desarrollo de una Calculadora Avanzada con Funciones y Arreglos
# ******************************************************************************************

# Importaciones
import math
import os
from decimal import Decimal, InvalidOperation, getcontext

# Configurar precisión para trabajar con números grandes
getcontext().prec = 80


# Función para cerrar el programa
def cerrar_programa():
    print("\nGracias por usar la calculadora avanzada.")
    raise SystemExit


# Función para limpiar la consola del CMD
def limpiar_consola():
    os.system("cls")
    print("Consola limpiada correctamente.")


# Función para mostrar datos en formato tabla en la consola
def imprimir_tabla(encabezados, filas):
    filas = [[str(dato) for dato in fila] for fila in filas]

    anchos = []
    for i in range(len(encabezados)):
        ancho_maximo = len(encabezados[i])

        for fila in filas:
            if len(fila[i]) > ancho_maximo:
                ancho_maximo = len(fila[i])

        anchos.append(ancho_maximo)

    separador = "+-" + "-+-".join("-" * ancho for ancho in anchos) + "-+"

    print(separador)
    print("| " + " | ".join(f"{encabezados[i]:<{anchos[i]}}" for i in range(len(encabezados))) + " |")
    print(separador)

    for fila in filas:
        print("| " + " | ".join(f"{fila[i]:<{anchos[i]}}" for i in range(len(fila))) + " |")

    print(separador)


# Función para leer números usando Decimal
def leer_numero(mensaje):
    while True:
        dato = input(mensaje).strip().lower()

        if dato == "salir":
            cerrar_programa()

        try:
            dato = dato.replace(",", ".")
            numero = Decimal(dato)
            return numero
        except InvalidOperation:
            print("Error: debe ingresar un número válido.")


# Función para leer números enteros
def leer_entero(mensaje):
    while True:
        dato = input(mensaje).strip().lower()

        if dato == "salir":
            cerrar_programa()

        try:
            numero = int(dato)

            if numero <= 0:
                print("Error: debe ingresar un número mayor a cero.")
            else:
                return numero

        except ValueError:
            print("Error: debe ingresar un número entero válido.")


# Función para formatear números en decimale válidos
def formatear_numero(numero, decimales=2):
    if abs(numero) >= Decimal("1000"):
        numero_formateado = f"{numero:,.{decimales}f}"
        numero_formateado = numero_formateado.replace(",", "X").replace(".", ",").replace("X", ".")
        return numero_formateado

    elif numero == numero.to_integral_value():
        return str(numero.quantize(Decimal("1")))

    else:
        numero_formateado = format(numero.normalize(), "f")
        numero_formateado = numero_formateado.replace(".", ",")
        return numero_formateado


# Función para realizar la operación de sumar números 
def suma():
    a = leer_numero("Ingrese el primer número: ")
    b = leer_numero("Ingrese el segundo número: ")
    resultado = a + b

    imprimir_tabla(
        ["Operación", "Primer número", "Segundo número", "Resultado"],
        [["Suma", formatear_numero(a), formatear_numero(b), formatear_numero(resultado)]]
    )


# Función para realizar la operación de restar números 
def resta():
    a = leer_numero("Ingrese el primer número: ")
    b = leer_numero("Ingrese el segundo número: ")
    resultado = a - b

    imprimir_tabla(
        ["Operación", "Primer número", "Segundo número", "Resultado"],
        [["Resta", formatear_numero(a), formatear_numero(b), formatear_numero(resultado)]]
    )


# Función para realizar la operación de multiplicar números 
def multiplicacion():
    a = leer_numero("Ingrese el primer número: ")
    b = leer_numero("Ingrese el segundo número: ")
    resultado = a * b

    imprimir_tabla(
        ["Operación", "Primer número", "Segundo número", "Resultado"],
        [["Multiplicación", formatear_numero(a), formatear_numero(b), formatear_numero(resultado)]]
    )


# Función para realizar la operación de dividir números 
def division():
    a = leer_numero("Ingrese el primer número: ")
    b = leer_numero("Ingrese el segundo número: ")

    if b == 0:
        imprimir_tabla(
            ["Error"],
            [["No se puede dividir para cero"]]
        )
    else:
        resultado = a / b

        imprimir_tabla(
            ["Operación", "Primer número", "Segundo número", "Resultado"],
            [["División", formatear_numero(a), formatear_numero(b), formatear_numero(resultado)]]
        )


# Función para realizar la raices cuadradas 
def raiz_cuadrada():
    a = leer_numero("Ingrese un número: ")

    if a < 0:
        imprimir_tabla(
            ["Error"],
            [["No se puede calcular la raíz cuadrada de un número negativo"]]
        )
    else:
        resultado = Decimal(str(math.sqrt(float(a))))

        imprimir_tabla(
            ["Operación", "Número", "Resultado"],
            [["Raíz cuadrada", formatear_numero(a), formatear_numero(resultado)]]
        )



# Función para realizar la potencia de números
def potencia():
    base = leer_numero("Ingrese la base: ")
    exponente = leer_numero("Ingrese el exponente: ")
    resultado = base ** exponente

    imprimir_tabla(
        ["Operación", "Base", "Exponente", "Resultado"],
        [["Potencia", formatear_numero(base), formatear_numero(exponente), formatear_numero(resultado)]]
    )


# Función para ingresar una matriz
def ingresar_matriz(nombre):
    print(f"\nIngreso de la matriz {nombre}")

    filas = leer_entero("Ingrese el número de filas: ")
    columnas = leer_entero("Ingrese el número de columnas: ")

    matriz = []

    for i in range(filas):
        fila = []

        for j in range(columnas):
            valor = leer_numero(f"Ingrese el valor [{i + 1}][{j + 1}]: ")
            fila.append(valor)

        matriz.append(fila)

    return matriz


# Función para mostrar una matriz
def mostrar_matriz(matriz):
    encabezados = []

    for i in range(len(matriz[0])):
        encabezados.append(f"Columna {i + 1}")

    filas = []

    for fila in matriz:
        fila_formateada = []

        for valor in fila:
            fila_formateada.append(formatear_numero(valor))

        filas.append(fila_formateada)

    imprimir_tabla(encabezados, filas)


# Función para multiplicar las matrices ingresadas
def multiplicar_matrices():
    matriz_a = ingresar_matriz("A")
    matriz_b = ingresar_matriz("B")

    filas_a = len(matriz_a)
    columnas_a = len(matriz_a[0])
    filas_b = len(matriz_b)
    columnas_b = len(matriz_b[0])

    if columnas_a != filas_b:
        print("\nError: no se pueden multiplicar las matrices.")
        print("El número de columnas de la matriz A debe ser igual al número de filas de la matriz B.")
        return

    resultado = []

    for i in range(filas_a):
        fila_resultado = []

        for j in range(columnas_b):
            suma = Decimal("0")

            for k in range(columnas_a):
                suma += matriz_a[i][k] * matriz_b[k][j]

            fila_resultado.append(suma)

        resultado.append(fila_resultado)

    print("\nMatriz A:")
    mostrar_matriz(matriz_a)

    print("\nMatriz B:")
    mostrar_matriz(matriz_b)

    print("\nResultado de la multiplicación:")
    mostrar_matriz(resultado)


# Función para mostrar en consola el menú principal
def menu():
    print("\nEscriba 'salir' en cualquier momento para cerrar el programa.")

    while True:
        print("\n************ MENÚ DE OPCIONES ***************")
        print("1. Suma")
        print("2. Resta")
        print("3. Multiplicación")
        print("4. División")
        print("5. Raíz cuadrada")
        print("6. Potencia")
        print("7. Multiplicación de matrices")
        print("8. Limpiar consola")
        print("9. Salir")
        print("*********************************************\n")

        opcion = input("Seleccione una opción: ").strip().lower()

        if opcion == "salir" or opcion == "9":
            print("\nGracias por usar la calculadora avanzada.")
            break
        elif opcion == "1":
            suma()
        elif opcion == "2":
            resta()
        elif opcion == "3":
            multiplicacion()
        elif opcion == "4":
            division()
        elif opcion == "5":
            raiz_cuadrada()
        elif opcion == "6":
            potencia()
        elif opcion == "7":
            multiplicar_matrices()
        elif opcion == "8":
            limpiar_consola()
        else:
            print("Opción no válida. Intente nuevamente.")


# Ejecutar el programa principal 
try:
    menu()

except KeyboardInterrupt:

    print("\n\nGracias por usar la calculadora avanzada.")

