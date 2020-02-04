#!/usr/bin/env python
# -*- coding: utf-8 -*-
"Aplicación del sistema experto"
"Librerias para crear elementos de la interfaz grafica"
from tkinter import *
import tkinter.ttk as ttk
from tkinter import font
import math

"Variables globales"
"Etiquetas"
#Tabla 1
Etiquetas_datos_entrada=["Capacidad Estimada de la hornilla [mp]", "Factor Consumo Bagazo [Fcb]", "Eficiencia Calculada [Eff]", "Bagazillo en Prelimpiador [Bgz]","Cachaza [Chz]", "CSS del Jugo De Caña [Cssi]", "CSS  del Jugo Clarificado [CssCl]", "CSS  del Jugo Posevaporación [CssTE]", "CSS Panela [Bp]", "Tipo de camara", "Humedad del bagazo [Hb]", "Exceso de Aire [λ]", "Extraccion [Extr]", "Porcentaje de Fibra [f]", "Altura del Sitio [h]", "Temperatura Ambiente [Ta]", "Humedad inicial bagazo [Hibv]", "Presion Atmosferica [Pa]","Temperatura Ebullición Agua [Te]"]

Unidades_datos_entrada=["Kg/h","Kg/Kg","%","%","%","°Bx","°Bx","°Bx","°Bx"," ","%"," ","%","%","m","°C","%","mmHG","°C"]

Valores_iniciales_datos_entrada=["102.633","2.111","31.87","2","4","17.000","18.000","75.000","93.500","ward","15","1.80","60","14","1.610","25","30","630.732","99.019"]

#Tabla 2
Titulos_Accionamiento=["Producto", "Alimentación de Bagazo", "Alimentación de Caña", "Cosecha", "Transporte"]	
	
Contenido_Accionamiento=["Panela","Manual","Manual","Manual","Manual"]

#Tabla 3
Carac_Molino_1=["Modelo","R 2-S","R 4-A","R 4-S","R-5-S","R 8-A","R 8-AC","R 8-S","R 12-AC","R 14-AL","R 14-S","R15-ACR","R-20-AT"]

Carac_Molino_2=["kg Caña/hora", "500", "900", "900", "1200", "1500", "1500", "1500", "1800", "2000", "2000", "-","3000"]

Carac_Molino_3=["Diesel","10","8","8","8","16","16","16","25","25","25","-","40"]

Carac_Molino_4=["Electrico","5","8","8","10","12","15","15","20","20","20","-","30"]

Carac_Molino_5=["Gasolina","8","-","16","-","-","-","-","-","-","-","-","-"]

Carac_Molino_6=["Relación i","20.5","25.8","11","11.2","33.8","22.75","14.5","51","24.7","28.4","-","27.7"]

Carac_Area=["Area de Caña Sembrada al rededor [Ha]","Area de Caña Sembrada Propia [Ha]","Area de Caña Sembrada Para Calculo [Ha]","Periodo vegetatio [Meses]",	"Caña por Hectarea Esperada [T/Ha]","CSS de la Caña [°Bx]","Jornada de Trabajo [sem]",	"Dias de Trabajo [Dias]", "Horas al Dia [h]"]

Carac_Area_i=["18", "18", "18", "15", "120", "17", "2", "6", "12"]

Calculos_Molino_1=["Caña molida al mes [T/mes]", "Area Cosechada al mes [Ha/mes]", "Caña molida a la semana	[T/sem]", "Caña Molida por Hora [T/h]", "Jugo Crudo [T/h]", "Jugo Clarificado [T/h]", "Masa De panela[Kg/h]", "Capacidad del molino"]

Rotulos_Masas=["Caña [Kg/h]", "Jugo [Kg/h]", "Bagazillo [Kg/h]", "Jugo Pre Limp [Kg/h]", "Cachaza [Kg/h]", "Jugo Clarificado [Kg/h]", "Agua a Evaporar [Kg/h]", "A Clarificacion [Kg/h]", "A Evaporacion [Kg/h]", "A Concentracion [Kg/h]", "Bag. Suministrado [Kg/h]", "Bag. humedo [Kg/h]", "Bag. seco [Kg/h]" ]

Rotulos_Propiedades_de_los_jugos=["Inicial P. Clf [Kg/m3]", "Inicial P. Eva 1 [Kg/m3]", "Inicial P. Con [Kg/m3]", "Clarificacón [°C]", "Evaporación [°C]", "Concentración [°C]", "Clarificación [KJ/kg]", "Evaporación [KJ/kg]", "Concentración [KJ/kg]", "Inicial [KJ/Kg °C]", "Clarificado [KJ/Kg °C]", "Eva [KJ/Kg °C]", "Poder Calorifico bagazo [MJ/kg]", "Calor Suministrado [KW]", "Area de Parrilla [m2]"]

"Listas de variables"
Variables_datos_entrada=[]
Variables_propiedades_jugos=[]
Variables_Molino=[]
Variables_Area=[]
Variables_Accionamiento=[]
Variables_Q_Etapa=[]
Calculos_Molino_2=[]
Calculos_Masas=[]
Cantidad_Etapas=" "
"Funciones para realizar los calculos de la geometria de la hornilla"
root = Tk()

#Estimar volumen de las pailas
def Precalentadora_Plana(H_fl,H_fn,Ang,A,L):
    #Parametros fijos para calcular el TCC
    #N_Aletas	
    #h_Aletas	
    Area=(A*L)+(2*A*H_fn)+(2*H_fn*L)	
    Volumen_Fon=(H_fn*A*L)	
    Volumen_total=(A*H_fn*L)+(A+H_fl/math.tan(Ang))*H_fl*L
    return Volumen_Fon
	
def Pirtubular_Circular_Aleteada_Clarificadora(H_fl,H_fn,A,L,dT,nT):
    Ang=68*math.pi/180
    Volumen_Fon=((H_fn*A)-(((math.pi/4)*(dT**2))*nT))*L
    Volumen_total=Volumen_Fon+(L*H_fl*(A+H_fl/math.tan(Ang)))
    return Volumen_total

def Semicilindrica_pequeña(H_fn,A,H_fa):
    R=((A/2)**2+H_fn**2)/(2*H_fn)	
    Ang=68*math.pi/180
    VTJ=(math.pi*H_fn**2*(3*R-H_fn))/3
    A1=math.pi*((A/2)**2)
    x=A+2*(H_fa/math.tan(Ang))
    A2=x**2
    VFA=(H_fa*(A1+A2+math.sqrt(A1*A2)))/3
    VTPA=VFA+VTJ	
    return VTJ

#Crear ventana para mostrar partes de la hornilla
def Mostrar_hornilla():
    raiz = Tk() 
    raiz.title("Hornilla") #Cambiar el nombre de la ventana 
    raiz.geometry("520x480") #Configurar tamaño 
    raiz.config(bg="red") #Cambiar color de fondo
    raiz.mainloop() 
    print(Precalentadora_Plana(0.59,0.1,1.87,0.8,1.2))
    print(Pirtubular_Circular_Aleteada_Clarificadora(0.5,0.3,0.96,0.8,0.17,3))
    print(Semicilindrica_pequeña(0.52,1.1,0.2))
    
def Mostrar_molino(self):
    p=h1.get()
    for j in range(len(Carac_Molino_1)):
        if(Carac_Molino_1[j]==p):
            #print(Carac_Molino_1[j])
            Variables_Molino[0].set(Carac_Molino_1[j])
            Variables_Molino[1].set(Carac_Molino_2[j])
            Variables_Molino[2].set(Carac_Molino_3[j])
            Variables_Molino[3].set(Carac_Molino_4[j])
            Variables_Molino[4].set(Carac_Molino_5[j])
            Variables_Molino[5].set(Carac_Molino_6[j])
            break

def Actualizar_Valores():
 #Mostrar hornilla
    Mostrar_hornilla()
    
    
    #Llenado panel 3
    G19=float(Variables_datos_entrada[0].get())
    G20=float(Variables_datos_entrada[1].get())
    G22=float(Variables_datos_entrada[3].get())/100
    G23=float(Variables_datos_entrada[4].get())/100 
    G24=float(Variables_datos_entrada[5].get())
    G25=float(Variables_datos_entrada[6].get())
    G26=float(Variables_datos_entrada[7].get())
    G27=float(Variables_datos_entrada[8].get())/100.0
    G29=float(Variables_datos_entrada[10].get())/100 
    G34=float(Variables_datos_entrada[15].get())
    G35=float(Variables_datos_entrada[16].get())
    G37=float(Variables_datos_entrada[18].get())
    #G40=float(Variables_datos_entrada[21].get())

            
    #Calculos_Molino_2.append(str())
    for i in range (0, len(Calculos_Molino_1)):
        Calculos_Molino_2.append(StringVar(value=str(i)))
        Label(Panel_3, text=Calculos_Molino_1[i]).grid(pady=5, row=i, column=0)  
        Label(Panel_3, textvariable=Calculos_Molino_2[i]).grid(pady=5, row=i, column=1) 
    
    #Operaciones matematicas Caña molida al mes
    Calculos_Molino_2[0].set((float(Variables_Area[2].get())*float(Variables_Area[4].get()))/float(Variables_Area[3].get()))          
    Calculos_Molino_2[1].set(float(Calculos_Molino_2[0].get())/float(Variables_Area[4].get()))
    Calculos_Molino_2[2].set(float(Calculos_Molino_2[0].get())/float(Variables_Area[6].get()))
    Calculos_Molino_2[3].set(float(Calculos_Molino_2[2].get())/(float(Variables_Area[7].get())*float(Variables_Area[8].get()))) 
    Calculos_Molino_2[4].set(float(Calculos_Molino_2[3].get())*(float(Variables_datos_entrada[12].get())/100.0)) 
    
    N12=float(Calculos_Molino_2[4].get())
    Calculos_Molino_2[5].set(N12-((N12*G22)+((N12-(N12*G22))*G23)))
    
    N13=float(Calculos_Molino_2[5].get())
    Calculos_Molino_2[6].set(N13*G24/G27*1000)
    
    N11=float(Calculos_Molino_2[3].get())
    Calculos_Molino_2[7].set(N11*1.3*1000)
    
    #Operaciones matematicas masas
    k=0
    for i in range (len(Calculos_Molino_1), len(Calculos_Molino_1)+len(Rotulos_Masas)):
        Calculos_Masas.append(StringVar(value=str(i)))
        Label(Panel_3, text=Rotulos_Masas[k]).grid(pady=5, row=i, column=0)  
        Label(Panel_3, textvariable=Calculos_Masas[k]).grid(pady=5, row=i, column=1)  
        k=k+1
           
    Cana=float(Calculos_Molino_2[3].get())*1000
    Jugo=float(Calculos_Molino_2[4].get())*1000
    Bagazillo= Jugo*G22  
    Jugo_Clarificado=float(Calculos_Molino_2[5].get())*1000
    Jugo_Pre_limp=Jugo_Clarificado/(1-G23)
    Cachaza=Jugo_Pre_limp*G23
    Agua_Evaporar=Jugo_Pre_limp-G19
    A_clarificacion=Jugo_Pre_limp
    A_Evaporacion=Jugo_Clarificado
    A_Concentracion=(A_Evaporacion*G25)/G26
    Bag_Suministrado=G19*G20
    Bag_Humedo=Cana-Jugo
    Bag_Seco=Bag_Humedo*((1-G35)/(1-G29))
    
    Calculos_Masas[0].set(Cana)  
    Calculos_Masas[1].set(Jugo)  
    Calculos_Masas[2].set(Bagazillo)  
    Calculos_Masas[3].set(Jugo_Pre_limp)  
    Calculos_Masas[4].set(Cachaza)  
    Calculos_Masas[5].set(Jugo_Clarificado)  
    Calculos_Masas[6].set(Agua_Evaporar)  
    Calculos_Masas[7].set(A_clarificacion)  
    Calculos_Masas[8].set(A_Evaporacion)  
    Calculos_Masas[9].set(A_Concentracion)  
    Calculos_Masas[10].set(Bag_Suministrado)  
    Calculos_Masas[11].set(Bag_Humedo)  
    Calculos_Masas[12].set(Bag_Seco)    
    
    
    #Contenido del panel 4
    Label(Panel_4, text="PROPIEDADES DE LOS JUGOS").grid(row=0, column=0)
    Label(Panel_4, text="Densidad").grid(row=1, column=0)
    f=2
    p=0
    
    for i in range (2, len(Rotulos_Propiedades_de_los_jugos)+6):
        
        if i!=5 and i!=9 and i!=13 and i!=17:
            Variables_propiedades_jugos.append(StringVar(value=str(i)))
            Label(Panel_4, text=Rotulos_Propiedades_de_los_jugos[p]).grid(pady=5, row=f, column=0)  
            Label(Panel_4, textvariable=Variables_propiedades_jugos[p]).grid(pady=5, row=f, column=1)   
            p=p+1
        else:
            if(i==5):
                Label(Panel_4, text="Temperatura de ebullición").grid(row=f, column=0)
                f=f+1
            elif(i==9):
                Label(Panel_4, text="Entalpia de Evaporizacion").grid(row=f, column=0)
                f=f+1
            elif(i==13):
                Label(Panel_4, text="Calor especifico jugo").grid(row=f, column=0)
                f=f+1   
            elif(i==17):
                Label(Panel_4, text=" ").grid(row=f, column=0)
                f=f+1
        f=f+1
    #Operaciones propiedades de los jugos
        
    #T33 viene del catalogo de molinos
    T33=float(Carac_Molino_3[9])
    #______
    #print(G24)
    Inicial_Clf=997.39+(4.46*G24)   
    Inicial_Eva=997.39+(4.46*G25)
    Inicial_Con=997.39+(4.46*G26)
    Ebullicion_Clarificacion=G37+(0.2209*math.exp(0.0557*G25))	
    Ebullicion_Evaporacion=G37+0.2209*math.exp(0.0557*G26)	
    Ebullicion_Concentracion=G37+0.2209*math.exp(0.0557*T33)	
    Entalpia_Clarificacion=2492.9-2.0523*((G37+Ebullicion_Clarificacion)/2)-0.0030752*((G37+Ebullicion_Clarificacion)/2)**2
    Entalpia_Evaporacion=2492.9-2.0523*((Ebullicion_Clarificacion+Ebullicion_Evaporacion)/2)-0.0030752*((Ebullicion_Clarificacion+Ebullicion_Evaporacion)/2)**2
    Entalpia_Concentracion=2492.9-2.0523*((Ebullicion_Evaporacion+Ebullicion_Concentracion)/2)-0.0030752*((Ebullicion_Evaporacion+Ebullicion_Concentracion)/2)**2
    Q_Especifico_Inicial=4.18*(1-0.006*G24)
    Q_Especifico_Clarificado=4.18*(1-0.006*G25)	
    Q_Especifico_Eva=4.18*(1-0.006*G26)	
    Poder_Calorifico_bagazo=17.85-20.35*G29
    Calor_Suministrado=(G20*G19)*Poder_Calorifico_bagazo/3.6	
    Area_de_Parrilla=Calor_Suministrado/1000	

    
    Variables_propiedades_jugos[0].set(Inicial_Clf)
    Variables_propiedades_jugos[1].set(Inicial_Eva)
    Variables_propiedades_jugos[2].set(Inicial_Con)
    Variables_propiedades_jugos[3].set(Ebullicion_Clarificacion)
    Variables_propiedades_jugos[4].set(Ebullicion_Evaporacion)
    Variables_propiedades_jugos[5].set(Ebullicion_Concentracion)
    Variables_propiedades_jugos[6].set(Entalpia_Clarificacion)
    Variables_propiedades_jugos[7].set(Entalpia_Evaporacion)
    Variables_propiedades_jugos[8].set(Entalpia_Concentracion)
    Variables_propiedades_jugos[9].set(Q_Especifico_Inicial)
    Variables_propiedades_jugos[10].set(Q_Especifico_Clarificado)
    Variables_propiedades_jugos[11].set(Q_Especifico_Eva)
    Variables_propiedades_jugos[12].set(Poder_Calorifico_bagazo)
    Variables_propiedades_jugos[13].set(Calor_Suministrado)
    Variables_propiedades_jugos[14].set(Area_de_Parrilla)
    
    #Contenido del panel 5
    for i in range(5):
        Variables_Q_Etapa.append(StringVar(value=str(i)))
        Label(Panel_5, textvariable=Variables_Q_Etapa[i]).grid(row=i+1, column=1)
    Label(Panel_5, text="Calor Requerido por Etapa").grid(row=0, column=0)
    Label(Panel_5, text="Clarificación [KW]").grid(row=1, column=0)
    Label(Panel_5, text="Evaporación [KW]").grid(row=2, column=0)
    Label(Panel_5, text="Concentración [KW]").grid(row=3, column=0)
    Label(Panel_5, text="Total [KW]").grid(row=4, column=0)
    Label(Panel_5, text="Total(F.L.) [KW]").grid(row=5, column=0)
    
    Q_Etapa_Clarificacion=((A_clarificacion*Q_Especifico_Inicial*(Ebullicion_Clarificacion-G34))+((A_clarificacion-A_Evaporacion)*Entalpia_Clarificacion))/3600   
    Q_Etapa_Evaporacion=(A_Evaporacion*Q_Especifico_Clarificado*(Ebullicion_Evaporacion-Ebullicion_Clarificacion)+(A_Evaporacion-A_Concentracion)*Entalpia_Evaporacion)/3600
    Q_Etapa_Concentracion=(A_Concentracion*Q_Especifico_Eva*(Ebullicion_Concentracion-Ebullicion_Evaporacion)+(A_Concentracion-G19)*Entalpia_Concentracion)/3600
    Total_Etapa=Q_Etapa_Clarificacion+Q_Etapa_Evaporacion+Q_Etapa_Concentracion
    Total_Etapa_F_L=(Jugo*(Ebullicion_Concentracion-G34)*Q_Especifico_Inicial+Agua_Evaporar*((Entalpia_Clarificacion+Entalpia_Concentracion)/2))/3600
    
    Variables_Q_Etapa[0].set(Q_Etapa_Clarificacion)
    Variables_Q_Etapa[1].set(Q_Etapa_Evaporacion)
    Variables_Q_Etapa[2].set(Q_Etapa_Concentracion)
    Variables_Q_Etapa[3].set(Total_Etapa)
    Variables_Q_Etapa[4].set(Total_Etapa_F_L)
    
    #Contenido del Panel 6 
    #Calculo de las demas etapas de la hornilla
    # Cantidad_Etapas=StringVar(value="7")
    # Label(Panel_6, text="Cantidad de etapas: ").grid(row=0, column=0)
    # Entry(Panel_6, width=20, textvariable=Cantidad_Etapas).grid(padx=5, row=0, column=1) 
    
    Lista_Contenido=[]
    Lista_columnas=[]
    Etapas=int(Cantidad_Etapas.get())
    if (Etapas>2):
        Factor_Division=Etapas-2
    else:
        Factor_Division=2     
    #Caracteristicas de las celdas de cada columna
    #Fila 0 concentración de solidos inicial
    #Fila 1 Concentración de solidos final
    #Fila 2 Concentración promedio
    #Fila 3 Masa de jugo de entrada
    #Fila 4 Calor Especifico P Cte jugo
    #Fila 5 Densidad del Jugo
    #Fila 6 Volumen de jugo kg
    #Fila 7 Volumen de jugo en L
    #Fila 8 Temperatura de Entrada
    #Fila 9 Temperatura de Salida
    #Fila 10 Entalpia de Vaporización
    #Fila 11 Masa de Agua a Evaporar
    #Fila 12 Calor Nece Calc por Etapa

    for i in range(Etapas):
        for j in range (13):
            Lista_columnas.append(float(i+j))
        Lista_Contenido.append(Lista_columnas)
        Lista_columnas=[]
    #Suposiciones iniciales
    Lista_Contenido[0][0]=G26        #Concentracion_solidos_inicial (CSS02)
    Lista_Contenido[0][1]=G27*100.0  #Concentracion_solidos_final   (CSSF1)
    Lista_Contenido[Etapas-1][0]=G24 #Concentracion_solidos_inicial (CSS01)
    Lista_Contenido[Etapas-1][1]=G25 #Concentracion_solidos_final   (CSSF1)
    ite=0
    for i in range(Etapas-2,0,-1):
        Lista_Contenido[i][0]=Lista_Contenido[i+1][1]
        if(ite==0):
            Lista_Contenido[i][1]=((Lista_Contenido[0][0]-Lista_Contenido[i][0])/Factor_Division)+Lista_Contenido[i][0]
            ite=ite+1
        else:
            Lista_Contenido[i][1]=((Lista_Contenido[0][0]-Lista_Contenido[Etapas-2][0])/Factor_Division)+Lista_Contenido[i][0]
               
    for i in range(Etapas-1,-1,-1):
        #Concentración promedio=(Concentracion_solidos_inicial+Concentracion_solidos_final)/2
        Lista_Contenido[i][2]=(Lista_Contenido[i][0]+Lista_Contenido[i][1])/2
        if(i==Etapas-1):
            #Masa de jugo de entrada
            Lista_Contenido[i][3]=A_clarificacion
        else:
            #Masa de jugo de entrada=(Masa de jugo etapa anterior*CCS inicial etapa anterior)/CCS Final etapa anterior
            Lista_Contenido[i][3]=Lista_Contenido[i+1][3]*Lista_Contenido[i+1][0]/Lista_Contenido[i+1][1]    
        #Calor_Especifico_P_Cte_jugo=4.18*(1-(0.006*Concetracion_promedio))
        Lista_Contenido[i][4]=4.18*(1-(0.006*Lista_Contenido[i][2]))
        #Densidad_del_Jugo=997.39+(4.46*Concetracion_promedio)
        Lista_Contenido[i][5]=997.39+(4.46*Lista_Contenido[i][2])
        #Volumen_jugo=Masa_jugo_de_entrada/Densidad_del_Jugo
        Lista_Contenido[i][6]=Lista_Contenido[i][3]/Lista_Contenido[i][5]
        #Volumen_jugo_L=Volumen_jugo*1000
        Lista_Contenido[i][7]=Lista_Contenido[i][6]*1000.0
        if(i==0):
            #Temperatura_Entrada=Temperatura ambiente
            Lista_Contenido[i][8]=G34         
        else:
            #Temperatura_Entrada=G37+0.2209*math.exp(0.0557*Concentracion_solidos_inicial)
            Lista_Contenido[i][8]=G37+0.2209*math.exp(0.0557*Lista_Contenido[i][0])
        if(i==0):    
            #Temperatura_Salida=Supuesta
            Lista_Contenido[i][9]=60.0        
        else:    
            #Temperatura_Salida=G37+0.2209*math.exp(0.0557*Concentracion_solidos_final)
            Lista_Contenido[i][9]=G37+0.2209*math.exp(0.0557*Lista_Contenido[i][1])    
        #Entalpia_Vaporizacion=(2492.9-(2.0523*Temperatura_Entrada))-(0.0030752*(Temperatura_Entrada**2))
        Lista_Contenido[i][10]=(2492.9-(2.0523*Lista_Contenido[i][8]))-(0.0030752*(Lista_Contenido[i][8]**2))
        #Masa_Agua_Evaporar=Masa_jugo_de_entrada-(Masa_jugo_de_entrada*Concentracion_solidos_inicial/Concentracion_solidos_final)
        Lista_Contenido[i][11]=Lista_Contenido[i][3]-(Lista_Contenido[i][3]*Lista_Contenido[i][0]/Lista_Contenido[i][1])
        #Calor_por_Etapa=(Masa_jugo_de_entrada*Calor_Especifico_P_Cte_jugo*(Temperatura_Salida-Temperatura_Entrada)+Masa_Agua_Evaporar*Entalpia_Vaporizacion)/3600
        Lista_Contenido[i][12]=(Lista_Contenido[i][3]*Lista_Contenido[i][4]*(Lista_Contenido[i][9]-Lista_Contenido[i][8])+Lista_Contenido[i][11]*Lista_Contenido[i][10])/3600.0
    
    #Mostrar en interfaz grafica
    #Rotulos
    Label(Panel_6, text="Orden según el flujo de gas").grid(row=1, column=0)
    Label(Panel_6, text="Concentracion de Solidos Inicial [ºBrix]").grid(row=2, column=0)
    Label(Panel_6, text="Concentracion de Solidos Final [ºBrix]").grid(row=3, column=0)
    Label(Panel_6, text="Concentracion de Solidos Promedio [ºBrix]").grid(row=4, column=0)
    Label(Panel_6, text="Masa de Jugo Entrada [Kg]").grid(row=5, column=0)
    Label(Panel_6, text="Calor Especifico P Cte jugo [KJ/Kg °C]").grid(row=6, column=0)
    Label(Panel_6, text="Densidad del Jugo [kg/m3]").grid(row=7, column=0)
    Label(Panel_6, text="Volumen de jugo [m^3/kg]").grid(row=8, column=0)
    Label(Panel_6, text="Volumen de jugo [L]").grid(row=9, column=0)
    Label(Panel_6, text="Temperatura de Entrada [ºC]").grid(row=10, column=0)
    Label(Panel_6, text="Temperatura de Salida [ºC]").grid(row=11, column=0)
    Label(Panel_6, text="Entalpia de Vaporización [KJ/kg]").grid(row=12, column=0)
    Label(Panel_6, text="Masa de Agua a Evaporar [Kg]").grid(row=13, column=0)
    Label(Panel_6, text="Calor Nece Calc por Etapa [KW]").grid(row=14, column=0)
    
    for i in range (Etapas):
        Label(Panel_6, text=" "+str(i+1)).grid(row=1, column=i+1)
        
    for i in range (13):
        for j in range (Etapas):
            Label(Panel_6, text=" "+str(round(Lista_Contenido[j][i],3))).grid(row=i+2, column=j+1)
    
   

"Calculos iniciales"    
if __name__== "__main__":
    Helvfont = font.Font(family="Helvetica", size=18, weight="bold")
    Label(root, text="SISTEMA EXPERTO", font=Helvfont).pack()
    Label(root, text=" ").pack()
    Paneles = ttk.Notebook(root)
    Panel_1 = ttk.Frame(Paneles)
    Panel_2 = ttk.Frame(Paneles)
    Panel_3 = ttk.Frame(Paneles)
    Panel_4 = ttk.Frame(Paneles)
    Panel_5 = ttk.Frame(Paneles)
    Panel_6 = ttk.Frame(Paneles)
    Paneles.add(Panel_1, text='Datos de entrada 1')
    Paneles.add(Panel_2, text='Datos de entrada 2')
    Paneles.add(Panel_3, text='Datos de salida 1')
    Paneles.add(Panel_4, text='Datos de salida 2')
    Paneles.add(Panel_5, text='Datos de salida 3')
    Paneles.add(Panel_6, text='Diseño geometrico inicial')
    "Crear interfaz grafica y calculos iniciales"
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
            
    Cantidad_Etapas=StringVar(value="7")
    Label(Panel_6, text="Cantidad de etapas: ").grid(row=0, column=0)
    Entry(Panel_6, width=20, textvariable=Cantidad_Etapas).grid(padx=5, row=0, column=1)     
    #Función para publicar
    Button(Panel_2, text="Actualizar", command=Actualizar_Valores).grid(pady=5, row=i+1, column=1)     
    
    #Expansión panel
    Paneles.pack(expand=1, fill='both')
    root.mainloop()