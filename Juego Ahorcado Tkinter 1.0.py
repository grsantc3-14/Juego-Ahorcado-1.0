##Juego Ahorcado Tkinter
from tkinter import *
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog # Importar filedialog
from random import choice
import json # Importar JSON para guardar/cargar datos
import os # Importar OS (para manejo de archivos)

root = tk.Tk()
root.title("Juego del Ahorcado")
C = Canvas(root, bg="white",height=400, width=600)

#Variables
botonR1=None
botonR2=None
botonInicio=None
letreroOp=None
v=IntVar()
inputFrame=None
e1=None #Campo de entrada
letreroPalabra=None #Mostrar guiones
letreroVidas=None #Mostrar vidas
letreroNombre=None
letreroRonda=None
botonGuardar=None # Referencia al nuevo botón de guardar

#Variables juego
contador=0
vidas=3
continuar="s"
palabraJugar=""
palabraGuion=[]
numeroRonda=1
nombreJugadorActual="Anónimo" # Variable para guardar el nombre del jugador

#Función de inicio de juego
def iniciar_juego():
    print("Hola Sigo Funcionando") #Prueba de errores
    botonInicio.place_forget()
    configurar_juego()
    mostrarLetreroRonda()
    # Mostrar el botón de guardar una vez iniciado el juego
    botonGuardar.place(relx=0.1, rely=0.9, anchor=tk.CENTER) 

#Botones de inicio de juego
def configurar_juego():
    global botonR1, botonR2, v,letreroOp
    #Limpiar canvas
    limpiarCanvas()
    #Leyenda
    letreroOp=C.create_text(310,80, text="Elije una opción", font=("Helvetica", 16, "bold"), anchor="center")
    botonR1=tk.Radiobutton(C,text="Color", variable=v, value=1, command=jugar_ronda)
    botonR2=tk.Radiobutton(C,text="Animal", variable=v, value=2, command=jugar_ronda)
    #Ubicacion de botones
    botonR1.place(relx=0.5,rely=0.3, anchor=tk.CENTER)
    botonR2.place(relx=0.51,rely=0.35, anchor=tk.CENTER)

#Funcion de botones de ronda
def mostrarLetreroRonda():
    global letreroRonda, numeroRonda
    if letreroRonda:
        C.delete(letreroRonda)
    letreroRonda=C.create_text(590, 10, text=f"Ronda: {numeroRonda}", font=("Helvetica", 10), anchor="ne")

#Función para limpiar canvas de letreros
def limpiarCanvas():
    global inputFrame, letreroPalabra, letreroVidas
    elementosJuego = [letreroPalabra, letreroVidas, letreroOp]
    for item in elementosJuego:
        if item:
            C.delete(item)
    if inputFrame:
        inputFrame.destroy()
    for item_id in C.find_withtag("message_temp"):
        C.delete(item_id)

#Función para guardar partida
def GuardarPartida():
    global nombreJugadorActual, numeroRonda, vidas, palabraJugar, palabraGuion
    
    #Diccionario para guardar datos del juego
    datosJuego = {
        "nombreJugador": nombreJugadorActual,
        "numeroRonda": numeroRonda,
        "vidasRestantes": vidas,
        "palabraSecreta": palabraJugar,
    }
    #Abre un cuadro de diálogo para que el usuario elija la ubicación y nombre del archivo
    #Se sugiere la extensión .json
    archivo_destino = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")],
        title="Guardar Partida de Juego de Ahorcado"
    )
    if archivo_destino:
        try:
            with open(archivo_destino, 'w') as f:
                json.dump(datosJuego, f, indent=4)
            messagebox.showinfo("Guardado Exitoso", f"La partida se ha guardado en:\n{os.path.basename(archivo_destino)}")
        except Exception as e:
            messagebox.showerror("Error al Guardar", f"Ocurrió un error: {e}")

#Botones
botonInicio=tk.Button(C, text="Iniciar Juego", pady=5,command=iniciar_juego)
botonInicio.place(relx=0.5,rely=0.3, anchor=tk.CENTER)
botonExit=tk.Button(C, text="Salir y reiniciar", pady=5,command=root.destroy)
botonExit.place(relx=0.9,rely=0.9, anchor=tk.CENTER)
botonGuardar=tk.Button(C, text="Guardar Partida", pady=5,command=GuardarPartida)

#Temporizador para borrar mensajes de error
def borrarMensaje(itemId):
    C.addtag_withtag("message_temp", itemId)
    root.after(1500, lambda:C.delete(itemId))

#Función de inicio de ronda
def jugar_ronda():
    
    global palabraJugar, palabraGuion, vidas
    opcionSelec=v.get()
    if opcionSelec not in (1, 2):
        return
    if opcionSelec==1:
        print("Selecciono Color")
        colores=["rojo", "azul", "amarillo", "verde", "negro", "blanco", "naranja", "rosa", "gris", "violeta"]
        palabraJugar=choice(colores) 
    elif opcionSelec==2:
        print("Selecciono Animal")
        animales=["perro", "pato", "león", "tigre", "elefante", "jirafa", "mono", "oso", "caballo", "conejo"]
        palabraJugar=choice(animales) 
    if botonR1 or botonR2:
        botonR1.place_forget()
        botonR2.place_forget()
        C.delete(letreroOp)
    vidas=3
    palabraGuion=["_"]*len(palabraJugar)
    C.create_text(350,100, text="Adivina la palabra secreta", font=("Helvetica", 16, "bold"), anchor="center")
    entradaLetra()

#Función para entrada de texto
def entradaLetra():
    global inputFrame, e1, letreroVidas, letreroPalabra

    if inputFrame:
        inputFrame.destroy()    
    inputFrame=tk.Frame(C, bg="white")
    tk.Label(inputFrame, text="Agrega una letra", bg="DeepSkyBlue").grid(row=1, column=1, sticky=E, padx=5, pady=2)
    e1=tk.Entry(inputFrame)
    e1.grid(row=2, column=1, sticky=W, padx=0, pady=2)
    #Acción ENTER
    e1.bind('<Return>', procesarLetra)
    C.create_window(330, 200, window=inputFrame, anchor=tk.CENTER)

    letreroPalabra = C.create_text(350,120, text=" ".join(palabraGuion), font=("Helvetica", 16, "bold"), anchor="center")
    letreroVidas = C.create_text(350,150, text=f"Vidas restantes: {vidas}", font=("Helvetica", 12), anchor=tk.CENTER)

#Función de final de juego
def finDeJuego(mensajeFinal, color, palabraCompleta=None):
    global numeroRonda
    e1.config(state=DISABLED) #Desabilita entrada de texto
    C.create_text(350, 250, text=mensajeFinal, font=("Helvetica", 24, "bold"), fill=color)
    if palabraCompleta:
        C.create_text(350, 285, text=f"La palabra era {palabraCompleta}", font=("Helvetica", 18, "bold"), fill=color)
    # Ventana emergente con SI/NO
    respuesta = messagebox.askyesno("Fin de la Ronda", "¿Quieres jugar otra ronda?")
    if respuesta:
        reiniciarJuego()
    else:
        root.destroy()

#Función para reiniciar juego
def reiniciarJuego():
    global numeroRonda
    # Limpia todo el canvas para empezar de nuevo
    for item in C.find_all():
        # Evita borrar el mono, el pasto o los letreros de nombre y ronda al reiniciar el juego
        if item not in (pisoZacate, poste, brazoPoste, basePoste, 
                        cabeza, cuerpo, soga, letreroNombre, 
                        letreroRonda, piernaDer, piernaIzq, manoDer, manoIzq): 
            C.delete(item)
    numeroRonda += 1
    mostrarLetreroRonda()
    configurar_juego() # Vuelve a la selección de tema

#Función para procesar letra
def procesarLetra(event):
    global vidas, palabraJugar, palabraGuion, e1, letreroPalabra, letreroVidas
    #Itera la cantidad de letras en la palabra
    letra=e1.get().lower() #Obtiene letra del espacio de entrada
    e1.delete(0,END) #Limpia el campo para la siguiente letra

    if not letra.isalpha() or len(letra) !=1: #Verifica si no puso una letra o dos letras
        textoInval_1=C.create_text(350, 310, text=f"Entrada inválida", font=("Helvetica", 20, "bold"), fill="red")
        textoInval_2=C.create_text(350, 330, text=f"Por favor, introduce solo una letra.", font=("Helvetica", 16, "bold"), fill="red")
        borrarMensaje(textoInval_1)
        borrarMensaje(textoInval_2)
        return
    
    if letra in palabraJugar:
        for indice in range(len(palabraJugar)):
            if palabraJugar[indice]==letra:
                palabraGuion[indice]=letra
    else:
        vidas-=1
        textInc=C.create_text(350, 280, text="X Letra incorrecta, -1 Vidas", font=("Helvetica", 14, "bold"), fill="red")
        borrarMensaje(textInc)
    C.itemconfig(letreroPalabra, text=" ".join(palabraGuion))
    C.itemconfig(letreroVidas, text=f"Vidas restantes: {vidas}")

    #Comprobar palabra completa o juego
    if"_" not in palabraGuion:
        finDeJuego("¡GANASTE!", "blue")
    elif vidas==0:
        finDeJuego("¡PERDISTE!", "red", palabraJugar)

#Función para nombre de jugador
def nombreJugador():
    global letreroNombre, nombreJugadorActual
    nombre = simpledialog.askstring("Nombre del Jugador", "¿Cuál es tu nombre?") # Muestra un cuadro emergente al inicio para pedir el nombre
    if letreroNombre: C.delete(letreroNombre)
    if nombre and nombre.strip(): # Verifica que el nombre no esté vacío
        nombreJugadorActual = nombre # Guarda el nombre en la variable global persistente
        mensaje = f"Jugador: {nombreJugadorActual}"
    else:
        nombreJugadorActual = "Anónimo"
        mensaje = f"Jugador: {nombreJugadorActual}"
    letreroNombre = C.create_text(20, 340, text=mensaje, font=("Helvetica", 10), anchor="sw", fill="white") 

#Zacate
pisoZacate=C.create_rectangle(0, 200, 600, 600, fill="green", outline="black", width=2)
C.tag_lower(pisoZacate)

#Dibujando al mono
poste=C.create_rectangle(100,30,110,340,fill="black")
brazoPoste=C.create_rectangle(80,40,220,50,fill="black")
basePoste=C.create_rectangle(80,340,300,360,fill="black")
cabeza=C.create_oval(170,75,220,125, fill="white", outline="DeepSkyBlue", width=7)
cuerpo=C.create_rectangle(190,130,200,250,fill="DeepSkyBlue", outline="blue")
piernaDer=C.create_polygon(200,250,240,320,240,300,200,230, fill="DeepSkyBlue", outline="blue") #Pierna Derecha
piernaIzq=C.create_polygon(190,250,150,320,150,300,190,230, fill="DeepSkyBlue", outline="Yellow") #Pierna Izquierda
manoDer=C.create_polygon(200,170,240,240,240,220,200,150, fill="DeepSkyBlue", outline="blue") #Mano Derecha
manoIzq=C.create_polygon(190,170,150,240,150,220,190,150, fill="DeepSkyBlue", outline="Yellow") #Mano Izquierda
soga=C.create_rectangle(190,30,200,130,fill="black") #Soga
C.lower(soga)
C.pack() #Enpaquetar el canvas

nombreJugador()
letreroRonda = C.create_text(590, 10, text=f"Ronda: {numeroRonda}", font=("Helvetica", 10), anchor="ne") 
mainloop()