"Aplicación del sistema experto"
from tkinter import *
import tkinter.ttk as ttk
from tkinter import font

Etiquetas_datos_entrada=["Capacidad Estimada de la hornilla [mp]",
                         "Factor Consumo Bagazo [Fcb]",
                         "Eficiencia Calculada [Eff]",
                         "Bagazillo en Prelimpiador [Bgz]",
                         "Cachaza [Chz]",
                         "CSS del Jugo De Caña [Cssi]",
                         "CSS  del Jugo Calrificado [CssCl]",
                         "CSS  del Jugo Posevaporacion [CssTE]",
                         "CSS Panela [Bp]",
                         "Tipo de camara",
                         "Humedad del bagazo [Hb]",
                         "Exceso de Aire [λ]",
                         "Extraccion [Extr]",
                         "Porcentaje de Fibra [f]",
                         "Altura del Sitio [h]",
                         "Temperatura Ambiente [Ta]",
                         "Humedad inicial bagazo [Hibv]",
                         "Presion Atmosferica [Pa]",
                         "Temperatura Ebullición Agua [Te]"]

Unidades_datos_entrada=["Kg/h",
                        "Kg/Kg",
                        "%",
                        "%",
                        "%",
                        "°Bx",
                        "°Bx",
                        "°Bx",
                        "°Bx",
                        " ",
                        "%",
                        " ",
                        "%",
                        "%",
                        "m",
                        "°C",
                        "%",
                        "mmHG",
                        "°C"]

Valores_iniciales_datos_entrada=["102,633",
                                 "2,111",
                                 "31,87%",
                                 "2%",
                                 "4%",
                                 "17,000",
                                 "22,000",
                                 "75,000",
                                 "93,500",
                                 "ward",
                                 "15%",
                                 "1,80",
                                 "60%",
                                 "14%",
                                 "1.610,000",
                                 "25,000",
                                 "54%",
                                 "630,732",
                                 "94,848"]

Titulos=["Producto", "Alimentacion de Bagazo", "Alimentacion de Caña", "Cosecha", "Transporte"]		
Contenido=["Panela","Manual","Manual","Manual","Manual"]

Titulos_Molino=["Modelo","R 2-S","R 4-A","R 4-S","R-5-S","R 8-A","R 8-AC","R 8-S","R 12-AC","R 14-AL","R 14-S","R15-ACR","R-20-AT"]

Titulos_Molino=["kg Caña/hora", "500", "900", "900", "1200", "1500", "1500", "1500", "1800", "2000", "2000", "-","3000"]

Titulos_Molino=["Diesel","10","8","8","8","16","16","16","25","25","25","-","40"]

Titulos_Molino=["Electrico","5","8","8","10","12","15","15","20","20","20","-","30"]

Titulos_Molino=["Gasolina","8","-","16","-","-","-","-","-","-","-","-","-"]

Titulos_Molino=["Relacion i","20,5","25,8","11","11,2","33,8","22,75","14,5","51","24,7","28,4","-","27,7"]

Variables_datos_entrada=[]

root = Tk()



    
if __name__== "__main__":
    Helvfont = font.Font(family="Helvetica", size=18, weight="bold")
    Label(root, text="SISTEMA EXPERTO", font=Helvfont).pack()
    Label(root, text=" ").pack()
    Paneles = ttk.Notebook(root)
    Panel_1 = ttk.Frame(Paneles)
    Panel_2 = ttk.Frame(Paneles)
    Paneles.add(Panel_1, text='Datos de entrada 1')
    Paneles.add(Panel_2, text='Datos de entrada 2')
    for i in range(0, len(Etiquetas_datos_entrada)):
        Label(Panel_2, text=Etiquetas_datos_entrada[i]).grid(pady=5, row=i, column=0)
        if (i!=9):
            Variables_datos_entrada.append(StringVar(value=Valores_iniciales_datos_entrada[i]))
            Entry(Panel_2, width=20, textvariable=Variables_datos_entrada[i]).grid(padx=5, row=i, column=1)  
            Label(Panel_2, text=Unidades_datos_entrada[i]).grid(pady=5, row=i, column=2)
        else:
            Variables_datos_entrada.append(StringVar(value="Camara"))
            ttk.Combobox(Panel_2,width=17,values=["Tpcam", "Ward", "Ad"], textvariable=Variables_datos_entrada[i]).grid(pady=5, row=i, column=1)
            Variables_datos_entrada[i].set("Tpcam")
    Paneles.pack(expand=1, fill='both')
    root.mainloop()