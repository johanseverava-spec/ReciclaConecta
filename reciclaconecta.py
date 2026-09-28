import tkinter as tk
from tkinter import ttk, messagebox

VERDE = "#2e7d32"
VERDE_CLARO = "#e8f5e9"
FONDO = "#eef2ef"
BLANCO = "#ffffff"

BARRIOS = [
    "Kennedy - Sector 4",
    "Kennedy - Sector 3",
    "Kennedy - Sector 5",
    "Bosa - Sector 1",
    "Barrio Centro",
]

# (texto del botón, valor guardado)
MATERIALES = [
    ("📦 Cartón (Caja)", "Cartón (Caja)"),
    ("🧴 Plástico (Botella)", "Plástico (Botella)"),
    ("🍾 Vidrio", "Vidrio"),
    ("🥫 Metal (Lata)", "Metal (Lata)"),
]

# Kg estimados por recolección (para el contador de impacto)
KG_POR_MATERIAL = {
    "Cartón (Caja)": 15,
    "Plástico (Botella)": 8,
    "Vidrio": 12,
    "Metal (Lata)": 6,
}

ventana = tk.Tk()
ventana.title("ReciclaConecta")
ventana.geometry("420x640")
ventana.resizable(False, False)
ventana.configure(bg=FONDO)


barrio = tk.StringVar(value=BARRIOS[0])
material = tk.StringVar(value="Cartón (Caja)")
direccion = tk.StringVar(value="Calle 42 # 10-15")
horario = tk.StringVar(value="Hoy 2pm - 6pm")
filtro_barrio = tk.StringVar(value="Todos los barrios")

avisos = [
    {
        "barrio": "Barrio Centro",
        "material": "Cartón (Caja)",
        "direccion": "Cra 68 # 25-30",
        "horario": "Mañana",
        "tiempo": "Hace 10 min",
    },
    {
        "barrio": "Kennedy - Sector 4",
        "material": "Plástico (Botella)",
        "direccion": "Calle 38 # 78-12",
        "horario": "Hoy 4pm - 6pm",
        "tiempo": "Hace 25 min",
    },
]

estado = {
    "ultimo_kg": None,       # kg de la última recolección confirmada
    "ultimo_aviso": None,    # aviso de la última recolección
    "total_kg": 0,           # acumulado de kg desviados
}


def limpiar_pantalla():
    """Elimina todos los elementos de la pantalla."""
    for widget in ventana.winfo_children():
        widget.destroy()


def crear_encabezado():
    """Título de la aplicación."""
    tk.Label(
        ventana,
        text="♻ ReciclaConecta",
        font=("Arial", 16, "bold"),
        fg=VERDE,
        bg=FONDO,
    ).pack(pady=(15, 0))


def crear_botones_superiores(paso):
    """Crea los botones de navegación superiores."""
    marco = tk.Frame(ventana, bg=FONDO)
    marco.pack(pady=12)

    botones = [
        ("1. Publicar", mostrar_publicar),
        ("2. Tablero", mostrar_tablero),
        ("3. Confirmar", ir_a_confirmar),
    ]

    for i, (texto, funcion) in enumerate(botones):
        if i + 1 == paso:
            boton = tk.Button(
                marco,
                text=texto,
                command=funcion,
                bg=VERDE,
                fg="white",
                relief="flat",
                padx=15,
                pady=7,
            )
        else:
            boton = tk.Button(
                marco,
                text=texto,
                command=funcion,
                bg=BLANCO,
                fg="black",
                relief="solid",
                padx=15,
                pady=7,
            )
        boton.grid(row=0, column=i, padx=3)



def mostrar_publicar():
    limpiar_pantalla()
    crear_encabezado()
    crear_botones_superiores(1)

    marco = tk.LabelFrame(
        ventana,
        text="Publicar residuo",
        font=("Arial", 10, "bold"),
        fg=VERDE,
        bg=BLANCO,
        padx=15,
        pady=15,
    )
    marco.pack(padx=30, fill="both")

    # Barrio
    tk.Label(marco, text="Barrio / Sector", bg=BLANCO).pack(anchor="w")
    combo_barrio = ttk.Combobox(
        marco,
        textvariable=barrio,
        values=BARRIOS,
        state="readonly",
    )
    combo_barrio.pack(fill="x", pady=(5, 12))

    # Dirección
    tk.Label(marco, text="Dirección", bg=BLANCO).pack(anchor="w")
    tk.Entry(marco, textvariable=direccion).pack(fill="x", pady=(5, 12))

    # Materiales (2 x 2)
    tk.Label(marco, text="Selecciona los materiales", bg=BLANCO).pack(anchor="w")
    marco_material = tk.Frame(marco, bg=BLANCO)
    marco_material.pack(fill="x", pady=5)

    for i, (texto, valor) in enumerate(MATERIALES):
        tk.Radiobutton(
            marco_material,
            text=texto,
            variable=material,
            value=valor,
            indicatoron=False,
            bg=VERDE_CLARO,
            fg="black",
            selectcolor=VERDE,
            activebackground=VERDE,
            relief="flat",
            pady=10,
            width=16,
        ).grid(row=i // 2, column=i % 2, padx=3, pady=3, sticky="ew")

    marco_material.columnconfigure(0, weight=1)
    marco_material.columnconfigure(1, weight=1)

    # Horario
    tk.Label(marco, text="Horario disponible", bg=BLANCO).pack(
        anchor="w", pady=(10, 3)
    )
    tk.Entry(marco, textvariable=horario).pack(fill="x")

    # Botón enviar
    tk.Button(
        marco,
        text="Enviar Aviso",
        command=publicar_aviso,
        bg=VERDE,
        fg="white",
        font=("Arial", 11, "bold"),
        relief="flat",
        pady=8,
    ).pack(fill="x", pady=(20, 5))


def publicar_aviso():
    if direccion.get().strip() == "" or horario.get().strip() == "":
        messagebox.showwarning(
            "Datos incompletos",
            "Por favor completa todos los campos.",
        )
        return

    avisos.insert(
        0,
        {
            "barrio": barrio.get(),
            "material": material.get(),
            "direccion": direccion.get().strip(),
            "horario": horario.get().strip(),
            "tiempo": "Hace 1 min",
        },
    )

    messagebox.showinfo(
        "Aviso publicado",
        "El aviso fue publicado correctamente.",
    )

    filtro_barrio.set("Todos los barrios")
    mostrar_tablero()



def mostrar_tablero():
    limpiar_pantalla()
    crear_encabezado()
    crear_botones_superiores(2)

    marco = tk.LabelFrame(
        ventana,
        text="Solicitudes cercanas",
        font=("Arial", 10, "bold"),
        fg=VERDE,
        bg=BLANCO,
        padx=15,
        pady=15,
    )
    marco.pack(padx=30, fill="both", expand=True, pady=(0, 15))

    tk.Label(marco, text="Selecciona Barrio", bg=BLANCO).pack(anchor="w")

    combo_filtro = ttk.Combobox(
        marco,
        textvariable=filtro_barrio,
        values=["Todos los barrios"] + BARRIOS,
        state="readonly",
    )
    combo_filtro.pack(fill="x", pady=(5, 10))

    lista = tk.Frame(marco, bg=BLANCO)
    lista.pack(fill="both", expand=True)

    # Al cambiar el filtro solo se redibuja la lista
    combo_filtro.bind(
        "<<ComboboxSelected>>", lambda evento: dibujar_lista(lista)
    )

    dibujar_lista(lista)


def dibujar_lista(contenedor):
    """Dibuja las solicitudes abiertas según el barrio elegido."""
    for widget in contenedor.winfo_children():
        widget.destroy()

    if filtro_barrio.get() == "Todos los barrios":
        visibles = avisos
    else:
        visibles = [a for a in avisos if a["barrio"] == filtro_barrio.get()]

    if not visibles:
        tk.Label(
            contenedor,
            text="No hay solicitudes abiertas en este barrio.",
            bg=BLANCO,
            fg="gray",
        ).pack(pady=20)
        return

    for aviso in visibles:
        tarjeta = tk.Frame(
            contenedor,
            relief="solid",
            borderwidth=1,
            bg=BLANCO,
            padx=10,
            pady=8,
        )
        tarjeta.pack(fill="x", pady=4)

        tk.Label(
            tarjeta,
            text=aviso["barrio"],
            font=("Arial", 10, "bold"),
            bg=BLANCO,
        ).pack(anchor="w")

        tk.Label(
            tarjeta,
            text=f"{aviso['material']} · {aviso['direccion']}",
            bg=BLANCO,
        ).pack(anchor="w")

        tk.Label(
            tarjeta,
            text=f"{aviso['horario']} · {aviso['tiempo']}",
            font=("Arial", 8),
            fg="gray",
            bg=BLANCO,
        ).pack(anchor="w")


        tk.Button(
            tarjeta,
            text="Tomar Ruta",
            command=lambda a=aviso: tomar_ruta(a),
            bg=VERDE,
            fg="white",
            relief="flat",
            pady=4,
        ).pack(fill="x", pady=(8, 0))


def tomar_ruta(aviso):
    """El reciclador toma la solicitud y se confirma la recolección."""
    kg = KG_POR_MATERIAL.get(aviso["material"], 10)

    estado["ultimo_kg"] = kg
    estado["ultimo_aviso"] = aviso
    estado["total_kg"] += kg

    avisos.remove(aviso)
    mostrar_confirmar()


def ir_a_confirmar():
    """Se usa desde el botón superior: solo entra si hay una recolección."""
    if estado["ultimo_aviso"] is None:
        messagebox.showinfo(
            "Sin recolección",
            "Primero toma una ruta desde el tablero.",
        )
        return
    mostrar_confirmar()


def mostrar_confirmar():
    limpiar_pantalla()
    crear_encabezado()
    crear_botones_superiores(3)

    aviso = estado["ultimo_aviso"]

    marco = tk.LabelFrame(
        ventana,
        bg=BLANCO,
        padx=15,
        pady=25,
    )
    marco.pack(padx=30, pady=(0, 15), fill="both", expand=True)

    tk.Label(
        marco,
        text="✓",
        font=("Arial", 40, "bold"),
        fg=VERDE,
        bg=BLANCO,
    ).pack(pady=5)

    tk.Label(
        marco,
        text="¡Recolección Exitosa!",
        font=("Arial", 15, "bold"),
        fg=VERDE,
        bg=BLANCO,
    ).pack(pady=5)

    tk.Label(
        marco,
        text=f"{aviso['direccion']} · {aviso['material']}",
        bg=BLANCO,
    ).pack()

    # Cuadro de impacto
    marco_total = tk.Frame(marco, bg=VERDE_CLARO, padx=20, pady=15)
    marco_total.pack(fill="x", pady=20)

    tk.Label(
        marco_total,
        text=f"Has ayudado a recuperar {estado['ultimo_kg']} kg de material",
        bg=VERDE_CLARO,
    ).pack()

    tk.Label(
        marco_total,
        text=f"{estado['total_kg']} kg",
        font=("Arial", 22, "bold"),
        fg=VERDE,
        bg=VERDE_CLARO,
    ).pack(pady=5)

    tk.Label(
        marco_total,
        text="Total desviado del vertedero",
        bg=VERDE_CLARO,
    ).pack()

    # Botón volver
    tk.Button(
        marco,
        text="Ver tablero principal",
        command=mostrar_tablero,
        bg=BLANCO,
        pady=8,
    ).pack(fill="x")


mostrar_publicar()
ventana.mainloop()