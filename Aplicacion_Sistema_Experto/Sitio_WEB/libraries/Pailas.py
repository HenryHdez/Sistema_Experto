# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 08:53:50 2020

@author: hahernandez
"""
import math
import random
"Funciones para realizar los calculos de la geometría de la hornilla"

#Estimar volumen de las pailas
def Precalentadora_Plana(H_fl,H_fn,A,L):
    #Parametros fijos para calcular el TCC
    #N_Aletas	
    #h_Aletas	
    Ang=68*math.pi/180
    Area=(A*L)+(2*A*H_fn)+(2*H_fn*L)	
    Volumen_Fon=(H_fn*A*L)	
    Volumen_total=(A*H_fn*L)+(A+H_fl/math.tan(Ang))*H_fl*L
    return Volumen_Fon
	
def Pirtubular_Circular_Aleteada_Clarificadora(H_fl,H_fn,A,L,dT,nT):
    Ang=68*math.pi/180
    Volumen_Fon=((H_fn*A)-(((math.pi/4)*(dT**2))*nT))*L
    Volumen_total=Volumen_Fon+(L*H_fl*(A+H_fl/math.tan(Ang)))
    return Volumen_total

def Semicilindrica_pequena(H_fn,A,H_fl):
    R=((A/2)**2+H_fn**2)/(2*H_fn)	
    Ang=68*math.pi/180
    VTJ=(math.pi*H_fn**2*(3*R-H_fn))/3
    A1=math.pi*((A/2)**2)
    x=A+2*(H_fl/math.tan(Ang))
    A2=x**2
    VFA=(H_fl*(A1+A2+math.sqrt(A1*A2)))/3
    VTPA=VFA+VTJ	
    return VTJ

#Crear ventana para mostrar partes de la hornilla
#Dimensiones de la lamina 4*10 pies
def Mostrar_pailas(Lista_Contenido, Etapas):
    Tipo_paila=[]
    Numero_maximo_geometrias=3
    for i in range(Etapas):
        Tipo_paila.append(random.randint(1,Numero_maximo_geometrias))
    #Ascenso a la colina
    for i in range(Etapas-1,-1,-1):
        f_1=1000
        iteraciones=0
        H_fl = random.uniform(0, 1)
        H_fn = random.uniform(0, 0.3)
        A    = random.uniform(0, 1)
        L    = random.uniform(0, 4)
        dT   = random.uniform(0, 2)
        nT   = random.randint(1,20)       
        if Tipo_paila[i]==1:
            f=abs(Lista_Contenido[i][6]-Precalentadora_Plana(H_fl,H_fn,A,L))
            f=(f/Lista_Contenido[i][6])*100.0
        elif Tipo_paila[i]==2:
            f=abs(Lista_Contenido[i][6]-Pirtubular_Circular_Aleteada_Clarificadora(H_fl,H_fn,A,L,dT,nT))
            f=(f/Lista_Contenido[i][6])*100.0
        else:
            f=abs(Lista_Contenido[i][6]-Semicilindrica_pequena(H_fn,A,H_fl))
            f=(f/Lista_Contenido[i][6])*100.0
        paso=1
        while (0.2<f):
            if(f_1<f):
                H_fl = H_fl_1
                H_fn = H_fn_1
                A    = A_1
                L    = L_1
                dT   = dT_1
                nT   = nT_1
                if Tipo_paila[i]==1:
                    f=abs(Lista_Contenido[i][6]-Precalentadora_Plana(H_fl,H_fn,A,L))
                    f=(f/Lista_Contenido[i][6])*100.0
                elif Tipo_paila[i]==2:
                    f=abs(Lista_Contenido[i][6]-Pirtubular_Circular_Aleteada_Clarificadora(H_fl,H_fn,A,L,dT,nT))
                    f=(f/Lista_Contenido[i][6])*100.0
                else:
                    f=abs(Lista_Contenido[i][6]-Semicilindrica_pequena(H_fn,A,H_fl))
                    f=(f/Lista_Contenido[i][6])*100.0
            H_fl_1 = abs(H_fl+random.uniform(-1*paso, paso))
            H_fn_1 = abs(H_fn+random.uniform(-1*paso, paso))
            A_1    = abs(A+random.uniform(-1*paso, paso))
            L_1    = abs(L+random.uniform(-1*paso, paso))
            dT_1   = random.uniform(0, 2)
            nT_1   = random.randint(1,20)
            if Tipo_paila[i]==1:
                f_1=abs(Lista_Contenido[i][6]-Precalentadora_Plana(H_fl_1,H_fn_1,A_1,L_1))
                f_1=(f_1/Lista_Contenido[i][6])*100.0
            elif Tipo_paila[i]==2:
                f_1=abs(Lista_Contenido[i][6]-Pirtubular_Circular_Aleteada_Clarificadora(H_fl_1,H_fn_1,A_1,L_1,dT_1,nT_1))
                f_1=(f_1/Lista_Contenido[i][6])*100.0
            else:
                f_1=abs(Lista_Contenido[i][6]-Semicilindrica_pequena(H_fn_1,A_1,H_fl_1))            
                f_1=(f_1/Lista_Contenido[i][6])*100.0
            iteraciones=iteraciones+1    
        if Tipo_paila[i]==1:
            print("Etapa: "+str(i+1))
            print("Cantidad en Litros esperada: "+str(Lista_Contenido[i][6]))
            print("Cantidad en Litros estimada: "+str(Precalentadora_Plana(H_fl,H_fn,A,L)))
            print("Tipo seleccionado: Precalentadora plana")
            print("H_fl: "+str(H_fl))
            print("H_fn: "+str(H_fn))
            print("A: "+str(A))
            print("L: "+str(L))
        elif Tipo_paila[i]==2:
            print("Etapa: "+str(i+1))
            print("Cantidad en Litros esperada: "+str(Lista_Contenido[i][6]))
            print("Cantidad en Litros estimada: "+str(Pirtubular_Circular_Aleteada_Clarificadora(H_fl,H_fn,A,L,dT,nT)))
            print("Tipo seleccionado: Pirotubular circular aleteada")
            print("H_fl: "+str(H_fl))
            print("H_fn: "+str(H_fn))
            print("A: "+str(A))
            print("L: "+str(L))
            print("Diametro de la tuberia: "+str(dT))
            print("Numero de tubos: "+str(nT))
        else:
            print("Etapa: "+str(i+1))
            print("Cantidad en Litros esperada: "+str(Lista_Contenido[i][6]))
            print("Cantidad en Litros estimada: "+str(Semicilindrica_pequena(H_fn,A,H_fl)))
            print("Tipo seleccionado: Semicilindrica pequeña")
            print("H_fl: "+str(H_fl))
            print("H_fn: "+str(H_fn))
            print("A: "+str(A)) 
        print("________>>>>>>>>>>>>>____________")
        print(str(iteraciones))
        print(str(f)) 