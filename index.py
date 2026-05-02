
# ************************************************************************************************
# Calculadora Avanzada con Interfaz Gráfica
# Realizar operaciones suma, resta, multiplicación, división, raíz cuadrada, potencia y matrices
# ************************************************************************************************

# Importación de utilidades
import tkinter as tk
from tkinter import messagebox
import math
from decimal import Decimal, InvalidOperation, getcontext

# Configurar precisión para trabajar con números grandes
getcontext().prec = 80

# Estilos para la interfaz de pantalla para los usuario
COLOR_FONDO = "#0f1117"
COLOR_PANEL = "#111318"
COLOR_PANEL_SECUNDARIO = "#1a1d24"
COLOR_BOTON_NUMERO = "#2d3342"
COLOR_BOTON_OPERADOR = "#3b4360"
COLOR_BOTON_ERROR = "#d85b5b"
COLOR_BOTON_IGUAL = "#9dbcf2"
COLOR_TEXTO = "white"
COLOR_TEXTO_SECUNDARIO = "#cfd6e6"

# Declaración de variables
NUMERO_MAXIMO_PERMITIDO = Decimal("1000000000000")
nombre_usuario = ""


# Método para maximizar la ventana al momento de abrirla
def maximizar_ventana(ventana):
    try:
        ventana.state("zoomed")
    except tk.TclError:
        ancho = ventana.winfo_screenwidth()
        alto = ventana.winfo_screenheight()
        ventana.geometry(f"{ancho}x{alto}+0+0")

    ventana.resizable(True, True)


# Método para convertir el elemento ingresado por el usuario de texto a número decimal
def convertir_decimal(texto):
    dato = str(texto).strip()

    if dato == "":
        raise InvalidOperation

    if dato.lower() == "salir":
        raise SystemExit

    if dato in [".", ",", "-", "-.", "-,"]:
        raise InvalidOperation

    if "," in dato and "." in dato:
        dato = dato.replace(".", "").replace(",", ".")
    else:
        dato = dato.replace(",", ".")

    return Decimal(dato)


# Método para formatear un número, eliminando decimales y ceros innecesarios
def formatear_numero(numero, decimales=2):
    if not isinstance(numero, Decimal):
        numero = Decimal(str(numero))

    if abs(numero) >= Decimal("1000"):
        numero_formateado = f"{numero:,.{decimales}f}"
        numero_formateado = numero_formateado.replace(",", "X").replace(".", ",").replace("X", ".")
        return numero_formateado

    if numero == numero.to_integral_value():
        return str(numero.quantize(Decimal("1")))

    numero_formateado = format(numero.normalize(), "f")
    numero_formateado = numero_formateado.replace(".", ",")
    return numero_formateado

# Método para preparar el número que se va a mostrar en la pantalla de la calculadora
def formatear_numero_pantalla(numero):
    if not isinstance(numero, Decimal):
        numero = Decimal(str(numero))

    if numero == numero.to_integral_value():
        return str(numero.quantize(Decimal("1")))

    return format(numero.normalize(), "f")


# Método para obtener el simbolo seleccionado para ejecutar la operación
def obtener_simbolo_operador(operador):
    if operador == "+":
        return "+"
    if operador == "-":
        return "−"
    if operador == "*":
        return "×"
    if operador == "/":
        return "÷"
    if operador == "**":
        return "^"
    return operador


# Método para obtener el nombre de la operacion para mostrar en la sección de análisis
def obtener_nombre_operacion(operador):
    if operador == "+":
        return "Suma"
    if operador == "-":
        return "Resta"
    if operador == "*":
        return "Multiplicación"
    if operador == "/":
        return "División"
    if operador == "**":
        return "Potencia"
    return "Operación desconocida"


# Método para validar el nombre del usuario antes de abrir la calculadora
def abrir_calculadora():
    ventana = tk.Tk()
    ventana.title("Calculadora Avanzada | Python")
    ventana.configure(bg=COLOR_FONDO)
    maximizar_ventana(ventana)

    entrada_actual = "0"
    primer_valor = None
    operador_actual = None
    reiniciar_pantalla = False

    variable_pantalla = tk.StringVar(value="0")

    # Método para actualizar el valor que se muestra en la pantalla principal de la calculadora
    def actualizar_pantalla():
        variable_pantalla.set(entrada_actual)

    # Método para escribir información dentro del panel de análisis de la calculadora
    def escribir_analisis(titulo, contenido):
        caja_analisis.config(state="normal")
        caja_analisis.delete("1.0", tk.END)
        caja_analisis.insert(tk.END, titulo + "\n", "titulo")
        caja_analisis.insert(tk.END, contenido, "normal")
        caja_analisis.config(state="disabled")

    # Método para limpiar el panel de análisis y mostrar nuevamente el mensaje inicial
    def limpiar_analisis():
        escribir_analisis(
            "Panel de análisis",
            "Aquí se mostrará el análisis del resultado."
        )

    # Método para mostrar en el panel de análisis un mensaje de error relacionado con la operación
    def mostrar_error_analisis(mensaje):
        escribir_analisis("Error:", mensaje)


    # Método para generar y mostrar el resumen del cálculo realizado por el usuario
    def mostrar_analisis(primer_numero, operador, segundo_numero, resultado):
        if resultado > 0:
            tipo_resultado = "Positivo"
        elif resultado < 0:
            tipo_resultado = "Negativo"
        else:
            tipo_resultado = "Cero"

        if resultado == resultado.to_integral_value():
            tipo_numero = "Entero"
        else:
            tipo_numero = "Decimal"

        resumen = (
            f"{formatear_numero(primer_numero)} "
            f"{obtener_simbolo_operador(operador)} "
            f"{formatear_numero(segundo_numero)} = "
            f"{formatear_numero(resultado)}"
        )

        contenido = (
            f"{resumen}\n\n"
            f"Tipo de operación: {obtener_nombre_operacion(operador)}\n"
            f"Tipo de resultado: {tipo_resultado}\n"
            f"Clasificación numérica: {tipo_numero}\n"
        )

        escribir_analisis("Resumen del cálculo:", contenido)


    # Método para agregar números o el punto decimal a la pantalla de la calculadora
    def agregar_numero(numero):
        nonlocal entrada_actual, reiniciar_pantalla

        if entrada_actual == "Error":
            entrada_actual = "0"

        if reiniciar_pantalla:
            entrada_actual = ""
            reiniciar_pantalla = False

        if numero == "." and "." in entrada_actual:
            return

        if entrada_actual == "0" and numero != ".":
            entrada_actual = numero
        else:
            entrada_actual += numero

        actualizar_pantalla()


    # Método para cambiar el número actual entre positivo y negativo
    def cambiar_signo():
        nonlocal entrada_actual

        if entrada_actual == "Error":
            entrada_actual = "0"

        if entrada_actual.startswith("-"):
            entrada_actual = entrada_actual[1:]
        else:
            if entrada_actual != "0":
                entrada_actual = "-" + entrada_actual

        actualizar_pantalla()


    # Método para guardar el operador seleccionado y preparar la calculadora para recibir el segundo número
    def establecer_operador(operador):
        nonlocal entrada_actual, primer_valor, operador_actual, reiniciar_pantalla

        if entrada_actual == "Error":
            return

        if operador_actual is not None and not reiniciar_pantalla:
            calcular_resultado()

        try:
            primer_valor = convertir_decimal(entrada_actual)
            operador_actual = operador
            reiniciar_pantalla = True
        except InvalidOperation:
            entrada_actual = "Error"
            actualizar_pantalla()
            mostrar_error_analisis("Debe ingresar un número válido.")


    # Método para calcular la potencia de un número usando una base y un exponente
    def calcular_potencia(base, exponente):
        try:
            if exponente == exponente.to_integral_value():
                return base ** int(exponente)

            resultado = Decimal(str(float(base) ** float(exponente)))
            return resultado

        except Exception:
            raise InvalidOperation
        

    # Método para realizar la operación seleccionada y mostrar el resultado en la pantalla
    def calcular_resultado():
        nonlocal entrada_actual, primer_valor, operador_actual, reiniciar_pantalla

        if operador_actual is None or reiniciar_pantalla:
            return

        try:
            segundo_valor = convertir_decimal(entrada_actual)
            primer_numero_operacion = primer_valor
            operador_operacion = operador_actual

            if operador_actual == "+":
                resultado = primer_valor + segundo_valor

            elif operador_actual == "-":
                resultado = primer_valor - segundo_valor

            elif operador_actual == "*":
                resultado = primer_valor * segundo_valor

            elif operador_actual == "/":
                if segundo_valor == 0:
                    entrada_actual = "Error"
                    operador_actual = None
                    primer_valor = None
                    reiniciar_pantalla = True
                    actualizar_pantalla()
                    mostrar_error_analisis("No se puede dividir para cero.")
                    return

                resultado = primer_valor / segundo_valor

            elif operador_actual == "**":
                resultado = calcular_potencia(primer_valor, segundo_valor)

            else:
                return

            if abs(resultado) > NUMERO_MAXIMO_PERMITIDO:
                messagebox.showwarning(
                    "Límite excedido",
                    f"Ha excedido el número máximo permitido ({formatear_numero(NUMERO_MAXIMO_PERMITIDO)})."
                )
                limpiar_pantalla()
                return

            entrada_actual = formatear_numero_pantalla(resultado)
            operador_actual = None
            primer_valor = None
            reiniciar_pantalla = True

            actualizar_pantalla()
            mostrar_analisis(
                primer_numero_operacion,
                operador_operacion,
                segundo_valor,
                resultado
            )

        except (InvalidOperation, ValueError, OverflowError):
            entrada_actual = "Error"
            operador_actual = None
            primer_valor = None
            reiniciar_pantalla = True
            actualizar_pantalla()
            mostrar_error_analisis("Se produjo un problema al procesar la operación.")

    # Método para calcular la raíz cuadrada del número que está actualmente en pantalla
    def calcular_raiz_cuadrada():
        nonlocal entrada_actual, reiniciar_pantalla

        try:
            numero = convertir_decimal(entrada_actual)

            if numero < 0:
                entrada_actual = "Error"
                reiniciar_pantalla = True
                actualizar_pantalla()
                mostrar_error_analisis("No se puede calcular la raíz cuadrada de un número negativo.")
                return

            resultado = Decimal(str(math.sqrt(float(numero))))

            entrada_actual = formatear_numero_pantalla(resultado)
            reiniciar_pantalla = True
            actualizar_pantalla()

            contenido = (
                f"√{formatear_numero(numero)} = {formatear_numero(resultado)}\n\n"
                f"Operación realizada: raíz cuadrada."
            )

            escribir_analisis("Resumen del cálculo:", contenido)

        except (InvalidOperation, ValueError, OverflowError):
            entrada_actual = "Error"
            reiniciar_pantalla = True
            actualizar_pantalla()
            mostrar_error_analisis("Debe ingresar un número válido.")

    # Método para limpiar la pantalla de la calculadora y reiniciar los valores de la operación actual
    def limpiar_pantalla():
        nonlocal entrada_actual, primer_valor, operador_actual, reiniciar_pantalla

        entrada_actual = "0"
        primer_valor = None
        operador_actual = None
        reiniciar_pantalla = False
        actualizar_pantalla()
        limpiar_analisis()

    # Método para cerrar la aplicación después de confirmar la acción con el usuario
    def cerrar_aplicacion():
        confirmar = messagebox.askyesno(
            "Salir",
            "¿Desea cerrar la calculadora avanzada?"
        )

        if confirmar:
            ventana.destroy()

    # Método para cerrar la calculadora actual y regresar a la ventana de inicio
    def volver_a_inicio():
        ventana.destroy()
        main()

    # Método para detectar las teclas presionadas y ejecutar la acción correspondiente en la calculadora
    def tecla_presionada(evento):
        tecla = evento.keysym
        caracter = evento.char

        if caracter.isdigit() or caracter == ".":
            agregar_numero(caracter)

        elif caracter in ["+", "-", "*", "/"]:
            establecer_operador(caracter)

        elif tecla == "Return":
            calcular_resultado()

        elif tecla == "Escape" or caracter.lower() == "c":
            limpiar_pantalla()

    
    # Método para abrir la ventana donde se gestionan las matrices  
    def abrir_ventana_matrices():

        ventana_matrices = tk.Toplevel(ventana)
        ventana_matrices.title("Multiplicación de matrices")
        ventana_matrices.configure(bg=COLOR_FONDO)

        maximizar_ventana(ventana_matrices)

        ventana_matrices.resizable(True, True)

        ventana_matrices.transient(ventana)
        ventana_matrices.lift()
        ventana_matrices.focus_force()

        entradas_a = []
        entradas_b = []
        dimensiones_a = (0, 0)
        dimensiones_b = (0, 0)


        # Método para mostrar mensajes o resultados dentro del panel de matrices
        def escribir_panel_matrices(titulo, contenido):
            caja_matrices.config(state="normal")
            caja_matrices.delete("1.0", tk.END)
            caja_matrices.insert(tk.END, titulo + "\n", "titulo")
            caja_matrices.insert(tk.END, contenido, "normal")
            caja_matrices.config(state="disabled")


        # Método para leer y validar que una dimensión ingresada sea un número entero positivo
        def leer_dimension(entrada, nombre):
            texto = entrada.get().strip()

            try:
                numero = int(texto)

                if numero <= 0:
                    raise ValueError

                return numero

            except ValueError:
                raise ValueError(f"{nombre} debe ser un número entero mayor a cero.")

        # Método para limpiar todos los elementos visuales dentro de un contenedor
        def limpiar_frame(frame):
            for widget in frame.winfo_children():
                widget.destroy()

        # Método para crear dinámicamente las casillas donde el usuario ingresará los valores de una matriz
        def crear_tabla_entradas(frame_padre, filas, columnas, nombre):
            tabla = []
            contenedor_tabla = tk.Frame(frame_padre, bg=COLOR_PANEL_SECUNDARIO)
            contenedor_tabla.pack(pady=10)

            tk.Label(
                contenedor_tabla,
                text="",
                bg=COLOR_PANEL_SECUNDARIO,
                fg=COLOR_TEXTO_SECUNDARIO,
                width=6
            ).grid(row=0, column=0, padx=3, pady=3)

            for columna in range(columnas):
                tk.Label(
                    contenedor_tabla,
                    text=f"C{columna + 1}",
                    bg=COLOR_PANEL_SECUNDARIO,
                    fg=COLOR_TEXTO_SECUNDARIO,
                    width=10,
                    font=("Arial", 9, "bold")
                ).grid(row=0, column=columna + 1, padx=3, pady=3)

            for fila in range(filas):
                tk.Label(
                    contenedor_tabla,
                    text=f"F{fila + 1}",
                    bg=COLOR_PANEL_SECUNDARIO,
                    fg=COLOR_TEXTO_SECUNDARIO,
                    width=6,
                    font=("Arial", 9, "bold")
                ).grid(row=fila + 1, column=0, padx=3, pady=3)

                fila_entradas = []

                for columna in range(columnas):
                    entrada = tk.Entry(
                        contenedor_tabla,
                        width=10,
                        bg=COLOR_PANEL,
                        fg=COLOR_TEXTO,
                        insertbackground=COLOR_TEXTO,
                        bd=0,
                        justify="center",
                        font=("Arial", 10)
                    )
                    entrada.grid(row=fila + 1, column=columna + 1, padx=3, pady=3, ipady=6)
                    fila_entradas.append(entrada)

                tabla.append(fila_entradas)

            return tabla

        # Método para generar las matrices en pantalla después de validar sus dimensiones
        def generar_matrices():
            nonlocal entradas_a, entradas_b, dimensiones_a, dimensiones_b

            try:
                filas_a = leer_dimension(entrada_filas_a, "Filas de la matriz A")
                columnas_a = leer_dimension(entrada_columnas_a, "Columnas de la matriz A")
                filas_b = leer_dimension(entrada_filas_b, "Filas de la matriz B")
                columnas_b = leer_dimension(entrada_columnas_b, "Columnas de la matriz B")

                # Validar compatibilidad antes de generar las matrices
                if columnas_a != filas_b:
                    messagebox.showerror(
                        "Matrices no compatibles",
                        "No se pueden generar las matrices.\n\n"
                        "Para multiplicar matrices, el número de columnas de la matriz A "
                        "debe ser igual al número de filas de la matriz B.\n\n"
                        f"Matriz A ingresada: {filas_a} x {columnas_a}\n"
                        f"Matriz B ingresada: {filas_b} x {columnas_b}",
                        parent=ventana_matrices
                    )

                    escribir_panel_matrices(
                        "Error:",
                        "No se generaron las matrices porque las dimensiones no son compatibles.\n\n"
                        "Recuerde que para multiplicar A x B, las columnas de A deben ser "
                        "iguales a las filas de B."
                    )

                    ventana_matrices.lift()
                    ventana_matrices.focus_force()
                    return

                dimensiones_a = (filas_a, columnas_a)
                dimensiones_b = (filas_b, columnas_b)

                limpiar_frame(frame_matriz_a)
                limpiar_frame(frame_matriz_b)
                limpiar_frame(frame_resultado)

                tk.Label(
                    frame_matriz_a,
                    text=f"Matriz A ({filas_a} x {columnas_a})",
                    bg=COLOR_PANEL_SECUNDARIO,
                    fg=COLOR_TEXTO,
                    font=("Arial", 12, "bold")
                ).pack(anchor="w")

                tk.Label(
                    frame_matriz_b,
                    text=f"Matriz B ({filas_b} x {columnas_b})",
                    bg=COLOR_PANEL_SECUNDARIO,
                    fg=COLOR_TEXTO,
                    font=("Arial", 12, "bold")
                ).pack(anchor="w")

                entradas_a = crear_tabla_entradas(frame_matriz_a, filas_a, columnas_a, "A")
                entradas_b = crear_tabla_entradas(frame_matriz_b, filas_b, columnas_b, "B")

                escribir_panel_matrices(
                    "Matrices generadas:",
                    "Las dimensiones son compatibles.\n\n"
                    "Ingrese los valores de ambas matrices y luego presione "
                    "'Multiplicar matrices'."
                )

            except ValueError as error:
                messagebox.showerror(
                    "Dato inválido",
                    str(error),
                    parent=ventana_matrices
                )

                ventana_matrices.lift()
                ventana_matrices.focus_force()


        # Método para leer los valores ingresados por el usuario y formar una matriz
        def leer_matriz(tabla_entradas, nombre):
            matriz = []

            for i, fila_entradas in enumerate(tabla_entradas):
                fila = []

                for j, entrada in enumerate(fila_entradas):
                    texto = entrada.get().strip()

                    try:
                        numero = convertir_decimal(texto)
                        fila.append(numero)

                    except InvalidOperation:
                        raise ValueError(
                            f"El valor de la matriz {nombre} en la posición "
                            f"[{i + 1}][{j + 1}] no es válido."
                        )

                matriz.append(fila)

            return matriz

        # Método para mostrar en pantalla la matriz resultante de la multiplicación
        def mostrar_matriz_resultado(matriz):
            limpiar_frame(frame_resultado)

            tk.Label(
                frame_resultado,
                text="Resultado de la multiplicación",
                bg=COLOR_PANEL_SECUNDARIO,
                fg=COLOR_TEXTO,
                font=("Arial", 12, "bold")
            ).pack(anchor="w", pady=(0, 10))

            contenedor_tabla = tk.Frame(frame_resultado, bg=COLOR_PANEL_SECUNDARIO)
            contenedor_tabla.pack(pady=5)

            for i, fila in enumerate(matriz):
                for j, valor in enumerate(fila):
                    etiqueta = tk.Label(
                        contenedor_tabla,
                        text=formatear_numero(valor),
                        bg=COLOR_BOTON_NUMERO,
                        fg=COLOR_TEXTO,
                        width=14,
                        height=2,
                        font=("Arial", 10, "bold")
                    )
                    etiqueta.grid(row=i, column=j, padx=4, pady=4)


        # Método para multiplicar las matrices ingresadas y mostrar el resultado obtenido
        def multiplicar_matrices_ingresadas():
            nonlocal dimensiones_a, dimensiones_b

            if not entradas_a or not entradas_b:
                messagebox.showwarning(
                    "Matrices no generadas",
                    "Primero debe generar las matrices.",
                    parent=ventana_matrices
                )

                ventana_matrices.lift()
                ventana_matrices.focus_force()
                return

            try:
                matriz_a = leer_matriz(entradas_a, "A")
                matriz_b = leer_matriz(entradas_b, "B")

                filas_a = len(matriz_a)
                columnas_a = len(matriz_a[0])
                filas_b = len(matriz_b)
                columnas_b = len(matriz_b[0])

                if columnas_a != filas_b:
                    escribir_panel_matrices(
                        "Error:",
                        "No se pueden multiplicar las matrices.\n\n"
                        "El número de columnas de la matriz A debe ser igual "
                        "al número de filas de la matriz B."
                    )
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

                mostrar_matriz_resultado(resultado)

                escribir_panel_matrices(
                    "Resumen de la multiplicación:",
                    f"Matriz A: {filas_a} x {columnas_a}\n"
                    f"Matriz B: {filas_b} x {columnas_b}\n"
                    f"Matriz resultado: {filas_a} x {columnas_b}\n\n"
                    "La operación se realizó correctamente."
                )

                escribir_analisis(
                    "Operación con matrices:",
                    f"Se multiplicó una matriz A de tamaño {filas_a} x {columnas_a} "
                    f"por una matriz B de tamaño {filas_b} x {columnas_b}.\n\n"
                    f"El resultado es una matriz de tamaño {filas_a} x {columnas_b}."
                )

            except ValueError as error:
                messagebox.showerror(
                    "Dato inválido",
                    str(error),
                    parent=ventana_matrices
                )

                ventana_matrices.lift()
                ventana_matrices.focus_force()


        # Método para limpiar los datos ingresados y reiniciar la ventana de matrices
        def limpiar_matrices():
            nonlocal entradas_a, entradas_b, dimensiones_a, dimensiones_b

            entradas_a = []
            entradas_b = []
            dimensiones_a = (0, 0)
            dimensiones_b = (0, 0)

            entrada_filas_a.delete(0, tk.END)
            entrada_columnas_a.delete(0, tk.END)
            entrada_filas_b.delete(0, tk.END)
            entrada_columnas_b.delete(0, tk.END)

            limpiar_frame(frame_matriz_a)
            limpiar_frame(frame_matriz_b)
            limpiar_frame(frame_resultado)

            escribir_panel_matrices(
                "Panel de matrices:",
                "Aquí se mostrará el análisis de la multiplicación de matrices."
            )


        # Método para cerrar la ventana de matrices y regresar a la calculadora principal
        def volver_inicio_matrices():
            ventana_matrices.destroy()

        # Contenedor con scroll
        canvas = tk.Canvas(ventana_matrices, bg=COLOR_FONDO, highlightthickness=0)
        scrollbar = tk.Scrollbar(ventana_matrices, orient="vertical", command=canvas.yview)
        contenido = tk.Frame(canvas, bg=COLOR_FONDO)

        contenido.bind(
            "<Configure>",
            lambda evento: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        ventana_contenido = canvas.create_window((0, 0), window=contenido, anchor="nw")


        # Método para ajustar el ancho del contenido cuando cambia el tamaño de la ventana
        def ajustar_ancho_contenido(evento):
            canvas.itemconfig(ventana_contenido, width=evento.width)

        canvas.bind("<Configure>", ajustar_ancho_contenido)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        titulo = tk.Label(
            contenido,
            text="Multiplicación de matrices",
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO,
            font=("Arial", 18, "bold")
        )
        titulo.pack(anchor="w", padx=20, pady=(20, 10))

        panel_superior = tk.Frame(contenido, bg=COLOR_PANEL, padx=20, pady=20)
        panel_superior.pack(fill="x", padx=20, pady=10)

        tk.Label(
            panel_superior,
            text="Matriz A",
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO,
            font=("Arial", 12, "bold")
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        tk.Label(
            panel_superior,
            text="Filas:",
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO_SECUNDARIO
        ).grid(row=1, column=0, sticky="w", padx=(0, 8))

        entrada_filas_a = tk.Entry(
            panel_superior,
            width=8,
            bg=COLOR_PANEL_SECUNDARIO,
            fg=COLOR_TEXTO,
            insertbackground=COLOR_TEXTO,
            bd=0,
            justify="center"
        )
        entrada_filas_a.grid(row=1, column=1, ipady=6, padx=(0, 20))

        tk.Label(
            panel_superior,
            text="Columnas:",
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO_SECUNDARIO
        ).grid(row=1, column=2, sticky="w", padx=(0, 8))

        entrada_columnas_a = tk.Entry(
            panel_superior,
            width=8,
            bg=COLOR_PANEL_SECUNDARIO,
            fg=COLOR_TEXTO,
            insertbackground=COLOR_TEXTO,
            bd=0,
            justify="center"
        )
        entrada_columnas_a.grid(row=1, column=3, ipady=6, padx=(0, 35))

        tk.Label(
            panel_superior,
            text="Matriz B",
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO,
            font=("Arial", 12, "bold")
        ).grid(row=0, column=4, columnspan=2, sticky="w", pady=(0, 8))

        tk.Label(
            panel_superior,
            text="Filas:",
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO_SECUNDARIO
        ).grid(row=1, column=4, sticky="w", padx=(0, 8))

        entrada_filas_b = tk.Entry(
            panel_superior,
            width=8,
            bg=COLOR_PANEL_SECUNDARIO,
            fg=COLOR_TEXTO,
            insertbackground=COLOR_TEXTO,
            bd=0,
            justify="center"
        )
        entrada_filas_b.grid(row=1, column=5, ipady=6, padx=(0, 20))

        tk.Label(
            panel_superior,
            text="Columnas:",
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO_SECUNDARIO
        ).grid(row=1, column=6, sticky="w", padx=(0, 8))

        entrada_columnas_b = tk.Entry(
            panel_superior,
            width=8,
            bg=COLOR_PANEL_SECUNDARIO,
            fg=COLOR_TEXTO,
            insertbackground=COLOR_TEXTO,
            bd=0,
            justify="center"
        )
        entrada_columnas_b.grid(row=1, column=7, ipady=6, padx=(0, 20))

        boton_generar = tk.Button(
            panel_superior,
            text="Generar matrices",
            bg=COLOR_BOTON_IGUAL,
            fg="#111",
            font=("Arial", 10, "bold"),
            relief="flat",
            command=generar_matrices,
            cursor="hand2"
        )
        boton_generar.grid(row=1, column=8, padx=8, ipadx=10, ipady=6)

        boton_multiplicar = tk.Button(
            panel_superior,
            text="Multiplicar matrices",
            bg=COLOR_BOTON_OPERADOR,
            fg=COLOR_TEXTO,
            font=("Arial", 10, "bold"),
            relief="flat",
            command=multiplicar_matrices_ingresadas,
            cursor="hand2"
        )
        boton_multiplicar.grid(row=1, column=9, padx=8, ipadx=10, ipady=6)

        boton_limpiar = tk.Button(
            panel_superior,
            text="Limpiar",
            bg=COLOR_BOTON_IGUAL,
            fg="#111",
            font=("Arial", 10, "bold"),
            relief="flat",
            command=limpiar_matrices,
            cursor="hand2"
        )
        boton_limpiar.grid(row=1, column=10, padx=8, ipadx=10, ipady=6)


        boton_volver_matrices = tk.Button(
            panel_superior,
            text="Volver a inicio",
            bg=COLOR_BOTON_ERROR,
            fg=COLOR_TEXTO,
            font=("Arial", 10, "bold"),
            relief="flat",
            command=volver_inicio_matrices,
            cursor="hand2"
        )
        boton_volver_matrices.grid(row=1, column=11, padx=8, ipadx=10, ipady=6)

        panel_matrices = tk.Frame(contenido, bg=COLOR_FONDO)
        panel_matrices.pack(fill="both", expand=True, padx=20, pady=10)

        frame_izquierdo = tk.Frame(panel_matrices, bg=COLOR_FONDO)
        frame_izquierdo.pack(side="left", fill="both", expand=True, padx=(0, 20))

        frame_derecho = tk.Frame(panel_matrices, bg=COLOR_PANEL_SECUNDARIO, padx=20, pady=20)
        frame_derecho.pack(side="left", fill="y")

        frame_matriz_a = tk.Frame(frame_izquierdo, bg=COLOR_PANEL_SECUNDARIO, padx=20, pady=20)
        frame_matriz_a.pack(fill="x", pady=(0, 15))

        frame_matriz_b = tk.Frame(frame_izquierdo, bg=COLOR_PANEL_SECUNDARIO, padx=20, pady=20)
        frame_matriz_b.pack(fill="x", pady=(0, 15))

        frame_resultado = tk.Frame(frame_izquierdo, bg=COLOR_PANEL_SECUNDARIO, padx=20, pady=20)
        frame_resultado.pack(fill="x", pady=(0, 15))

        caja_matrices = tk.Text(
            frame_derecho,
            width=38,
            height=24,
            bg=COLOR_PANEL_SECUNDARIO,
            fg=COLOR_TEXTO_SECUNDARIO,
            bd=0,
            wrap="word",
            font=("Arial", 11),
            spacing3=8
        )
        caja_matrices.pack(fill="both", expand=True)

        caja_matrices.tag_configure("titulo", foreground=COLOR_TEXTO, font=("Arial", 12, "bold"))
        caja_matrices.tag_configure("normal", foreground=COLOR_TEXTO_SECUNDARIO, font=("Arial", 11))

        escribir_panel_matrices(
            "Panel de matrices:",
            "1. Ingrese las dimensiones de la matriz A y B.\n"
            "2. Presione 'Generar matrices'.\n"
            "3. Escriba los valores.\n"
            "4. Presione 'Multiplicar matrices'."
        )

    # Código para iniciar la construcción de la calculadora en la inetrfaz del ususario
    contenedor_general = tk.Frame(ventana, bg=COLOR_FONDO)
    contenedor_general.pack(fill="both", expand=True)

    header = tk.Frame(contenedor_general, bg=COLOR_FONDO)
    header.pack(fill="x", padx=20, pady=15)

    top_bar = tk.Frame(header, bg=COLOR_FONDO)
    top_bar.pack(fill="x")

    saludo = tk.Label(
        top_bar,
        text=f"Hola, {nombre_usuario}",
        bg=COLOR_PANEL_SECUNDARIO,
        fg=COLOR_TEXTO,
        font=("Arial", 12, "bold"),
        padx=14,
        pady=10,
        anchor="w"
    )
    saludo.pack(side="left", fill="x", expand=True)

    boton_volver = tk.Button(
        top_bar,
        text="Volver a inicio",
        bg=COLOR_BOTON_ERROR,
        fg=COLOR_TEXTO,
        font=("Arial", 10, "bold"),
        relief="flat",
        padx=14,
        pady=10,
        command=volver_a_inicio,
        cursor="hand2"
    )
    boton_volver.pack(side="right", padx=(12, 0))

    boton_salir = tk.Button(
        top_bar,
        text="Salir",
        bg=COLOR_BOTON_OPERADOR,
        fg=COLOR_TEXTO,
        font=("Arial", 10, "bold"),
        relief="flat",
        padx=14,
        pady=10,
        command=cerrar_aplicacion,
        cursor="hand2"
    )
    boton_salir.pack(side="right", padx=(12, 0))

    main_content = tk.Frame(contenedor_general, bg=COLOR_FONDO)
    main_content.pack(fill="both", expand=True, padx=20, pady=10)

    zona_central = tk.Frame(main_content, bg=COLOR_FONDO)
    zona_central.pack(fill="both", expand=True)

    panel_principal = tk.Frame(zona_central, bg=COLOR_FONDO)
    panel_principal.place(relx=0.5, rely=0.5, anchor="center")

    contenedor_calculadora = tk.Frame(panel_principal, bg=COLOR_FONDO)
    contenedor_calculadora.pack(side="left", padx=(0, 20), anchor="n")

    calculator = tk.Frame(
        contenedor_calculadora,
        bg=COLOR_PANEL,
        padx=20,
        pady=20
    )
    calculator.pack()

    display = tk.Entry(
        calculator,
        textvariable=variable_pantalla,
        font=("Arial", 34),
        justify="right",
        bd=0,
        relief="flat",
        bg=COLOR_PANEL_SECUNDARIO,
        fg=COLOR_TEXTO,
        readonlybackground=COLOR_PANEL_SECUNDARIO
    )
    display.configure(state="readonly")
    display.pack(fill="x", pady=(0, 18), ipady=18)

    buttons_frame = tk.Frame(calculator, bg=COLOR_PANEL)
    buttons_frame.pack(fill="both", expand=True)

    botones = [
        ("AC", 0, 0, 1, COLOR_BOTON_ERROR, limpiar_pantalla),
        ("±", 0, 1, 1, COLOR_BOTON_OPERADOR, cambiar_signo),
        ("√", 0, 2, 1, COLOR_BOTON_OPERADOR, calcular_raiz_cuadrada),
        ("÷", 0, 3, 1, COLOR_BOTON_OPERADOR, lambda: establecer_operador("/")),

        ("7", 1, 0, 1, COLOR_BOTON_NUMERO, lambda: agregar_numero("7")),
        ("8", 1, 1, 1, COLOR_BOTON_NUMERO, lambda: agregar_numero("8")),
        ("9", 1, 2, 1, COLOR_BOTON_NUMERO, lambda: agregar_numero("9")),
        ("×", 1, 3, 1, COLOR_BOTON_OPERADOR, lambda: establecer_operador("*")),

        ("4", 2, 0, 1, COLOR_BOTON_NUMERO, lambda: agregar_numero("4")),
        ("5", 2, 1, 1, COLOR_BOTON_NUMERO, lambda: agregar_numero("5")),
        ("6", 2, 2, 1, COLOR_BOTON_NUMERO, lambda: agregar_numero("6")),
        ("−", 2, 3, 1, COLOR_BOTON_OPERADOR, lambda: establecer_operador("-")),

        ("1", 3, 0, 1, COLOR_BOTON_NUMERO, lambda: agregar_numero("1")),
        ("2", 3, 1, 1, COLOR_BOTON_NUMERO, lambda: agregar_numero("2")),
        ("3", 3, 2, 1, COLOR_BOTON_NUMERO, lambda: agregar_numero("3")),
        ("+", 3, 3, 1, COLOR_BOTON_OPERADOR, lambda: establecer_operador("+")),

        ("0", 4, 0, 1, COLOR_BOTON_NUMERO, lambda: agregar_numero("0")),
        (".", 4, 1, 1, COLOR_BOTON_NUMERO, lambda: agregar_numero(".")),
        ("xʸ", 4, 2, 1, COLOR_BOTON_OPERADOR, lambda: establecer_operador("**")),
        ("=", 4, 3, 1, COLOR_BOTON_IGUAL, calcular_resultado),

        ("Matrices", 5, 0, 4, COLOR_BOTON_OPERADOR, abrir_ventana_matrices),
    ]

    for texto, fila, columna, colspan, color, comando in botones:
        fg_color = "#111" if texto == "=" else COLOR_TEXTO

        boton = tk.Button(
            buttons_frame,
            text=texto,
            bg=color,
            fg=fg_color,
            font=("Arial", 16, "bold"),
            relief="flat",
            width=5,
            height=2,
            command=comando,
            cursor="hand2",
            activebackground=color,
            activeforeground=fg_color
        )
        boton.grid(
            row=fila,
            column=columna,
            columnspan=colspan,
            padx=6,
            pady=6,
            sticky="nsew"
        )

    for fila in range(6):
        buttons_frame.grid_rowconfigure(fila, weight=1)

    for columna in range(4):
        buttons_frame.grid_columnconfigure(columna, weight=1)

    panel_analisis = tk.Frame(
        panel_principal,
        bg=COLOR_PANEL_SECUNDARIO,
        padx=20,
        pady=20
    )
    panel_analisis.pack(side="left", anchor="n")

    caja_analisis = tk.Text(
        panel_analisis,
        width=42,
        height=18,
        bg=COLOR_PANEL_SECUNDARIO,
        fg=COLOR_TEXTO_SECUNDARIO,
        bd=0,
        wrap="word",
        font=("Arial", 12),
        spacing3=8
    )
    caja_analisis.pack(fill="both", expand=True)

    caja_analisis.tag_configure("titulo", foreground=COLOR_TEXTO, font=("Arial", 12, "bold"))
    caja_analisis.tag_configure("normal", foreground=COLOR_TEXTO_SECUNDARIO, font=("Arial", 12))

    limpiar_analisis()

    ventana.bind("<Key>", tecla_presionada)
    ventana.mainloop()


# Método para crear la ventana de bienvenida y para solicitar el nombre del usuario
def iniciar_calculadora(event=None):
    global nombre_usuario

    nombre = entrada_nombre.get().strip()
    mensaje_error.config(text="")

    if nombre == "":
        mensaje_error.config(text="Por favor, ingrese su nombre.")
        return

    if len(nombre) < 5:
        mensaje_error.config(text="El nombre debe tener mínimo 5 caracteres.")
        return

    if len(nombre) > 25:
        mensaje_error.config(text="El nombre no debe superar los 25 caracteres.")
        return

    nombre_usuario = nombre

    ventana_bienvenida.destroy()
    abrir_calculadora()



# Método para ejecutar la ventana inicial luego de la ventana de bienvenida
def main():
    global ventana_bienvenida, entrada_nombre, mensaje_error

    ventana_bienvenida = tk.Tk()
    ventana_bienvenida.title("Bienvenida")
    ventana_bienvenida.configure(bg=COLOR_FONDO)
    maximizar_ventana(ventana_bienvenida)

    contenedor_principal = tk.Frame(ventana_bienvenida, bg=COLOR_FONDO)
    contenedor_principal.pack(fill="both", expand=True)

    marco = tk.Frame(
        contenedor_principal,
        bg=COLOR_PANEL,
        padx=25,
        pady=25
    )
    marco.place(relx=0.5, rely=0.5, anchor="center")

    titulo = tk.Label(
        marco,
        text="Bienvenido",
        bg=COLOR_PANEL,
        fg=COLOR_TEXTO,
        font=("Arial", 18, "bold")
    )
    titulo.pack(pady=(0, 20))

    etiqueta = tk.Label(
        marco,
        text="Ingrese su nombre",
        bg=COLOR_PANEL,
        fg=COLOR_TEXTO_SECUNDARIO,
        font=("Arial", 11)
    )
    etiqueta.pack(anchor="w", pady=(0, 8))

    entrada_nombre = tk.Entry(
        marco,
        width=28,
        font=("Arial", 12),
        bd=0,
        bg=COLOR_PANEL_SECUNDARIO,
        fg=COLOR_TEXTO,
        insertbackground=COLOR_TEXTO
    )
    entrada_nombre.pack(fill="x", ipady=8, pady=(0, 15))

    boton = tk.Button(
        marco,
        text="Continuar",
        bg=COLOR_BOTON_IGUAL,
        fg="#111",
        font=("Arial", 11, "bold"),
        relief="flat",
        command=iniciar_calculadora,
        cursor="hand2"
    )
    boton.pack(fill="x", ipady=8)

    mensaje_error = tk.Label(
        marco,
        text="",
        bg=COLOR_PANEL,
        fg=COLOR_BOTON_ERROR,
        font=("Arial", 10)
    )
    mensaje_error.pack(pady=(15, 0))

    ventana_bienvenida.bind("<Return>", iniciar_calculadora)
    ventana_bienvenida.mainloop()


main()