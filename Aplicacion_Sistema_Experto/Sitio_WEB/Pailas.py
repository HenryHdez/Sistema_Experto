# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 08:53:50 2020

@author: hahernandez
"""
import math
import random
"Librería que realiza los calculos de la geometría de la hornilla"

#Funciones para estimar el volumen de cada paila, donde
    #Hfn        Altura de fondo
    #Hfa o hfl  Alftura falca
    #hal        Altura aletas
    #An o A     Ancho de paila
    #Hc         Altura de casco
    #H          Altura total

def Cantidad_Aletas(A,B_Aletas):
    #El numero de aletas es un parámetro que varia en función del 
    #ancho de la paila.Lla separación minima entre ellas es de 7cm
    if(B_Aletas==True):
        Separacion_Aletas=0.07
        return round(A/Separacion_Aletas,0)	
    else:
        return 0
                
def Semiesferica(H_fn,A,H_fl):
    R=(((A/2)**2)+(H_fn**2))/(2*H_fn)	
    Ang=68*math.pi/180
    VTJ=(math.pi*(H_fn**2)*(3*R-H_fn))/3
    A1=math.pi*((A/2)**2)
    x=A+2*(H_fl/math.tan(Ang))
    A2=x**2
    VFA=(H_fl*(A1+A2+math.sqrt(A1*A2)))/3
    Volumen_Total=VFA+VTJ	
    return Volumen_Total

def Semicilindrica(H,Hc,A,L,Hfa,B_Aletas):
    #la altura de las aletas es fijo por ahora 10cm
    N_Aletas_Canal=Cantidad_Aletas(A,B_Aletas)
    h_Aletas=0.01
    Ang=68*math.pi/180
    #Oculto en la base
    R=((A/2)**2+(H**2))/(2*H)
    d=R-A
    Teta=2*math.asin((A/2)/R)
    s=Teta*R
    Asccil=(R**2)*(Teta)/2-((R**2)*math.sin(Teta)/2)
    Vcil=Asccil*L
    Acil=s*L
    Rca=((R**2)+(Hc**2))/(2*Hc)
    Vsc=(math.pi*(Hc**2)*(3*Rca-Hc)/3)
    Vca=(H/(R*2))*Vsc
    Asc=2*math.pi*Rca*Hc
    Aca=Asc*(H/(R*2))
    x1=A+2*(Hfa/math.tan(Ang))
    x2=(L+2*Hc)+2*(Hfa/math.tan(Ang))
    A1=x1*x2
    R1=((A/2)**2+(Hc**2))/(2*Hc)
    Teta1=2*math.asin((A/2)/R1)
    Ax=((R1**2)*Teta1/2)-((R1**2)*math.sin(Teta1)/2)
    A2=A*L+2*Ax
    V=(Hfa*(A1+A2+math.sqrt(A1*A2)))/3
    #No oculto en la base
    Arco=Acil+(2*Aca)
    VTJ=Vcil+(2*Vca)
    VFA=V
    Volumen_Total=VTJ+VFA
    return Volumen_Total
       
def Plana(H_fl,H_fn,A,L,B_Aletas):
    #La altura de las aletas es fijo por ahora 10cm
    N_Aletas=Cantidad_Aletas(A,B_Aletas)
    h_Aletas=0.01
    Ang=68*math.pi/180
    Area=(A*L)+(2*A*H_fn)+(2*H_fn*L)	
    Volumen_Fon=(H_fn*A*L)	
    Volumen_Total=(A*H_fn*L)+(A+H_fl/math.tan(Ang))*H_fl*L
    """Otros parámetros"""
    Porcentaje_Llenado=Volumen_Fon/Volumen_Total
    Area_TCC=(2*h_Aletas*L*N_Aletas)+Area
    return Volumen_Total
	
def Pirotubular_Circular(H_fl,H_fn,A,L,B_Aletas):
    #dT es el diametro del tubo
    #nT es el numero de tubos
    #La altura de las aletas es fijo por ahora 10cm
    N_Aletas=Cantidad_Aletas(A,B_Aletas)
    h_Aletas=0.01
    Ang=68*math.pi/180
    dT=H_fn/3
    nT=round((A+dT)/(dT*2))
    Volumen_Fon=((H_fn*A)-(((math.pi/4)*(dT**2))*nT))*L
    Volumen_Total=Volumen_Fon+(L*H_fl*(A+H_fl/math.tan(Ang)))
    """Otros parámetros"""
    Porcentaje_Llenado=Volumen_Fon/Volumen_Total
    Area_TCC=((((H_fn)*(A))-(2*((math.pi/4)*dT**2)*nT))+(2*(H_fn*L)+(A*L)))+(math.pi*dT*L*nT)+(2*(L*h_Aletas)+(2*(h_Aletas))*N_Aletas)
    return Volumen_Total

def Pirotubular_Cuadrada(H_fl,H_fn,A,L,B_Aletas):
    #lT es la medida de un lado de un tubo cuadrado
    #nT es el numero de tubos
    #La altura de las aletas es fijo por ahora 10cm
    N_Aletas=Cantidad_Aletas(A,B_Aletas)
    h_Aletas=0.01
    Ang=68*math.pi/180
    lT=H_fl/2
    nT=round((A+lT)/(lT*2))
    Area=(A*L+2*L*H_fn+2*A*H_fn)-2*nT*(lT**2)
    Volumen_Fon=((A*H_fn)-(nT*(lT**2)))*L
    Volumen_Total=Volumen_Fon+(L*H_fl*(A+H_fl/math.tan(Ang)))
    """Otros parámetros"""
    Porcentaje_Llenado=Volumen_Fon/Volumen_Total
    Area_TCC=(h_Aletas*L*N_Aletas*2)+Area
    return Volumen_Total
    
def Acanalada_Cuadrada(H_fl,H_fn,A,L,B_Aletas):
    #la altura de las aletas es fijo por ahora 10cm
    #lC es la medida de un lado de un canal cuadrado y las aletas van el
    #ducto del canal
    lC=H_fn/3
    N_Aletas_Canal=Cantidad_Aletas(lC,B_Aletas)
    h_Aletas=0.01
    Ang=68*math.pi/180
    N_Canales=round((A+lC)/(lC*2))
    Area=(A*L+2*L*H_fn+2*A*H_fn)-2*(N_Canales-1)*(lC**2)
    Volumen_Fon=((A*(H_fn-lC))+N_Canales*(lC**2))*L
    Volumen_Total=Volumen_Fon+(L*H_fl*(A+H_fl/math.tan(Ang)))
    """Otros parámetros"""
    Porcentaje_Llenado=Volumen_Fon/Volumen_Total
    Area_TCC=(h_Aletas*L*N_Aletas_Canal*N_Canales*2)+Area
    return Volumen_Total

#Está función mide el valor de aptitud del individuo (Paila)
def Valor_Aptitud(Vol_objetivo,Tipo_paila,H_fl,H_fn,A,L,H,Hc,Activar_Aletas):
    #Semiesferica(H_fn,A,H_fl)
    #Semicilindrica(H,Hc,A,L,Hfa,B_Aletas)
    #Plana(H_fl,H_fn,A,L,B_Aletas)
    #Pirotubular_Circular(H_fl,H_fn,A,L,B_Aletas)
    #Pirotubular_Cuadrada(H_fl,H_fn,A,L,B_Aletas)
    #Acanalada_Cuadrada(H_fl,H_fn,A,L,lC,B_Aletas)
    f=100.0
    if Tipo_paila==1:
        f=abs(Vol_objetivo-Plana(H_fl,H_fn,A,L,Activar_Aletas))
        f=(f/Vol_objetivo)*100.0
    elif Tipo_paila==2:
        f=abs(Vol_objetivo-Pirotubular_Circular(H_fl,H_fn,A,L,Activar_Aletas))
        f=(f/Vol_objetivo)*100.0
    elif Tipo_paila==3:
        f=abs(Vol_objetivo-Semiesferica(H_fn,A,H_fl))
        f=(f/Vol_objetivo)*100.0
    elif Tipo_paila==4:
        f=abs(Vol_objetivo-Semicilindrica(H,Hc,A,L,H_fl,Activar_Aletas))
        f=(f/Vol_objetivo)*100.0
    elif Tipo_paila==5:
        f=abs(Vol_objetivo-Pirotubular_Cuadrada(H_fl,H_fn,A,L,Activar_Aletas))
        f=(f/Vol_objetivo)*100.0    
    elif Tipo_paila==6:
        f=abs(Vol_objetivo-Acanalada_Cuadrada(H_fl,H_fn,A,L,Activar_Aletas))
        f=(f/Vol_objetivo)*100.0 
    return f

def Dibujar_paila(Vol,i,Tipo_paila,H_fl,H_fn,A,L,H,Hc,Activar_Aletas):
    print("Etapa: "+str(i+1))
    print("Capacidad en m^3/kg esperada: "+str(Vol))
    if Tipo_paila==1:
        print("Capacidad en m^3/kg estimada: "+str(Plana(H_fl,H_fn,A,L,Activar_Aletas)))
        if(Activar_Aletas==True):
            print("Tipo seleccionado: Plana con aletas")
        else:
            print("Tipo seleccionado: Plana sin aletas")
        print("H_fl: "+str(H_fl))
        print("H_fn: "+str(H_fn))
        print("A: "+str(A))
        print("L: "+str(L))
    elif Tipo_paila==2:
        print("Cantidad en Litros estimada: "+str(Pirotubular_Circular(H_fl,H_fn,A,L,Activar_Aletas)))
        if(Activar_Aletas==True):
            print("Tipo seleccionado: Pirotubular circular con aletas")
        else:
            print("Tipo seleccionado: Pirotubular circular sin aletas")
        print("H_fl: "+str(H_fl))
        print("H_fn: "+str(H_fn))
        print("A: "+str(A))
        print("L: "+str(L))
    elif Tipo_paila==3:
        print("Cantidad en Litros estimada: "+str(Semiesferica(H_fn,A,H_fl)))
        print("Tipo seleccionado: Semiesferica")
        print("H_fl: "+str(H_fl))
        print("H_fn: "+str(H_fn))
        print("A: "+str(A))
    elif Tipo_paila==4:
        print("Cantidad en Litros estimada: "+str(Semicilindrica(H,Hc,A,L,H_fl,Activar_Aletas)))
        if(Activar_Aletas==True):
            print("Tipo seleccionado: Semicilindrica con aletas")
        else:
            print("Tipo seleccionado: Semicilindrica sin aletas")
        print("H_fl: "+str(H_fl))
        print("Hc: "+str(Hc))
        print("A: "+str(A))
        print("L: "+str(L)) 
        print("H: "+str(H))
    elif Tipo_paila==5:  
        print("Cantidad en Litros estimada: "+str(Pirotubular_Cuadrada(H_fl,H_fn,A,L,Activar_Aletas)))
        if(Activar_Aletas==True):
            print("Tipo seleccionado: Pirotubular cuadrada con aletas")
        else:
            print("Tipo seleccionado: Pirotubular cuadrada sin aletas")
        print("H_fl: "+str(H_fl))
        print("H_fn: "+str(H_fn))
        print("A: "+str(A))
        print("L: "+str(L))        
    elif Tipo_paila==6:
        print("Cantidad en Litros estimada: "+str(Acanalada_Cuadrada(H_fl,H_fn,A,L,Activar_Aletas)))
        if(Activar_Aletas==True):
            print("Tipo seleccionado: Acanalada cuadrada con aletas")
        else:
            print("Tipo seleccionado: Acanalada cuadrada sin aletas")
        print("H_fl: "+str(H_fl))
        print("H_fn: "+str(H_fn))
        print("A: "+str(A))
        print("L: "+str(L))

def comprobar_individuo(Lim_inf,Lim_sup,valor_actual):
    if(valor_actual>=Lim_sup):
        return Lim_sup
    elif (valor_actual<=Lim_inf):
        return Lim_inf
    else:
        return valor_actual
    
#Dimensiones de la lamina 4*10 pies o 1.21*3.04 metros (Restricción del sistema)
def Mostrar_pailas(Vol_aux, Etapas):
    Tipo_paila=[[],[]]
    Total_pailas=6
    for i in range(Etapas):
        Tipo_paila[0].append(random.randint(1,Total_pailas))
        if(i==0):
            Tipo_paila[1].append(False)
        else:
            Tipo_paila[1].append(random.choice([True,False]))   
    #Algoritmo de optimización (Ascenso a la colina)
    for i in range(Etapas-1,-1,-1):
        f_1=1000
        iteraciones=0
        Volumen=float(Vol_aux[i])
        #Recuerde H_fl o Hfa es lo mismo
        #Asignación de valores iniciales (variables de entrada)
        H_fl = comprobar_individuo(0.05, 1.00, abs(random.uniform(0.05, 1.00)))
        H_fn = comprobar_individuo(0.05, 0.50, abs(random.uniform(0.05, 0.50)))
        A    = comprobar_individuo(0.15, 1.00, abs(random.uniform(0.15, 1.00)))
        L    = comprobar_individuo(0.30, 3.00, abs(random.uniform(0.40, 3.00)))
        H    = comprobar_individuo(0.02, 1.50, abs(random.uniform(0.02, 1.50)))
        Hc   = comprobar_individuo(0.05, 0.50, abs(random.uniform(0.05, 0.50)))
        f=Valor_Aptitud(Volumen,int(Tipo_paila[0][i]),H_fl,H_fn,A,L,H,Hc,bool(Tipo_paila[1][i]))
        #Paso es una variable que aumenta o disminuye el cambio de la variable de entrada
        sigma=0.03
        while ((0.2<f)and(iteraciones<20000)):
            if(f_1<f):
                H_fl = H_fl_1
                H_fn = H_fn_1
                A    = A_1
                L    = L_1
                H    = H_1
                Hc   = Hc_1
                f=Valor_Aptitud(Volumen,int(Tipo_paila[0][i]),H_fl,H_fn,A,L,H,Hc,bool(Tipo_paila[1][i]))     
            H_fl_1 = comprobar_individuo(0.05, 1.00, abs(random.uniform(0.05, 1.00)))
            H_fn_1 = comprobar_individuo(0.05, 0.50, abs(random.uniform(0.05, 0.50)))
            A_1    = comprobar_individuo(0.15, 1.00, abs(random.uniform(0.15, 1.00)))
            L_1    = comprobar_individuo(0.30, 3.00, abs(random.uniform(0.40, 3.00)))
            H_1    = comprobar_individuo(0.02, 1.50, abs(random.uniform(0.02, 1.50)))
            Hc_1   = comprobar_individuo(0.05, 0.50, abs(random.uniform(0.05, 0.50)))
            f_1    = Valor_Aptitud(Volumen,int(Tipo_paila[0][i]),H_fl_1,H_fn_1,A_1,L_1,H_1,Hc_1,bool(Tipo_paila[1][i]))
            iteraciones=iteraciones+1    
        
        Dibujar_paila(Volumen,i,Tipo_paila[0][i],H_fl,H_fn,A,L,H,Hc,Tipo_paila[1][i])
        print("________>>>>>>>>>>>>>____________")
        print(str(iteraciones))
        print(str(f))     