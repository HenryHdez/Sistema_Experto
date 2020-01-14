#!/usr/bin/env python
# -*- coding: utf-8 -*-
"Aplicación del sistema experto"
from tkinter import *
import tkinter.ttk as ttk
from tkinter import font

#Tabla 1
Etiquetas_datos_entrada=["Capacidad Estimada de la hornilla [mp]", "Factor Consumo Bagazo [Fcb]", "Eficiencia Calculada [Eff]", "Bagazillo en Prelimpiador [Bgz]","Cachaza [Chz]", "CSS del Jugo De Caña [Cssi]", "CSS  del Jugo Calrificado [CssCl]", "CSS  del Jugo Posevaporación [CssTE]", "CSS Panela [Bp]", "Tipo de camara", "Humedad del bagazo [Hb]", "Exceso de Aire [λ]", "Extraccion [Extr]", "Porcentaje de Fibra [f]", "Altura del Sitio [h]", "Temperatura Ambiente [Ta]", "Humedad inicial bagazo [Hibv]", "Presion Atmosferica [Pa]","Temperatura Ebullición Agua [Te]"]

Unidades_datos_entrada=["Kg/h","Kg/Kg","%","%","%","°Bx","°Bx","°Bx","°Bx"," ","%"," ","%","%","m","°C","%","mmHG","°C"]

Valores_iniciales_datos_entrada=["102.633","2.111","31.87%","2","4","17.000","22.000","75.000","93.500","ward","15%","1.80","60","14%","1.610.000","25.000","54%","630.732","94.848"]

#Tabla 2
Titulos_Accionamiento=["Producto", "Alimentación de Bagazo", "Alimentación de Caña", "Cosecha", "Transporte"]	
	
Contenido_Accionamiento=["Panela","Manual","Manual","Manual","Manual"]

#Tabla 3
Carac_Molino_1=["Modelo","R 2-S","R 4-A","R 4-S","R-5-S","R 8-A","R 8-AC","R 8-S","R 12-AC","R 14-AL","R 14-S","R15-ACR","R-20-AT"]

Carac_Molino_2=["kg Caña/hora", "500", "900", "900", "1200", "1500", "1500", "1500", "1800", "2000", "2000", "-","3000"]

Carac_Molino_3=["Diesel","10","8","8","8","16","16","16","25","25","25","-","40"]

Carac_Molino_4=["Electrico","5","8","8","10","12","15","15","20","20","20","-","30"]

Carac_Molino_5=["Gasolina","8","-","16","-","-","-","-","-","-","-","-","-"]

Carac_Molino_6=["Relación i","20,5","25,8","11","11,2","33,8","22,75","14,5","51","24,7","28,4","-","27,7"]

Carac_Area=["Area de Caña Sembrada al rededor [Ha]","Area de Caña Sembrada Propia [Ha]","Area de Caña Sembrada Para Calculo [Ha]","Periodo vegetatio [Meses]",	"Caña por Hectarea Esperada [T/Ha]","CSS de la Caña [°Bx]","Jornada de Trabajo [sem]",	"Dias de Trabajo [Dias]", "Horas al Dia [h]"]

Carac_Area_i=["18", "18", "18", "15", "120", "17.000", "2", "6", "12"]

Calculos_Molino_1=["Caña molida al mes [T/mes]", "Area Cosechada al mes [Ha/mes]", "Caña molida a la semana	[T/sem]", "Caña Molida por Hora [T/h]", "Jugo Crudo [T/h]", "Jugo Clarificado [T/h]", "Masa De panela[Kg/h]", "Capacidad del molino"]


Variables_datos_entrada=[]
Variables_Accionamiento=[]
Variables_Molino=[]
Variables_Area=[]
Calculos_Molino_2=[]

root = Tk()

def Mostrar_molino(self):
    p=h1.get()
    for j in range(len(Carac_Molino_1)):
        if(Carac_Molino_1[j]==p):
            print(Carac_Molino_1[j])
            Variables_Molino[0].set(Carac_Molino_1[j])
            Variables_Molino[1].set(Carac_Molino_2[j])
            Variables_Molino[2].set(Carac_Molino_3[j])
            Variables_Molino[3].set(Carac_Molino_4[j])
            Variables_Molino[4].set(Carac_Molino_5[j])
            Variables_Molino[5].set(Carac_Molino_6[j])
            break
    
if __name__== "__main__":
    Helvfont = font.Font(family="Helvetica", size=18, weight="bold")
    Label(root, text="SISTEMA EXPERTO", font=Helvfont).pack()
    Label(root, text=" ").pack()
    Paneles = ttk.Notebook(root)
    Panel_1 = ttk.Frame(Paneles)
    Panel_2 = ttk.Frame(Paneles)
    Panel_3 = ttk.Frame(Paneles)
    Paneles.add(Panel_1, text='Datos de entrada 1')
    Paneles.add(Panel_2, text='Datos de entrada 2')
    Paneles.add(Panel_3, text='Datos de salida 1')
    
    k=0
    #Llenado panel 1 Parte 1
    for i in range(0, len(Carac_Area)):
        Variables_Area.append(StringVar(value=Carac_Area_i[i]))
        Label(Panel_1, text=Carac_Area[i]).grid(pady=5, row=i, column=0)
        Entry(Panel_1, width=20, textvariable=Variables_Area[i]).grid(padx=5, row=i, column=1)    
        k=k+1
    
    #Llenado panel 1 Parte 2
    j=k
    for i in range(k, k+len(Titulos_Accionamiento)):
        Label(Panel_1, text=Titulos_Accionamiento[j-i]).grid(pady=5, row=i, column=0)
        Variables_Accionamiento.append(StringVar(value=Contenido_Accionamiento[j-i]))
        Entry(Panel_1, width=20, textvariable=Variables_Accionamiento[j-i]).grid(padx=5, row=i, column=1)
        k=k+1
        
    #Llenado panel 1 Parte 3
    Variables_Molino.append(StringVar(value=Carac_Molino_1[1]))
    Variables_Molino.append(StringVar(value=Carac_Molino_2[1]))
    Variables_Molino.append(StringVar(value=Carac_Molino_3[1]))
    Variables_Molino.append(StringVar(value=Carac_Molino_4[1]))
    Variables_Molino.append(StringVar(value=Carac_Molino_5[1]))
    Variables_Molino.append(StringVar(value=Carac_Molino_6[1]))
        
    offset_fila_1=k+len(Titulos_Accionamiento)
    h1=StringVar(value="Modelo_Molino")
    b1=ttk.Combobox(Panel_1,width=25,values=Carac_Molino_1[1:], textvariable=h1)
    b1.bind("<<ComboboxSelected>>", Mostrar_molino)
    h1.set("R 2-S")
    b1.grid(pady=5, row=offset_fila_1, column=0)
    
    Label(Panel_1, text=Carac_Molino_1[0]).grid(pady=5, row=offset_fila_1+1, column=0)
    Label(Panel_1, text=Carac_Molino_2[0]).grid(pady=5, row=offset_fila_1+2, column=0)
    Label(Panel_1, text=Carac_Molino_3[0]).grid(pady=5, row=offset_fila_1+3, column=0)
    Label(Panel_1, text=Carac_Molino_4[0]).grid(pady=5, row=offset_fila_1+4, column=0)
    Label(Panel_1, text=Carac_Molino_5[0]).grid(pady=5, row=offset_fila_1+5, column=0)
    Label(Panel_1, text=Carac_Molino_6[0]).grid(pady=5, row=offset_fila_1+6, column=0)    
    
    Entry(Panel_1, width=20, textvariable=Variables_Molino[0]).grid(padx=5, row=offset_fila_1+1, column=1) 
    Entry(Panel_1, width=20, textvariable=Variables_Molino[1]).grid(padx=5, row=offset_fila_1+2, column=1)
    Entry(Panel_1, width=20, textvariable=Variables_Molino[2]).grid(padx=5, row=offset_fila_1+3, column=1)
    Entry(Panel_1, width=20, textvariable=Variables_Molino[3]).grid(padx=5, row=offset_fila_1+4, column=1)
    Entry(Panel_1, width=20, textvariable=Variables_Molino[4]).grid(padx=5, row=offset_fila_1+5, column=1)
    Entry(Panel_1, width=20, textvariable=Variables_Molino[5]).grid(padx=5, row=offset_fila_1+6, column=1)    
       
    #Llenado panel 2
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
    
    
    #Llenado panel 3
            
    #Calculos_Molino_2.append(str())
    for i in range (0, len(Calculos_Molino_1)):
        Calculos_Molino_2.append(StringVar(value=str(i)))
        Label(Panel_3, text=Calculos_Molino_1[i]).grid(pady=5, row=i, column=0)  
        Label(Panel_3, textvariable=Calculos_Molino_2[i]).grid(pady=5, row=i, column=1) 
    #Operaciones matematicas
    Calculos_Molino_2[0].set((int(Variables_Area[2].get())*int(Variables_Area[4].get()))/int(Variables_Area[3].get()))          
    Calculos_Molino_2[1].set(float(Calculos_Molino_2[0].get())/int(Variables_Area[4].get()))
    Calculos_Molino_2[2].set(float(Calculos_Molino_2[0].get())/int(Variables_Area[6].get()))
    Calculos_Molino_2[3].set(float(Calculos_Molino_2[2].get())/(int(Variables_Area[7].get())*int(Variables_Area[8].get()))) 
    Calculos_Molino_2[4].set(float(Calculos_Molino_2[3].get())*(float(Variables_datos_entrada[12].get())/100.0)) 
    
    N12=float(Calculos_Molino_2[4].get())
    G22=float(Variables_datos_entrada[3].get())/100.0
    G23=float(Variables_datos_entrada[4].get())/100.0
    Calculos_Molino_2[5].set(N12-((N12*G22)+((N12-(N12*G22))*G23)))
    
    N13=float(Calculos_Molino_2[5].get())
    G24=float(Variables_datos_entrada[5].get())/100.0
    G27=float(Variables_datos_entrada[8].get())/100.0
    Calculos_Molino_2[6].set(N13*G24/G27*1000)
    
    N11=float(Calculos_Molino_2[3].get())
    Calculos_Molino_2[7].set(N11*1.3*1000)
    #Expansión panel
    Paneles.pack(expand=1, fill='both')
    root.mainloop()