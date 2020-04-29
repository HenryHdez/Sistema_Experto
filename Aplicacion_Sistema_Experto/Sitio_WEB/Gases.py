# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 07:52:53 2020

@author: hahernandez
"""
import math
from Modulo1 import *
from Modulo2 import *
from Modulo21 import *
#from Modulo3 import *
from Modulo4 import *

def Calcular_parrillas(Area_Calculada,Capacidad_Hornilla,i):
    """>>>----------Algoritmo para el calculo de las parrillas-----------<<<<<<<<<"""
    Ancho_seccion=0.155	
    Longitudes=[0.75, 1, 1.25, 1.5]
    if(Capacidad_Hornilla<40):
        Longitud_Seccion=0.5
    else:
        Longitud_Seccion=Longitudes[i]        
    Temp=math.ceil(Area_Calculada/(Ancho_seccion*Longitud_Seccion))
    
    if (Temp>7):
        Temp2=math.ceil(Temp/2)
    else:
        Temp2=Temp
        
    if (Temp<7):
        Temp3=1
    else:
        Temp3=math.ceil(Temp/Temp2)  
        
    Temp4=Temp2*Ancho_seccion
    if(Temp4<0.62):
        Temp4=5
    
    Numero_secciones_An1=Temp
    Numero_secciones_An2=Temp2  
    Numero_secciones_Lon=Temp3
    Secciones_totales=Temp2*Temp3
    Ancho_parrilla=Temp4
    Area_Calculada=Longitud_Seccion*Temp3*Temp4
    
    if(Capacidad_Hornilla<40):
        Area_Calculada=(Longitud_Seccion*Numero_secciones_Lon)*(Ancho_seccion*Numero_secciones_An2)  
    
    return [Ancho_seccion, Longitud_Seccion, Numero_secciones_An1, Numero_secciones_An2, Numero_secciones_Lon,
            Secciones_totales, Ancho_parrilla, Area_Calculada]
                
def Propiedades(Diccionario_Entr, Diccionario_Pailas):
#    print(Diccionario_Entr)
#    print(Diccionario_Pailas)
    #Valores iniciales
    Masa_Bagazo=float(Diccionario_Entr['Capacidad Estimada de la hornilla'])*float(Diccionario_Entr['Factor Consumo Bagazo'])
    Cantidad_Pailas=int(Diccionario_Pailas['Etapas'])   
    Humedad_bagazo=float(Diccionario_Entr['Humedad del bagazo'])
    Exceso_aire=float(Diccionario_Entr['Exceso de Aire'])
    print(Exceso_aire)
    Temperatura_ambiente=(float(Diccionario_Entr['CSS panela'])*100.0)+273.0
    Eficiencia_Combustion=0.95 #Lo esperado en la combustión    
    Humedad_aire=0.001
    #Composición del bagazo en %
    Carbono=0.470
    Hidrogeno=0.065
    Oxigeno=0.440
    Escorias=0.025
    Masa_Bagazo_Seco=Masa_Bagazo*(1-(Humedad_bagazo))
    #Masa molar    
    C=12.011
    H2=2.016
    CO2=44.010
    CO=28.010
    H2O=18.015
    O2=31.999
    N2=28.013
    #Masa molar (Entrada)
    C_bagazo=Masa_Bagazo_Seco*Carbono/C
    H2_bagazo=Masa_Bagazo_Seco*Hidrogeno/H2
    O2_bagazo=Masa_Bagazo_Seco*Oxigeno/O2
    H2O_bagazo=Humedad_bagazo*Masa_Bagazo/H2O
    O2_req=(C_bagazo+(H2_bagazo/2))-O2_bagazo
    O2_sum=O2_req*Exceso_aire
    N2_sum=O2_sum*3.76
    H2O_aire=(((N2_sum*N2)+(O2_sum*O2))*Humedad_aire)/H2O
    #Masa molar(Salida)
    CO2_producidos=Eficiencia_Combustion*C_bagazo*1000.0
    CO_producidos=(C_bagazo*1000)-CO2_producidos
    H2O_producidos=H2_bagazo*1000.0
    H2O_Totales=H2O_producidos+((H2O_aire+H2O_bagazo)*1000.0)
    O2_producidos=((O2_sum-O2_req)*1000.0)+(CO_producidos/2)
    N2_producidos=N2_sum*1000.0
    Gases_Totales=CO2_producidos+CO_producidos+H2O_Totales+O2_producidos+N2_producidos
    Temperatura_llama= 1180.0 + 273.15
    masa_Gases_Total= (CO2_producidos*CO2)+(CO_producidos*CO)+(H2O_Totales*H2O)+(O2_producidos*O2)+(N2_producidos*N2)
    Potencia_Inicial_Gas=float(Diccionario_Entr['Calor Suministrado'])
    
    CO2_producidos_2=CO2*CO2_producidos/1000.0
    CO_producidos_2=CO*CO_producidos/1000.0
    H2O_Totales_2=(H2O*H2O_Totales)/1000.0
    O2_producidos_2=(O2*O2_producidos)/1000.0
    N2_producidos_2=(N2*N2_producidos)/1000.0
    Gas_Total=CO2_producidos_2+CO_producidos_2+H2O_Totales_2+O2_producidos_2+N2_producidos_2
    Flujo_Masico=Gas_Total/3600.0
    
    CO2_producidos_3=CO2_producidos/Gases_Totales
    CO_producidos_3=CO_producidos/Gases_Totales
    H2O_Totales_3=H2O_Totales/Gases_Totales
    O2_producidos_3=O2_producidos/Gases_Totales
    N2_producidos_3=N2_producidos/Gases_Totales
    Gas_Total_2=CO2_producidos_3+CO_producidos_3+H2O_Totales_3+O2_producidos_3+N2_producidos_3  
    
    Presion=float(Diccionario_Entr['Presion Atmosferica'])/760.0
    print('Presión= '+ str(Presion))
    Temperatura_Flama_Ad=Tadiabatica(Exceso_aire,Eficiencia_Combustion,Humedad_bagazo,Humedad_aire)
    print(Temperatura_Flama_Ad)
    Velocidad_I=(Flujo_Masico/Densidad_kgm3(CO_producidos_3,CO2_producidos_3,N2_producidos_3,O2_producidos_3,H2O_Totales_3,Presion*101.325,Temperatura_Flama_Ad))/0.32
    print(Velocidad_I)
    Energia_inicial_Gas=DH_KJKmol(25,Temperatura_Flama_Ad,CO_producidos/1000,CO2_producidos/1000,N2_producidos/1000,O2_producidos/1000,H2O_Totales/1000)/3600
    print(Energia_inicial_Gas)

    Perdida_total=Energia_inicial_Gas*0.14
    
    
    print(Calcular_parrillas(1.109,120,1))
    """>>>----------Geometrias basadas en el diseño inicial-----<<<<"""
    
    #Lista_Geometrias_F[0][Cantidad de pailas]=Area de Flujo
    #Lista_Geometrias_F[1][Cantidad de pailas]=Perimetro
    #Lista_Geometrias_F[2][Cantidad de pailas]=Altura del Ducto
    #Lista_Geometrias_F[3][Cantidad de pailas]=Area Paredes Radiación
    #Lista_Geometrias_F[4][Cantidad de pailas]=Area Piso Radiación
    #Lista_Geometrias_F[5][Cantidad de pailas]=Area Paredes Piso y TechoPara Perdidas
#    Lista_Geometrias_F=[]
#    Lista_Geometrias_C=[]  
#    #Se debe cambiar por las formulas para estimar el Area, perimetro ...
#    for i in range(int(Diccionario_Pailas['Etapas'])):
#        for j in range (6):
#            Lista_Geometrias_C.append(float(j))
#        Lista_Geometrias_F.append(Lista_Geometrias_C)
#        Lista_Geometrias_C=[] 
#        
#    print(Lista_Geometrias_F)
    
#    #Supuesto
#    Area_Chimenea=53.327
#    Area_Total=105.964	
#    
#    Calores_Transferidos_Qtt=[]
#    for i in range(int(Diccionario_Pailas['Etapas'])):
#        Calores_Transferidos_Qtt.append(random.uniform(45, 70))
#        
#    print(Calores_Transferidos_Qtt)
#    
#    Lista_Contenido_Qtt=[]
#    Lista_columnas_Qtt=[]  
#    #Caracteristicas de las celdas de cada columna
#    #Fila 0 Calor del Gas antes de Paila
#    #Fila 1 Calor Gas despues paila
#    #Fila 2 Temperarura antes de Paila
#    #Fila 3 Temperatura despues de Paila
#    #Fila 4 Temperatura Bajo la Paila
#    #Fila 5 Perdidas
#    #Fila 6 Pedidas según 14%
#
#    for i in range(int(Diccionario_Pailas['Etapas'])):
#        for j in range (7):
#            Lista_columnas_Qtt.append(float(i+j))
#        Lista_Contenido_Qtt.append(Lista_columnas_Qtt)
#        Lista_columnas_Qtt=[] 
#        
#    print(Lista_Contenido_Qtt)


def EYE_1():
    Error=0.0
    tolerancia=0.0
    Numero_pailas=0.0
    tolerancia = 0.000001
    Numero_pailas=np.zeros((5,4))
    #Numero_pailas = Cells(5, 4) #' valor fijo
    #Error = Range("M182")
    
    while Error > tolerancia:
        for i in range(0,Numero_pailas):
            print(9)
            #Cells(114, i + 4) = Cells(180, i + 4)
        #Error = Range("M182")
    print(9)

def EYE_2():
    Error = 0.0
    tolerancia = 0.0
    Xp1 = 0.0
    Xp2 = 0.0
    Fx = 0.0
    Fxc = 0.0
    Bz = 0.0
    Bz2 = 0.0
    Numero_pailas = 0.0
    #Calor Etapa
    Iniciales=float(Diccionario_pailas['Calor Nece Calc por Etapa [KW]'])
#    for i in range(0,Numero_pailas):
#        #Cells(114, i + 4) = Cells(41, i + 4)
#        print(1)
    tolerancia = 0.000001
    Xp1 = float(Diccionario_Entr['Calor Nece Calc por Etapa [KW]'])
    #Xp1 = Cells(12, 4) #' valor fijo
    #CSS jugo concentrado = CSS jugo panela
    Xp2 = float(Diccionario_Entr['CSS panela'])
    Error = abs(Xp1 - Xp2)
    Bz = 3
    Niter = 0   
    
    while Error > tolerancia and Niter < 50.0:
        Niter = Niter + 1
        #Range("l183") = Niter
        
        #Cells(4, 4) = Bz
        #EYE_1()
        #Fx=CSS concentrado - CSS Calculado
        #Fx = Cells(76, 5) - Cells(12, 4)
        #Factor de consumo de bagazo
#        Cells(4, 4) = Bz + tolerancia
        #EYE_1()
        #Fxc=CSS concentrado - CSS Calculado
        #Fxc = Cells(76, 5) - Cells(12, 4)
        Der = (Fxc - Fx) / tolerancia
        B = Fx - Der * Bz
        Bz2 = -B / Der
        Error = abs(Bz - Bz2)
        if Error < 0.5:
            Bz = Bz2
        else:
            if Bz - Bz2 > 0.5:
                Bz = Bz - 0.5
            else:
                Bz = Bz + 0.5
                
Propiedades(Diccionario,Diccionario_2)