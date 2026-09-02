import tkinter as tk


def iniciar_aplicacion():

    ventana = tk.Tk()

    ventana.title("Simulador de Autómatas")

    ventana.geometry("1000x650")

    ventana.minsize(900, 600)

    titulo = tk.Label(
        ventana,
        text="SIMULADOR DE AUTÓMATAS",
        font=("Arial", 22, "bold")
    )

    titulo.pack(pady=25)

    subtitulo = tk.Label(
        ventana,
        text="Autómatas Finitos Deterministas y No Deterministas",
        font=("Arial", 13)
    )

    subtitulo.pack()

    ventana.mainloop()