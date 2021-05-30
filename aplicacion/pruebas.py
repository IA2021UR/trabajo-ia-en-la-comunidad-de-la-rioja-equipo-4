from tkinter import *
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import cv2
import numpy as np

from fastai import core

from deoldify.visualize import get_image_colorizer

global numero
def elegir_imagen():
    global path_image
    # Especificar los tipos de archivos, para elegir solo a las imágenes
    path_image = filedialog.askopenfilename(filetypes = [
        ("image", ".jpeg"),
        ("image", ".png"),
        ("image", ".jpg")])

    if len(path_image) > 0:
        global image

        # Leer la imagen de entrada y la redimensionamos
        image = cv2.imread(path_image)
        #image= imutils.resize(image, height=380)
        # Para visualizar la imagen de entrada en la GUI
        #imageToShow= imutils.resize(image, width=180)
        imageToShow = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(imageToShow )
        img = ImageTk.PhotoImage(image=im)
        lblInputImage.configure(image=img)
        lblInputImage.image = img
        # Label IMAGEN DE ENTRADA
        lblInfo1 = Label(root, text="IMAGEN DE ENTRADA:")
        lblInfo1.grid(column=0, row=1, padx=5, pady=5)
        # Al momento que leemos la imagen de entrada, vaciamos
        # la iamgen de salida y se limpia la selección de los
        # radiobutton
        lblOutputImage.image = ""


def colorear_imagen():
    global image

    numero = textbox.get(1.0, END)
    numero = str(numero)
    numero_str = numero.replace("\n", "")
    print(numero_str)
    print("ayuda")

    colorizer = get_image_colorizer(artistic=True)
    render_factor = int(numero)

    image_path = colorizer.plot_transformed_image(path=path_image, render_factor=render_factor, compare=True, watermarked=False)

    im = Image.open(image_path)
    
    # Para visualizar la imagen en lblOutputImage en la GUI
    img = ImageTk.PhotoImage(image=im)
    lblOutputImage.configure(image=img)
    lblOutputImage.image = img
    # Label IMAGEN DE SALIDA
    lblInfo3 = Label(root, text="IMAGEN DE SALIDA:", font="bold")
    lblInfo3.grid(column=1, row=0, padx=5, pady=5)



# Creamos la ventana principal
root = Tk()

# Label donde se presentará la imagen de entrada
lblInputImage = Label(root)
lblInputImage.grid(column=0, row=2)


# Label donde se presentará la imagen de salida
lblOutputImage = Label(root)
lblOutputImage.grid(column=1, row=1, rowspan=6)

# Creamos el botón para elegir la imagen de entrada
btn = Button(root, text="Elegir imagen", width=25, command=elegir_imagen)
btn.grid(column=0, row=0, padx=5, pady=5)

#Label para modificar el renderizado
lblReder = Label(root, text="Elegir un numero entre 10 y 30")
lblReder.grid(column=0, row=3)

#Creamos el texto de entrada para obtener el renderizado
textbox = Text(height=1, width=2);
textbox.grid(column=0, row = 4)

#Creamos el botón para colorear la imagen de entrada
boton = Button(root, text="Colorear imagen", width=25, command=colorear_imagen)
boton.grid(column=0,row=5, padx=5, pady=5)


root.mainloop()

