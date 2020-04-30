# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 07:52:53 2020

@author: hahernandez
"""
import math
import numpy as np
from Modulo1 import *
from Modulo2 import *
from Modulo21 import *
#from Modulo3 import *
from Modulo4 import *

def Calcular_parrillas(Area_Calculada,Capacidad_Hornilla,i,Calor_suministrado,Tipo_ladrillo,Temperatura_ambiente,Temperatura_Flama_Ad):
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

    #>>>>>>-------------Aqui se pone la geometría de la camara para hallar el vólumen
    Volumen_Calculado=Calor_suministrado/300
    Ancho_camara=Ancho_parrilla+0.2
    Longitud_Camara=(Longitud_Seccion*Numero_secciones_Lon)+0.1
    Altura_camara=Volumen_Calculado/(Ancho_camara*Longitud_Camara)
    
    #Calculo de la pared con respecto a los ladrillos
    Area_Cam=2*((Ancho_camara*Longitud_Camara)+(Ancho_camara*Altura_camara)+(Longitud_Camara*Altura_camara))
    Coef_Conduct_Termica=0
    if(Tipo_ladrillo=='Refractario'):
        Coef_Conduct_Termica=0.29
    else:
        if(Tipo_ladrillo=='Semirefractario'):
            Coef_Conduct_Termica=0.45
        else:
            Coef_Conduct_Termica=0.9
    Esp_Camara=0.12
    Aux=-264.44+(1.03*Temperatura_Flama_Ad)
    Q_Perd_Camara=(Coef_Conduct_Termica*Area_Cam)*((Aux-Temperatura_ambiente)/Esp_Camara)
    return Q_Perd_Camara
                
def Propiedades(Diccionario_Entr, Diccionario_Pailas):
#    print(Diccionario_Entr)
#    print(Diccionario_Pailas)
    #Valores iniciales
    Masa_Bagazo=float(Diccionario_Entr['Capacidad Estimada de la hornilla'])*float(Diccionario_Entr['Factor Consumo Bagazo'])
    Cantidad_Pailas=int(Diccionario_Pailas['Etapas'])   
    Humedad_bagazo=float(Diccionario_Entr['Humedad del bagazo'])
    Exceso_aire=float(Diccionario_Entr['Exceso de Aire'])
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
    #print('Presión= '+ str(Presion))
    Temperatura_Flama_Ad=1160#=Tadiabatica(Exceso_aire,Eficiencia_Combustion,Humedad_bagazo,Humedad_aire)
    #print(Temperatura_Flama_Ad)
    Velocidad_I=(Flujo_Masico/Densidad_kgm3(CO_producidos_3,CO2_producidos_3,N2_producidos_3,O2_producidos_3,H2O_Totales_3,Presion*101.325,Temperatura_Flama_Ad))/0.32
    #print(Velocidad_I)
    Energia_inicial_Gas=DH_KJKmol(25,Temperatura_Flama_Ad,CO_producidos/1000,CO2_producidos/1000,N2_producidos/1000,O2_producidos/1000,H2O_Totales/1000)/3600
   #print(Energia_inicial_Gas)

    Perdida_total=Energia_inicial_Gas*0.14
    
    Tipo_ladrillo=0
    Q_perdido_cam = Calcular_parrillas(float(Diccionario_Entr['Area de Parrilla']),
                                       float(Diccionario_Entr['Capacidad Estimada de la hornilla']),
                                       Tipo_ladrillo,
                                       float(Diccionario_Entr['Calor Suministrado']),
                                       'Refractario',
                                       float(Diccionario_Entr['Temperatura Ambiente']),
                                       Temperatura_Flama_Ad)
    '''>>>>>>>>---------------Calculo de los gases----------------<<<<<<<<<<<<'''
    Calor_transferido_inicial=Diccionario_Pailas['Calor Nece Calc por Etapa [KW]']#[47.135,59.740,78.743,64.603,57.385,62.503,10.596]#100*(np.random.rand(Cantidad_Pailas))
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>Este arreglo inicia por la ultima paila<<<<<<<<<<<<<<<<<<<<<<<
    Gas_Paila=[]
    Gases_Consolidado=[] 
    Temp1=0
    Temp2=0
    for i in range(Cantidad_Pailas):
        if(i==0):
            Temp1=Energia_inicial_Gas-(Q_perdido_cam/1000)
        else:
            Temp1=Temp2
        Gas_Paila.append(Temp1)                                     #Calor antes de la paila
        aux=Temp1-(0.25*Perdida_total)-Calor_transferido_inicial[i]
        Gas_Paila.append(aux)        
        mem1= abs(Tcalculada(Temp1,                                 #Temperatura antes de la paila
                             Gas_Total,
                             CO_producidos_3,
                             CO2_producidos_3,
                             N2_producidos_3,
                             O2_producidos_3,
                             H2O_Totales_3))                        #Calor despues de la paila
        Gas_Paila.append(mem1)
        mem2= abs(Tcalculada(aux,                                   #Temperatura despues de la paila
                             Gas_Total,
                             CO_producidos_3,
                             CO2_producidos_3,
                             N2_producidos_3,
                             O2_producidos_3,
                             H2O_Totales_3))
        Gas_Paila.append(mem2)
        Promedio_mem=(mem1+mem2)/2                                  #Temperatura bajo la paila
        Gas_Paila.append(Promedio_mem)
        Gas_Paila.append(0)                                         #Perdidas (Falta modelo)
        Gas_Paila.append(0.25*Perdida_total)                        #Perdida 14%
        Gases_Consolidado.append(Gas_Paila)                         #Consolidado
        Gas_Paila=[]
        Temp2=aux        
    
    Gases_Consolidado_t=np.transpose(np.around(Gases_Consolidado,3))
    '''>>>>>>>>---------------Estimar el calor por convección y radiación----------------<<<<<<<<<<<<'''
    Temperarura_Gases=Gases_Consolidado_t[4]  
    C_Boltzman=0.0000000567
    Emisividad_Fondo_paila=0.4 
    Emisividad_Ducto=0.96
    Factor_forma_Pared=0.4
    Factor_Forma_Piso=0.2
    Area_Paredes_radiantes=np.random.random(Cantidad_Pailas)              #Faltan ecuaciones
    Area_Piso_radiante=np.random.random(Cantidad_Pailas)                  #Faltan ecuaciones
    Area_Flujo=np.random.random(Cantidad_Pailas)                          #Faltan las ecuaciones
    Area_Lisa=np.random.random(Cantidad_Pailas)                           #Faltan las ecuaciones
    Perimetro=np.random.random(Cantidad_Pailas)                           #Faltan las ecuaciones
    Temperatura_Superficie=np.random.random(Cantidad_Pailas)              #Faltan las ecuaciones
    Emisividad_gases=np.random.random(Cantidad_Pailas)                    #Revisar nomograma
    Calor_Q_gases=[]
    for i in range(1):
    #'''>>>>>>>>---------------Calor por convección----------------<<<<<<<<<<<<'''
        aux=Cp(Temperarura_Gases[i],                                                                                #Calor Especifico a Presión Cte           
               CO_producidos_3,
               CO2_producidos_3,
               N2_producidos_3,
               O2_producidos_3,
               H2O_Totales_3)
        aux2=Densidad_kgm3(CO_producidos_3,                                                                         #Densidad
                           CO2_producidos_3,
                           N2_producidos_3,
                           O2_producidos_3,
                           H2O_Totales_3,
                           Presion*101.325,
                           Temperarura_Gases[i])
        visc_dina =0.0000175+(0.0000000335*Temperarura_Gases[i])                                                    #Viscosidad dinámica
        Coef_teri =(0.0229+(0.0000647*Temperarura_Gases[i]))/1000                                                   #Coeficiente conductividad térmica
        vel_gase1 =(masa_Gases_Total/(3600*1000))/(aux2*Area_Flujo[i])                                              #Velocidad del gas
        visc_sup1 =0.0000175+(0.0000000335*Temperatura_Superficie[i])                                               #Viscocidad dinamica superficial
        visc_cine =visc_dina/aux2                                                                                   #Viscocidad cinematica
        n_plant   =visc_dina*aux/Coef_teri                                                                          #N° Prandlt
        Diametro_h=4*Area_Flujo[i]/Perimetro[i]                                                                     #Diametro hidraulico
        n_reynol  =(aux2*vel_gase1*Diametro_h)/visc_dina                                                            #Numero de Reynolds
        Nu1=((0.664*n_reynol)**(1/2))*(n_plant**(1/3))                                                              #No. Nusselt  Nre<1e5
        Nu2=(0.037*(n_reynol**0.8)*n_plant)/(1+(2.443*(n_reynol**-0.1))*((n_plant**0.67)-1))                        #No. Nusselt  Nre>5e5
        Nu3=((Nu1**2)+(Nu2**2))**(0.5)                                                                              #No. Nusselt  1e5< Nre <5e5
        Nu4=((0.4*(n_reynol**0.5))+0.06*(n_reynol**(2/3)))*((n_plant**0.4)*((visc_dina/visc_sup1)**(1/4)))          #No. Nusselt P.S.E
        Nu5=(2.36*((0.027*(n_reynol**0.8))*(n_plant**(1/3))*(visc_dina/visc_sup1)**(1/4)))-13.6                     #No. Nusselt Pirotubular Re<2,3e3
        Coef_conv=Coef_teri*Nu4/Diametro_h                                                                          #Coeficiente de convección corregido
        Calor_conv=Area_Lisa[i]*Coef_conv*(Temperarura_Gases[i]-Temperatura_Superficie[i])                          #Calor por convección
        T_pared=abs(-264.44+(1.03*Temperarura_Gases[i]))+273                                                        #Temperatura de la pared
        T_piso=abs(-87.31+(0.79*Temperarura_Gases[i]))+273                                                          #Temperatura del piso
        '''>>>>>>>>---------------Calor por radiación----------------<<<<<<<<<<<<'''
        Temp_Fon=Temperatura_Superficie[i]+273,15                                                                   #Temperatura del fondo de la paila
        T_pared=841+273
        T_piso=761+273
        Temp_Fon=400+273
        Area_Lisa[0]=0.614
        Area_Paredes_radiantes[0]=1.88   
        Area_Piso_radiante[0]=0.8        
        Emisividad_gases[0]=0.119        
        Temperarura_Gases[0]=1073+271        
        Q_Paredes=2*(C_Boltzman*(T_pared**4-Temp_Fon**4)/((1-Emisividad_Fondo_paila)/(Area_Lisa[i]*Emisividad_Fondo_paila)+1/(Area_Lisa[i]*Factor_forma_Pared)+(1-Emisividad_Ducto)/(Area_Paredes_radiantes[i]/Emisividad_Ducto)))/1000
        Q_Piso=((C_Boltzman*((T_piso**4)-(Temp_Fon**4)))/((1-Emisividad_Fondo_paila)/(Area_Lisa[i]*Emisividad_Fondo_paila)+1/(Area_Lisa[i]*Factor_Forma_Piso)+(1-Emisividad_Ducto)/(Area_Piso_radiante[i]/Emisividad_Ducto)))/1000
        Q_Gas=((C_Boltzman*Area_Lisa[i]*Emisividad_Fondo_paila*Emisividad_gases[i]*(Temperarura_Gases[i]**4-Temp_Fon**4))/(1-(1-Emisividad_Fondo_paila)*(1-Emisividad_gases[i])))/1000
        Q_Total_paila=Q_Paredes+Q_Piso+Q_Gas
        print(Q_Total_paila)
        Calor_Q_gases.append([aux, aux2, visc_dina, Coef_teri, vel_gase1, visc_sup1,
                       visc_cine, n_plant, Diametro_h, n_reynol, Nu1, Nu2, Nu3,
                       Nu4, Nu5, Coef_conv, Calor_conv, T_pared, T_piso])
    #print(Calor_Q_gases)

    
    
    
    
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
#    Calores_Transferidoas_Qtt=[]
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