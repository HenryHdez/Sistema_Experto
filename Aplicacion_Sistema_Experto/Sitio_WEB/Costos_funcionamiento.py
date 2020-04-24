# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 10:08:42 2020

@author: hahernandez
"""

import xlrd
import math
import random
import pandas as pd
import numpy as np
import numpy_financial as npf
import matplotlib.pyplot as plt
import time
global Capacidad_hornilla
global Molino_seleccionado
global Horas_trabajo_al_dia

###Rutinas para generar el pdf del costo
#Layout del informe
def Fondo(canvas, Hoja):
    #Dibujar logo y membrete de AGROSAVIA
    canvas.drawImage('static/Iconos/Agrosavia.jpg', 240, 720, width=150, height=40)
    canvas.drawImage('static/Iconos/Membrete.png' , 0, 0, width=650, height=15)
    canvas.drawImage('static/Iconos/Membrete2.png', 0, 650, width=150, height=150)   
    canvas.setLineWidth(.3)
    canvas.setFont('Helvetica-Bold', 20)
#    if(Hoja=="--"):
#        canvas.drawString(275,700,"INFORME:")
#        canvas.drawString(125,678,"DISEÑO PRELIMINAR DE UNA HORNILLA")
#        canvas.line(0,670,680,670)
#        canvas.line(0,665,680,665)
    tiempo = time.asctime(time.localtime(time.time()))
    canvas.setFont('Helvetica-Bold', 7)
    canvas.drawString(520,5,str(tiempo))
    canvas.drawString(10,5,"Hoja: "+str(Hoja))
    return canvas

#Función para generar la parte escrita del informe
def Generar_reporte(D1, D2, D3, D4, D5, D6):
    #Genera la vista previa
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    canvas = canvas.Canvas("static/pdf/A5_informe.pdf", pagesize=letter)
    #Hoja=1
    for k in range(3):
        canvas=Fondo(canvas,"--")
        canvas.setFont('Helvetica-Bold', 12)
        """----------->>>>>>> Publicar Calculos por etapa<<<<<<<<<<<------------"""
        #Publicar calculos de la hornilla
        if(k==0):
            Diccionario=D1
            puntero_v=640
            puntero_h=50
        elif(k==1):
            Diccionario=D2
            puntero_v=640
            puntero_h=50
        elif(k==2):
            Diccionario=D3
        Etiquetas=list(dict.keys(Diccionario))
        for i in Etiquetas:
            canvas.setFont('Helvetica-Bold', 11)
            canvas.drawString(puntero_h, puntero_v, i)
            #Función para dibujar los valores de la Tabla    
            Valores=Diccionario[i]
            puntero_h=puntero_h+300
            for j, vector in enumerate(Valores):
                Texto=str(vector)
                if(i=='Nombre'):
                    canvas.setFont('Helvetica-Bold', 11)
                elif((i=='Valor total de la hornilla') 
                        or (i=='Valor total del recuperador de calor') 
                        or (i=='Total de gastos operativos')):
                    canvas.setFillColorRGB(1,0,0)
                    canvas.setFont('Helvetica-Bold', 11)
                    if(j>1):
                        Texto="$"+Texto
                else:
                    canvas.setFont('Helvetica', 11)
                    if(j>0):
                        Texto="$"+Texto
                canvas.drawString(puntero_h, puntero_v, Texto) 
                puntero_h=puntero_h+80
            puntero_v=puntero_v-15
            puntero_h=50
            if(puntero_v<=30):
                canvas.showPage()
                Fondo(canvas,"--")
                puntero_v=640
        if(k==0):
            canvas.setFillColorRGB(0,0,0)
            canvas.setFont('Helvetica-Bold', 14)
            canvas.drawString(190,680,'--->>>COSTO DE LA HORNILLA<<<---')
            canvas.setFont('Helvetica-Oblique', 10)
            canvas.drawString(puntero_h, puntero_v-10, "Nota: El acero usado en la construcción de la hornilla es inoxidable.") 
            canvas.showPage()
            Fondo(canvas,"--") 
            canvas.setFont('Helvetica-Bold', 14)
            canvas.drawString(140,680,'--->>>COSTO DEL RECUPERADOR DE CALOR<<<---')
            puntero_v=640
        elif(k==1):
            canvas.setFillColorRGB(0,0,0)
            canvas.setFont('Helvetica-Oblique', 10)
            puntero_v=puntero_v-10
            canvas.drawString(puntero_h, puntero_v, "Nota: El acero usado en la construcción del recuperador de calor es inoxidable.")
            canvas.setFont('Helvetica-Bold', 14)
            puntero_v=puntero_v-40
            canvas.drawString(215, puntero_v,'--->>>GASTOS OPERATIVOS<<<---')  
            puntero_v=puntero_v-40
    
    canvas.setFillColorRGB(0,0,0)       
    canvas.setFont('Helvetica-Bold', 14)
    puntero_v=puntero_v-40
    canvas.drawString(215, puntero_v,'--->>>CONSOLIDADO PARCIAL<<<---')  
    puntero_v=puntero_v-40
    Diccionario=D4
    Etiquetas=list(dict.keys(Diccionario))
    for i in Etiquetas:
        canvas.setFont('Helvetica-Bold', 11)
        canvas.drawString(puntero_h, puntero_v, i)
        #Función para dibujar los valores de la Tabla    
        Valores=Diccionario[i]
        puntero_h=puntero_h+450
        Texto=str(Valores)
        if(i=='Descripción'):
            canvas.setFont('Helvetica-Bold', 11)
        elif((i=='Valor total de la construcción con recuperador de calor') 
                or (i=='Valor total de la construcción sin recuperador de calor')):
            canvas.setFillColorRGB(1,0,0)
            canvas.setFont('Helvetica-Bold', 11)
            Texto="$"+Texto
        else:
            canvas.setFont('Helvetica', 11)
            Texto="$"+Texto
        canvas.drawString(puntero_h, puntero_v, Texto) 
        canvas.setFillColorRGB(0,0,0)
        puntero_v=puntero_v-15
        puntero_h=50
        if(puntero_v<=30):
            canvas.showPage()
            Fondo(canvas,"--")
            puntero_v=640
            
    canvas.showPage()
    canvas=Fondo(canvas,"--")
    canvas.setFillColorRGB(0,0,0)       
    canvas.setFont('Helvetica-Bold', 14)
    puntero_v=680
    canvas.drawString(90, puntero_v,'--->>>COSTO DE FUNCIONAMIENTO DE LA HORNILLA POR KG<<<---')  
    puntero_v=640
    Diccionario=D5
    Etiquetas=list(dict.keys(Diccionario))
    for i in Etiquetas:
        canvas.setFont('Helvetica-Bold', 11)
        canvas.drawString(puntero_h, puntero_v, i)
        #Función para dibujar los valores de la Tabla    
        Valores=Diccionario[i]
        puntero_h=puntero_h+400
        for j, vector in enumerate(Valores):
            Texto=str(vector)
            if((i=='El diseño incorpora recuperador de calor') or (i=='Capacidad de la hornilla')):
                canvas.setFont('Helvetica-Bold', 11)
            elif(i=='Valor total del kg de caña'):
                canvas.setFillColorRGB(1,0,0)
                canvas.setFont('Helvetica-Bold', 11)
                Texto="$"+Texto
            else:
                canvas.setFont('Helvetica', 11)
                Texto="$"+Texto
            canvas.drawString(puntero_h, puntero_v, Texto) 
            puntero_h=puntero_h+80
        puntero_v=puntero_v-15
        puntero_h=50
        if(puntero_v<=30):
            canvas.showPage()
            Fondo(canvas,"--")
            puntero_v=640
    canvas.setFillColorRGB(0,0,0)
    canvas.setFont('Helvetica-Oblique', 10)
    puntero_v=puntero_v-10
    canvas.drawString(puntero_h, puntero_v, "Nota: Si el molino implementa un motor eléctrico ignore el costo del motor Diesel o viceversa.")
    canvas.setFont('Helvetica-Bold', 14)
    puntero_v=puntero_v-40
    canvas.drawString(180, puntero_v,'--->>>GASTOS DE FINANCIACIÓN<<<---')  
    puntero_v=puntero_v-40 

    Diccionario=D6
    Etiquetas=list(dict.keys(Diccionario))
    for i in Etiquetas:
        canvas.setFont('Helvetica-Bold', 11)
        canvas.drawString(puntero_h, puntero_v, i)
        #Función para dibujar los valores de la Tabla    
        Valores=Diccionario[i]
        puntero_h=puntero_h+350
        for j, vector in enumerate(Valores):
            Texto=str(vector)
            if(i=='El diseño incorpora recuperador de calor'):
                canvas.setFont('Helvetica-Bold', 11)
            elif(i=='Ingresos anuales aproximados ($)'):
                canvas.setFillColorRGB(1,0,0)
                canvas.setFont('Helvetica-Bold', 11)          
            else:
                canvas.setFont('Helvetica', 11)
            canvas.drawString(puntero_h, puntero_v, Texto) 
            puntero_h=puntero_h+80
        puntero_v=puntero_v-15
        puntero_h=50
        if(puntero_v<=30):
            canvas.showPage()
            Fondo(canvas,"--")
            puntero_v=640
            
    canvas.showPage()
    canvas=Fondo(canvas,"--")
    canvas.drawImage('static/Graficas/Depreciacion.jpg', 175, 490, width=330, height=230)
    canvas.drawImage('static/Graficas/Flujo_Caja_1.jpg', 175, 260, width=330, height=230)
    canvas.drawImage('static/Graficas/Flujo_Caja_2.jpg', 175, 20, width=330, height=230)
    canvas.showPage()
    canvas=Fondo(canvas,"--")
    canvas.drawImage('static/Graficas/RI_Meses.jpg', 175, 490, width=330, height=230)
    canvas.drawImage('static/Graficas/RI_Anos.jpg', 175, 260, width=330, height=230)                         
    canvas.save()
    
def Variables(Capacidad, Horas, semana, moliendas, Cana_estimada):
    global Capacidad_hornilla
    global Horas_trabajo_al_dia
    global Dias_trabajo_semana
    global Toneladas_cana_a_moler
    global numero_moliendas
    Capacidad_hornilla=Capacidad
    Horas_trabajo_al_dia=Horas
    Dias_trabajo_semana=semana
    Toneladas_cana_a_moler=Cana_estimada
    numero_moliendas=moliendas
    
def estimar_total(vector):
    acumulado=[]
    for i in vector:
        acumulado.append(i[2])
    return sum(acumulado)
   
def costos():
    plt.ion()
    global Capacidad_hornilla
    global Horas_trabajo_al_dia
    global Dias_trabajo_semana
    global Toneladas_cana_a_moler
    global numero_moliendas
    Archivo_Temporal=xlrd.open_workbook('static/Temp/Temp2.xlsx')
    libro = Archivo_Temporal.sheet_by_index(0)
    Tipo_de_Pailas=[]
    Cantidad_pailas=[]
    for i in range(len(libro.row(1))):
        Tipo_de_Pailas.append(libro.row(1)[i].value)
        Cantidad_pailas.append(libro.row(2)[i].value)
    Tipo_de_Pailas=Tipo_de_Pailas[1:]
    Cantidad_pailas=Cantidad_pailas[1:]
    """>>>>>>>>>>>>-----------IMPORTAR MOLINOS-------------<<<<<<<<<<<<<<<"""
    Molino=pd.read_excel('static/Temp/Temp.xlsx',skipcolumn = 0,)
    Marca=Molino['Marca'].values
    Modelo=Molino['Modelo'].values
    Kilos=Molino['kg/hora'].values
    Diesel=Molino['Diesel'].values
    Electrico=Molino['Electrico'].values
    Gas=Molino['Gasolina'].values
    Relacion=Molino['Relación i'].values
    Valor_M=Molino['Precio'].values      
    """>>>>>>>>>>>>-----------COSTOS DEL PROYECTO-------------<<<<<<<<<<<<"""
    """>>>>>>>>>>>>----------Costos de la hornilla-------------<<<<<<<<<<<<"""
    Valor_Hornilla=[]
    Total_pailas=sum(Cantidad_pailas)
    Hornilla=pd.read_excel('static/Costos/Hornilla.xlsx')   
    #>>>>>>>>>Pailas<<<<<<<<<#
    a=float(Hornilla['plana'].values)
    Valor_Hornilla.append([Cantidad_pailas[0], a, a*Cantidad_pailas[0]])
    a=float(Hornilla['plana SA'].values)
    Valor_Hornilla.append([Cantidad_pailas[1], a, a*Cantidad_pailas[1]])
    a=float(Hornilla['pirotubular circular'].values)
    Valor_Hornilla.append([Cantidad_pailas[2], a, a*Cantidad_pailas[2]])
    a=float(Hornilla['pirotubular circular SA'].values)
    Valor_Hornilla.append([Cantidad_pailas[3], a, a*Cantidad_pailas[3]])
    a=float(Hornilla['semiesférica'].values)
    Valor_Hornilla.append([Cantidad_pailas[4], a, a*Cantidad_pailas[4]])
    a=float(Hornilla['semicilindrica'].values)
    Valor_Hornilla.append([Cantidad_pailas[5], a, a*Cantidad_pailas[5]])
    a=float(Hornilla['semicilindrica SA'].values)
    Valor_Hornilla.append([Cantidad_pailas[6], a, a*Cantidad_pailas[6]])
    a=float(Hornilla['cuadrada'].values)
    Valor_Hornilla.append([Cantidad_pailas[7], a, a*Cantidad_pailas[7]])
    a=float(Hornilla['cuadrada SA'].values)
    Valor_Hornilla.append([Cantidad_pailas[8], a, a*Cantidad_pailas[8]])
    a=float(Hornilla['acanalada'].values)
    Valor_Hornilla.append([Cantidad_pailas[9], a, a*Cantidad_pailas[9]])
    a=float(Hornilla['acanalada SA'].values)
    Valor_Hornilla.append([Cantidad_pailas[10], a, a*Cantidad_pailas[10]])
    #>>>>>>>>>>Otros accesorios de la hornilla<<<<<<<<<<<<<#
    a=float(Hornilla['Prelimpiador'].values)
    Cantidad=math.ceil(Total_pailas/20)
    Valor_Hornilla.append([Cantidad, a, a*Cantidad])
    a=float(Hornilla['tanque recibidor'].values)
    Cantidad=math.ceil(Total_pailas/20)
    Valor_Hornilla.append([Cantidad, a, a*Cantidad])
    a=float(Hornilla['Ladrillos refractarios'].values)
    Cantidad=1200*Total_pailas
    Valor_Hornilla.append([Cantidad, a, a*Cantidad])
    a=float(Hornilla['Pegante'].values)
    Cantidad=6*Total_pailas
    Valor_Hornilla.append([Cantidad, a, a*Cantidad])
    a=float(Hornilla['Tubo sanitario'].values)
    Cantidad=math.ceil(0.6*Total_pailas)
    Valor_Hornilla.append([Cantidad, a, a*Cantidad])
    a=float(Hornilla['Codos sanitarios'].values)
    Cantidad=math.ceil(1.2*Total_pailas)
    Valor_Hornilla.append([Cantidad, a, a*Cantidad])
    a=float(Hornilla['Válvula de bola'].values)
    Cantidad=math.ceil(0.45*Total_pailas)
    Valor_Hornilla.append([Cantidad, a, a*Cantidad])
    a=float(Hornilla['férula sanitaria'].values)
    Cantidad=math.ceil(0.9*Total_pailas)
    Valor_Hornilla.append([Cantidad, a, a*Cantidad])
    a=float(Hornilla['Abrazadera sanitaria'].values)
    Cantidad=math.ceil(0.9*Total_pailas)
    Valor_Hornilla.append([Cantidad, a, a*Cantidad])
    a=float(Hornilla['Empaque de silicona'].values)
    Cantidad=math.ceil(0.9*Total_pailas)
    Valor_Hornilla.append([Cantidad, a, a*Cantidad])
    a=float(Hornilla['Sección de parrilla'].values)	
    Cantidad=math.ceil(0.45*Total_pailas)
    Valor_Hornilla.append([Cantidad, a, a*Cantidad])
    a=float(Hornilla['Entrada de la hornilla'].values)	
    Cantidad=math.ceil(Total_pailas/20)
    Valor_Hornilla.append([Cantidad, a, a*Cantidad])
    a=float(Hornilla['Descachazado'].values)	
    Cantidad=math.ceil(Total_pailas/20)
    Valor_Hornilla.append([Cantidad, a, a*Cantidad])
    Valor_molino=math.ceil(sum(Valor_M)/len(Valor_M))
    Valor_Hornilla.append([1,Valor_molino,1*Valor_molino])
    #>>>>>>>>>>>>>>>>>>>>>>>>>total gastos de la hornilla
    total_hornilla=math.ceil(estimar_total(Valor_Hornilla))
    Valor_Hornilla.append([' ',' ',total_hornilla])
    Valor_Hornilla.insert(0,['Cantidad', 'Valor unitario', 'Valor Total'])
    """>>>>>>>>>>>>>>>>>>>>>Codificar rotulo del informe<<<<<<<<<<<<<<<<"""
    Etiquetas_Hornilla=['Nombre',
                        'Paila plana', 'Paila plana sin aletas', 'Paila pirotubular circular', 'Paila pirotubular sin aletas',
                        'Paila semiesférica', 'Paila semicilindrica', 'Paila semicilindrica sin aletas', 'Paila cuadrada',
                        'Paila cuadrada sin aletas', 'Paila acanalada con canales cuadrados','Paila acanalada con canales cuadrados y sin aletas',
                        'Prelimpiador', 'Tanque recibidor', 'Ladrillos refractarios', 'Pegante', 'Tubo sanitario de 3 pulgadas',
                        'Codos sanitarios de 3 pulgadas','Valvula de bola de 2 y 1/2 pulgadas', 'Ferula sanitaria de 3 pulgadas',
                        'Abrazadera sanitaria de 3 pulgadas', 'Empaque de silicona de 3 pulgadas (alta temperatura)',
                        'Sección de parrilla', 'Entrada hornilla', 'Descachazado', 'Valor aproximado del molino',
                        'Valor total de la hornilla']
    D_Hornilla=dict(zip(Etiquetas_Hornilla,Valor_Hornilla))  

    """>>>>>>>>>>>>----------Costos recuperador------------<<<<<<<<<<<<"""
    Recuperador=pd.read_excel('static/Costos/Recuperador.xlsx')
    Valor_Recuperador=[]
    b=float(Recuperador['Recuperador Exterior'].values)
    Cantidad=math.ceil(Total_pailas/30)
    Valor_Recuperador.append([Cantidad, b, b*Cantidad])
    b=float(Recuperador['Recuperador Interior'].values)	
    Cantidad=math.ceil(Total_pailas/30)
    Valor_Recuperador.append([Cantidad, b, b*Cantidad])
    b=float(Recuperador['Serpentín Semicilíndrico'].values)	
    Cantidad=Cantidad*2
    Valor_Recuperador.append([Cantidad, b, b*Cantidad])
    b=float(Recuperador['Serpentín Plano'].values)
    Cantidad=math.ceil(Total_pailas/30)
    Valor_Recuperador.append([Cantidad, b, b*Cantidad])
    b=float(Recuperador['Tubería y Accesorios'].values)	
    Cantidad=math.ceil(Total_pailas/30)
    Valor_Recuperador.append([Cantidad, b, b*Cantidad])
    b=float(Recuperador['Ladrillo Chimeneas'].values)	
    Cantidad=math.ceil(Total_pailas/30)*1000
    Valor_Recuperador.append([Cantidad, b, b*Cantidad])
    b=float(Recuperador['Pegante'].values)	
    Cantidad=math.ceil(Total_pailas/30)*8
    Valor_Recuperador.append([Cantidad, b, b*Cantidad])
    b=float(Recuperador['Sección Metálica Chimeneas'].values)
    Cantidad=math.ceil(Total_pailas/30)*4
    Valor_Recuperador.append([Cantidad, b, b*Cantidad])
    b=float(Recuperador['Bomba'].values)
    Valor_Recuperador.append([1, b, b*1])    
    b=float(Recuperador['Instrumentacion y control'].values)
    Valor_Recuperador.append([1, b, b*1])   
    #>>>>>>>>>>>>>>>>>>>>>>>>total gastos de recuperador
    total_recuperador=estimar_total(Valor_Recuperador) 
    """>>>>>>>>>>>>>>>>>>>>>Codificar rotulo del informe<<<<<<<<<<<<<<<<"""
    Valor_Recuperador.append([' ',' ',total_recuperador])
    Valor_Recuperador.insert(0,['Cantidad', 'Valor unitario', 'Valor Total'])    
    Etiquetas_Recuperador=['Nombre',
                        'Recuperador exterior', 'Recuperador interior', 'Serpentín semicilíndrico', 'Serpentín plano',
                        'Tubería y accesorios', 'Ladrillo para la chimenea', 'Pegante','Sección metálica para la chimenea',
                        'Bomba','Instrumentación y control', 'Valor total del recuperador de calor']
    D_Recuperador=dict(zip(Etiquetas_Recuperador,Valor_Recuperador))    
    """>>>>>>>>>>>>----------Costos operativos-------------<<<<<<<<<<<<"""
    #Construcción
    Operativos=pd.read_excel('static/Costos/Operativos.xlsx')
    Valor_Operativo=[]
    c=float(Operativos['Ingeniero'].values)
    Valor_Operativo.append([2, c, c*2])
    c=float(Operativos['Maestro de obra'].values)
    Valor_Operativo.append([2, c, c*2])
    c=float(Operativos['Obrero'].values)	
    Cantidad=math.ceil(Total_pailas/4)
    Valor_Operativo.append([Cantidad, c, Cantidad*c])
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>Total gastos operativos
    total_operativos=estimar_total(Valor_Operativo)
    """>>>>>>>>>>>>>>>>>>>>>Codificar rotulo del informe<<<<<<<<<<<<<<<<"""
    Valor_Operativo.append([' ',' ',total_operativos])
    Valor_Operativo.insert(0,['Cantidad', 'Valor unitario', 'Valor Total'])    
    Etiquetas_Operativos=['Nombre',
                          'Profesional titulado', 'Maestro de obra', 'Obrero', 
                          'Total de gastos operativos']
    D_Operativo=dict(zip(Etiquetas_Operativos,Valor_Operativo))  
    
    """>>>>>>>>>>>>>>-------------TOTALES PROYECTO--------------<<<<<<<<<<<<<<<"""
    Costo_imprevistos=math.ceil(0.02*total_hornilla)
    Consolidado_totales_1=[total_hornilla, total_recuperador, total_operativos, Costo_imprevistos, float(Operativos['Movilidad'])]
    Total_proyecto=sum(Consolidado_totales_1)
    """>>>>>>>>>>>>>>>>>>>>>Codificar rotulo del informe<<<<<<<<<<<<<<<<"""
    Consolidado_totales_1.append(Total_proyecto)
    Consolidado_totales_1.append(Total_proyecto-total_recuperador)
    Consolidado_totales_1.insert(0,'Valor aproximado')    
    Etiquetas_Totales=['Descripción',
                          'Valor total de la construcción de la hornilla',
                          'Valor total de la construcción del recuperador de calor', 
                          'Valor total del gasto operativo durante la construcción', 
                          'Seguro contra gastos imprevistos (2% del total de la construcción de la hornilla)',
                          'Movilidad',
                          'Valor total de la construcción con recuperador de calor',
                          'Valor total de la construcción sin recuperador de calor',
                          ]
    D_Consolidado=dict(zip(Etiquetas_Totales,Consolidado_totales_1))   
    
    mem_capacidad=Capacidad_hornilla
    lista_produccion_1=[]
    lista_produccion_2=[]
    for k in range(2):    
        """>>>>-----------------COSTOS DE LA PRODUCCIÓN-------------------------<<<"""
        if(k==0):
            Capacidad_hornilla=mem_capacidad*0.6
        elif (k==1):
            Capacidad_hornilla=mem_capacidad
        #Variables
        Valor_Cana=float(Operativos['Tonelada de Caña'].values)	
        Galon_diesel=float(Operativos['Galon diesel'].values)		
        P_KWh=float(Operativos['Precio kWh'].values)	
        Mtto=float(Operativos['Mantenimiento'].values)
        Valor_operario=float(Operativos['Operarios'].values)
        Precio_otros_dia=float(Operativos['Valor otros'].values)
        Produ_diaria=Horas_trabajo_al_dia*Capacidad_hornilla
        #>>>>>>>>>>>>>>>>>>>>>Calculos de los Molinos<<<<<<<<<<<<<<<<<<
        #Calculos del molino con motores eléctricos     
        Potencia_e=sum(Electrico)/len(Electrico)
        Eficiencia=0.875		
        PA=((Potencia_e*0.75)/Eficiencia)
        Consumo=PA*Horas_trabajo_al_dia
        Precio_KWh=P_KWh
        Consumo_Motor=Precio_KWh*Consumo
        Costo_kg_Motor=math.ceil(Consumo_Motor/Produ_diaria)
        #Calculos del molino con motores eléctricos de combustion Diesel		
        Potencia_d=sum(Diesel)/len(Diesel)
        Eficiencia=30	
        Consumo=((Potencia_d)/Eficiencia)*Horas_trabajo_al_dia
        Precio_Galon_Diesel=Galon_diesel
        Consumo_Diesel =	Precio_Galon_Diesel*Consumo 
        Costo_kg_Diesel=math.ceil(Consumo_Diesel/Produ_diaria)
        #Potencia disipada por el controlador y la bomba del evaporador   
        Activaciones=Horas_trabajo_al_dia*0.1
        Watts=3000 #Consumo aproximado de la bomba y el controlador
        Consumo=Watts*Activaciones
        Precio_KWh=P_KWh
        Consumo_Controlador=Precio_KWh*Consumo
        Total_Control=math.ceil(Consumo_Controlador/Produ_diaria)
        if(k==0):
            Costo_kg_control=0
        elif(k==1):
            Costo_kg_control=math.ceil(Total_Control/Produ_diaria)
        # >>>>>>>>>> Materia Prima	
        #Multiplico por 1000 para pasar de KG/h a litros
        Relacion=	Toneladas_cana_a_moler/(Capacidad_hornilla*1000)
    
        Costo_kg_cana=math.ceil(Valor_Cana*Relacion)
        #Otros insumos Cera, Empaques, Clarificante			
        Costo_kg_otros=math.ceil(Precio_otros_dia/Produ_diaria)
        #Costo personal			
        Numero_Operarios=Total_pailas-2
        Valor_Contrato=Valor_operario*Numero_Operarios
        Costo_kg_Contrato=math.ceil(Valor_Contrato/Produ_diaria)			
        #Costo Mantenimiento			
        
        Costo_kg_Mtto=math.ceil(Mtto/(Produ_diaria*Dias_trabajo_semana*4*12))
        """>>>>>>>>>>>>>>-------------TOTALES PRODUCCION--------------<<<<<<<<<<<<<<<"""
        Consolidado_totales_2=[Costo_kg_Motor, Costo_kg_Diesel, Costo_kg_control, Costo_kg_cana, Costo_kg_otros, Costo_kg_Mtto, Costo_kg_Contrato]
        Costo_total_kg=sum(Consolidado_totales_2)
        if(k==0):
            lista_produccion_1=Consolidado_totales_2
            lista_produccion_1.append(Costo_total_kg)
            lista_produccion_1.insert(0,Capacidad_hornilla)
            lista_produccion_1.insert(0,'NO')
        elif (k==1):
            lista_produccion_2=Consolidado_totales_2
            lista_produccion_2.append(Costo_total_kg)
            lista_produccion_2.insert(0,Capacidad_hornilla)
            lista_produccion_2.insert(0,'SI')

    """>>>>>>>>>>>>>>>>>>>>>Codificar rotulo del informe<<<<<<<<<<<<<<<<"""  
    Etiquetas_produccion=['El diseño incorpora recuperador de calor',
                          'Capacidad de la hornilla',
                          'Costo de funcionamiento del molino por kg (Motor eléctrico)', 
                          'Costo de funcionamiento del molino por kg (Motor Diesel)', 
                          'Costo de funcionamiento del controlador por kg',
                          'Costo del kg de caña',
                          'Costo de los insumos para la producción (Cera, Empaques, Clarificante)',
                          'Costo del Mantenimiento de la hornilla por kg',
                          'Costo de los operarios kg',
                          'Valor total del kg de caña'
                          ]
    lista1=[]
    for i in range(len(lista_produccion_1)):
        lista1.append([lista_produccion_1[i], lista_produccion_2[i]])
    D_Produccion=dict(zip(Etiquetas_produccion,lista1))    
    
    """>>>>>>>>>>>>>>>>>>>>----------------COSTO FINANCIERO---------------------<<<<<<<<<"""
    mem_capacidad=Capacidad_hornilla
    mem_total_proyecto=Total_proyecto
    lista_financiero_1=[]
    lista_financiero_2=[]   
    lista_Depreciacion1=[]
    lista_Depreciacion2=[]      
    for k in range(2):
        if(k==0):
            Total_proyecto=mem_total_proyecto-total_recuperador
            Capacidad_hornilla=mem_capacidad*0.6
        elif (k==1):
            Total_proyecto=mem_total_proyecto
            Capacidad_hornilla=mem_capacidad
            
        Interes=float(Operativos['Tasa interes'].values)
        t_anos=float(Operativos['Anos depreciacion'].values)
        Costo_financiero=(Total_proyecto*(1+Interes)**t_anos)-Total_proyecto
        """>>>>>>>>>>>>-------------GANACIAS DE LA PANELA-----------<<<<<<<<<<<<<<<<<<<<<<<"""
        Valor_panela=float(Operativos['Costo panela'].values)
        Produccion_mensual_kg=Capacidad_hornilla*Horas_trabajo_al_dia*Dias_trabajo_semana*numero_moliendas
        Produccion_anual_kg=Produccion_mensual_kg*12
        Ingreso_anual=Valor_panela*Produccion_anual_kg
        """>>>>>>>>>>>>>>>>>>>>--------------------DEPRECIACION---------------<<<<<<<<<<<<<<<<<"""
        Valor_Inicial=Total_proyecto
        Vida_util_anos_horn=int(Operativos['vida util hornilla'].values)
        Valor_Salvamento=Total_proyecto*0.05
        Depreciacion_anual=math.ceil((Valor_Inicial-Valor_Salvamento)/Vida_util_anos_horn)
        Depreciacion=[]
        Depreciacion.append(round(Valor_Inicial,3))
        for ano in range(1,Vida_util_anos_horn):
            Depreciacion.append(round(Depreciacion[ano-1]-Depreciacion_anual,3))
        if(k==0):
            lista_financiero_1=[Vida_util_anos_horn, 
                                Interes, 
                                t_anos, 
                                Valor_panela, 
                                math.ceil(Costo_financiero), 
                                Depreciacion_anual, 
                                Produccion_mensual_kg, 
                                Produccion_anual_kg, 
                                Valor_Salvamento, 
                                Ingreso_anual]
            lista_Depreciacion1=Depreciacion
            lista_financiero_1.insert(0,'NO')
        elif (k==1):
            lista_financiero_2=[' ', ' ', ' ', ' ', 
                                math.ceil(Costo_financiero), Depreciacion_anual, Produccion_mensual_kg, 
                                Produccion_anual_kg, Valor_Salvamento, Ingreso_anual]
            lista_Depreciacion2=Depreciacion
            lista_financiero_2.insert(0,'SI')
            
    """>>>>>>>>>>>>>>>>>>>>>Codificar rotulo del informe<<<<<<<<<<<<<<<<"""  
    Etiquetas_financiacion=['El diseño incorpora recuperador de calor',
                          'Vida útil estimada de la hornilla (años)',
                          'Tasa de interés de la financiación',
                          'Tiempo mínimo para recuperar la inversión (años)', 
                          'Valor de la panela actualmente ($)', 
                          'Costo financiero ($)',
                          'Depreciación anual ($)',
                          'Producción mensual (kg)',
                          'Producción anual en (kg)',
                          'Valor de salvamento (5% del total del costo de la hornilla) ($)',
                          'Ingresos anuales aproximados ($)'                          
                          ]
    lista1=[]
    for i in range(len(lista_financiero_1)):
        lista1.append([lista_financiero_1[i], lista_financiero_2[i]])
    D_Financiero=dict(zip(Etiquetas_financiacion,lista1)) 
    Generar_reporte(D_Hornilla, D_Recuperador, D_Operativo, D_Consolidado, D_Produccion, D_Financiero)     
    ###########>>>>>>>>>>>>>>>>>>>>>>Graficar Depreciación<<<<<<<<<<<<<<<<<<<<<################
    Fig_1,a = plt.subplots()
    l1,=a.plot(range(len(lista_Depreciacion1)),np.array(lista_Depreciacion1)/1000000)
    l2,=a.plot(range(len(lista_Depreciacion2)),np.array(lista_Depreciacion2)/1000000)
    a.grid(color='k', linestyle='--', linewidth=1)
    a.set_ylabel('Depreciación en pesos (X1000000)')
    a.set_xlabel('Años [Vida útil de la hornilla]')
    a.set_title('Depreciación de la hornilla')
    a.legend([l1, l2],["Con recuperador", "Sin recuperador"])
    Fig_1.savefig("static/Graficas/Depreciacion.jpg")
    ############################################################################################
    
    """>>>>>>>>>>>>>>>>>>>>--------------------FLUJO DE CAJA---------------<<<<<<<<<<<<<<<<<"""
    mem_total_proyecto=Total_proyecto  
    lista_costo_produccion_1=[]  
    lista_costo_produccion_2=[] 
    lista_flujo_1=[]  
    lista_flujo_2=[] 
    for k in range(2):
        if(k==0):
            Total_proyecto=mem_total_proyecto-total_recuperador
            Costo_financiero=lista_financiero_1[5]
            Depreciacion_anual=lista_financiero_1[6]
            Produccion_anual_kg=lista_financiero_1[8]
            Valor_Salvamento=lista_financiero_1[9]
            Ingreso_anual=lista_financiero_1[10]   
            Costo_total_kg=lista_produccion_1[9]
        elif (k==1):
            Total_proyecto=mem_total_proyecto
            Costo_financiero=lista_financiero_2[5]
            Depreciacion_anual=lista_financiero_2[6]
            Produccion_anual_kg=lista_financiero_2[8]
            Valor_Salvamento=lista_financiero_2[9]
            Ingreso_anual=lista_financiero_2[10]   
            Costo_total_kg=lista_produccion_2[9]
        #Depreciación Anual, Mtto, Ingresos, Flujo de caja
        Estado_caja=[0, 0, 0, Valor_Salvamento-(Total_proyecto+Costo_financiero)]
        Lista_caja=[]
        Lista_caja.append(Estado_caja)
        flujo_caja=[]
        flujo_caja.append(Estado_caja[3])
        Costo_produccion=[]
        for ano in range(1,Vida_util_anos_horn):
            Estado_caja=[Depreciacion_anual, 
                         Produccion_anual_kg*Costo_total_kg, 
                         Ingreso_anual, 
                         Ingreso_anual-(Depreciacion_anual+(Produccion_anual_kg*Costo_total_kg))]
            Lista_caja.append(Estado_caja)
            Costo_produccion.append(Estado_caja[1])
            flujo_caja.append(Estado_caja[3])
        if(k==0):
            lista_costo_produccion_1=Costo_produccion   
            lista_flujo_1=flujo_caja 
        elif (k==1):
            lista_costo_produccion_2=Costo_produccion   
            lista_flujo_2=flujo_caja 

    ###########>>>>>>>>>>>>>>>>>>>>>>Graficar flujo de caja<<<<<<<<<<<<<<<<<<<<<################
    #Sin recuperador
    Fig_2,b = plt.subplots()
    b.barh(range(len(lista_flujo_1)),np.array(lista_flujo_1)/1000000)
    b.grid(color='k', linestyle='--', linewidth=1)
    b.set_ylabel('Años [Vida útil de la hornilla]')
    b.set_xlabel('Valor en pesos (X1000000)')
    b.set_title('Flujo de caja aproximado de la hornilla sin recuperador')
    Fig_2.savefig('static/Graficas/Flujo_Caja_1.jpg')
    #Con recuperador
    Fig_2a,c = plt.subplots()
    c.barh(range(len(lista_flujo_2)),np.array(lista_flujo_2)/1000000)
    c.grid(color='k', linestyle='--', linewidth=1)
    c.set_ylabel('Años [Vida útil de la hornilla]')
    c.set_xlabel('Valor en pesos (X1000000)')
    c.set_title('Flujo de caja aproximado de la hornilla con recuperador')
    Fig_2a.savefig('static/Graficas/Flujo_Caja_2.jpg')
    ############################################################################################
#    print(Depreciacion_anual)
#    print(Produccion_anual_kg)
#    print(Costo_total_kg)
#    print(Produccion_anual_kg*Costo_total_kg)
#    print(flujo_caja)
#    #Valor presente neto
#    Tasa_Interes=float(Operativos['Tasa interes'].values)
#    NPV=npf.npv(rate=Tasa_Interes,values=flujo_caja)
#    TIR=round(npf.irr(flujo_caja), 3)
    """>>>>>>------RETORNO A LA INVERSION----<<<<"""
    Retorno_inversion1=[]  
    Retorno_inversion2=[] 
    for k in range(2):
        if(k==0):
            Valor_panela=float(Operativos['Costo panela'].values)
            Costo_produccion=lista_costo_produccion_1
            flujo_caja=lista_flujo_1
            Produccion_anual_kg=lista_financiero_1[8]
        elif (k==1):
            Valor_panela=float(Operativos['Costo panela'].values)
            Costo_produccion=lista_costo_produccion_2
            flujo_caja=lista_flujo_2
            Produccion_anual_kg=lista_financiero_2[8]
            
        Retorno_inversion=[]    
        for i in Costo_produccion:
            Ingreso_esperado=Valor_panela*Produccion_anual_kg
            Ganancia_Acumulada=Ingreso_esperado-i
            Valor_Proyecto=round(flujo_caja[0],3)
            Tiempo_anos=round(-Valor_Proyecto/Ganancia_Acumulada,3)
            Estado_retorno=[Valor_panela, 
                            i, 
                            Ingreso_esperado,
                            Ganancia_Acumulada,  
                            Valor_Proyecto, 
                            Tiempo_anos, 
                            Tiempo_anos*12]
            Valor_panela=Valor_panela+25#+random.uniform(-500, 500)
            Retorno_inversion.append(Estado_retorno)
        if(k==0):
            Retorno_inversion1=Retorno_inversion
        elif (k==1):
            Retorno_inversion2=Retorno_inversion
    MA=np.array(Retorno_inversion1)
    lista_valor_panela1=MA[:,0]
    Anos1=MA[:,5]
    Meses1=MA[:,6]
    
    MB=np.array(Retorno_inversion2)
    lista_valor_panela2=MB[:,0]
    Anos2=MB[:,5]
    Meses2=MB[:,6]
    #print(Anos)
    ###########>>>>>>>>>>>>>>>>>Graficar Retorno a la inversión<<<<<<<<<<<<<<<<<################
    Fig_3,d = plt.subplots()
    l1,=d.plot(lista_valor_panela1,Anos1)
    l2,=d.plot(lista_valor_panela2,Anos2)
    d.grid(color='k', linestyle='--', linewidth=1)
    d.set_ylabel('Años [Funcionamiento de la hornilla]')
    d.set_xlabel('Valor de la panela en pesos')
    d.set_title('Retorno a la inversión de la hornilla')
    d.legend([l1, l2],["Con recuperador", "Sin recuperador"])
    Fig_3.savefig('static/Graficas/RI_Anos.jpg')
    ############################################################################################
    ###########>>>>>>>>>>>>>>>>>Graficar Retorno a la inversión<<<<<<<<<<<<<<<<<################
    Fig_4,e = plt.subplots()
    l1,=e.plot(lista_valor_panela1,Meses1)
    l2,=e.plot(lista_valor_panela2,Meses2)
    e.grid(color='k', linestyle='--', linewidth=1)
    e.set_ylabel('Meses [Funcionamiento de la hornilla]')
    e.set_xlabel('Valor de la panela en pesos')
    e.set_title('Retorno a la inversión de la hornilla')
    e.legend([l1, l2],["Con recuperador", "Sin recuperador"])
    Fig_4.savefig('static/Graficas/RI_Meses.jpg')
    ############################################################################################
#print(Retorno_inversion)
#    Marca=Molino['Marca'].values
#    Modelo=Molino['Modelo'].values
#    Kilos=Molino['kghora'].values
#    Diesel=Molino['Diesel'].values
#    Electrico=Molino['Electrico'].values
#    Gas=Molino['Gasolina'].values
#    Relacion=Molino['Relacion'].values
#    Valor=Molino['Valor'].values
#    Seleccionado=[]
#    