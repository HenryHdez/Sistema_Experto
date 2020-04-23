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
global Capacidad_hornilla
global Molino_seleccionado
global Horas_trabajo_al_dia

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
    #>>>>>>>>>>>>>>>>>>>>>>>>>total gastos de la hornilla
    total_hornilla=estimar_total(Valor_Hornilla)   
    
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
    
    """>>>>>>>>>>>>----------Costos operativos-------------<<<<<<<<<<<<"""
    #Construcción
    Operativos=pd.read_excel('static/Costos/Operativos.xlsx')
    Valor_Operativo=[]
    c=float(Operativos['Ingeniero'].values)
    Valor_Operativo.append([2, b, b*2])
    c=float(Operativos['Maestro de obra'].values)
    Valor_Operativo.append([2, b, b*2])
    c=float(Operativos['Obrero'].values)	
    Cantidad=math.ceil(Total_pailas/4)
    Valor_Operativo.append([2, Cantidad, Cantidad*2])
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>Total gastos operativos
    total_operativos=estimar_total(Valor_Operativo)
    """>>>>>>>>>>>>>>-------------TOTALES PROYECTO--------------<<<<<<<<<<<<<<<"""
    Costo_imprevistos=0.02*total_hornilla
    Consolidado_totales_1=[total_hornilla, total_recuperador, total_operativos, Costo_imprevistos, float(Operativos['Movilidad'])]
    Total_proyecto=sum(Consolidado_totales_1)
    """>>>>-----------------COSTOS DE LA PRODUCCIÓN-------------------------<<<"""
    #Variables
    Valor_Cana=float(Operativos['Tonelada de Caña'].values)	
    Galon_diesel=float(Operativos['Galon diesel'].values)		
    P_KWh=float(Operativos['Precio kWh'].values)	
    Mtto=float(Operativos['Mantenimiento'].values)
    Valor_operario=float(Operativos['Operarios'].values)
    Precio_otros_dia=float(Operativos['Valor otros'].values)
    Produ_diaria=Horas_trabajo_al_dia*Capacidad_hornilla
    #>>>>>>>>>>>>>>>>>>>>>Molinos<<<<<<<<<<<<<<<<<<
    Molino=pd.read_excel('static/Temp/Temp.xlsx',skipcolumn = 0,)
    Marca=Molino['Marca'].values
    Modelo=Molino['Modelo'].values
    Kilos=Molino['kg/hora'].values
    Diesel=Molino['Diesel'].values
    Electrico=Molino['Electrico'].values
    Gas=Molino['Gasolina'].values
    Relacion=Molino['Relación i'].values
    Valor=Molino['Precio'].values    
    #Calculos del molino con motores eléctricos     
    Potencia_e=Electrico[0]
    Eficiencia=0.875		
    PA=((Potencia_e*0.75)/Eficiencia)
    Consumo=PA*Horas_trabajo_al_dia
    Precio_KWh=P_KWh
    Consumo_Motor=Precio_KWh*Consumo
    Costo_kg_Motor=math.ceil(Consumo_Motor/Produ_diaria)
    #Calculos del molino con motores eléctricos de combustion Diesel		
    Potencia_d=Diesel[0]
    Consumo=2
    Precio_Galon_Diesel=Galon_diesel
    Consumo_Diesel =	Precio_Galon_Diesel*Horas_trabajo_al_dia*Consumo 
    Costo_kg_Diesel=math.ceil(Consumo_Diesel/Produ_diaria)
    #Potencia disipada por el controlador y la bomba del evaporador   
    Activaciones=Horas_trabajo_al_dia*0.1
    Watts=3000 #Consumo aproximado de la bomba y el controlador
    Consumo=Watts*Activaciones
    Precio_KWh=P_KWh
    Consumo_Controlador=Precio_KWh*Consumo
    Total_Control=math.ceil(Consumo_Controlador/Produ_diaria)
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
    """>>>>>>>>>>>>>>>>>>>>----------------COSTO FINANCIERO---------------------<<<<<<<<<"""
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
    Depreciacion_anual=(Valor_Inicial-Valor_Salvamento)/Vida_util_anos_horn
    Depreciacion=[]
    Depreciacion.append(round(Valor_Inicial,3))
    for ano in range(1,Vida_util_anos_horn):
        Depreciacion.append(round(Depreciacion[ano-1]-Depreciacion_anual,3))
    ###########>>>>>>>>>>>>>>>>>>>>>>Graficar Depreciación<<<<<<<<<<<<<<<<<<<<<################
    Fig = plt.Figure()
    Fig_1 = Fig.add_subplot(111)
    Fig_1.plot(range(len(Depreciacion)),np.array(Depreciacion)/1000000)
    Fig_1.grid(color='k', linestyle='--', linewidth=1)
    Fig_1.set_ylabel('Depreciación en pesos (X1000000)')
    Fig_1.set_xlabel('Años')
    Fig.savefig("static/Graficas/Depreciacion.jpg")
    ############################################################################################
    
    """>>>>>>>>>>>>>>>>>>>>--------------------FLUJO DE CAJA---------------<<<<<<<<<<<<<<<<<"""
    #Depreciación Anual, Mtto, Ingresos, Flujo de caja
    Estado_caja=[0, 0, 0, -(Total_proyecto+Costo_financiero)+Valor_Salvamento]
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
    ###########>>>>>>>>>>>>>>>>>>>>>>Graficar flujo de caja<<<<<<<<<<<<<<<<<<<<<################
    Fig = plt.Figure()
    Fig_2 = Fig.add_subplot(111)
    Fig_2.barh(range(len(flujo_caja)),np.array(flujo_caja)/1000000)
    Fig_2.grid(color='k', linestyle='--', linewidth=1)
    Fig_2.set_ylabel('Años')
    Fig_2.set_xlabel('Flujo de caja en pesos (X1000000)')
    Fig.savefig("static/Graficas/Flujo_Caja.jpg")
    ############################################################################################
#    print(Depreciacion_anual)
#    print(Produccion_anual_kg)
#    print(Costo_total_kg)
#    print(Produccion_anual_kg*Costo_total_kg)
#    print(flujo_caja)
    #Valor presente neto
    Tasa_Interes=float(Operativos['Tasa interes'].values)
    NPV=npf.npv(rate=Tasa_Interes,values=flujo_caja)
    TIR=round(npf.irr(flujo_caja), 3)
    """>>>>>>------RETORNO A LA INVERSION----<<<<"""
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
        Valor_panela=Valor_panela+random.uniform(-500, 500)
        Retorno_inversion.append(Estado_retorno)
    MA=np.array(Retorno_inversion)
    lista_valor_panela=MA[:,0]
    Anos=MA[:,5]
    Meses=MA[:,6]
    #print(Anos)
    ###########>>>>>>>>>>>>>>>>>Graficar Retorno a la inversión<<<<<<<<<<<<<<<<<################
    Fig = plt.Figure()
    Fig_3 = Fig.add_subplot(111)
    Fig_3.plot(lista_valor_panela,Anos)
    Fig_3.grid(color='k', linestyle='--', linewidth=1)
    Fig_3.set_ylabel('Años')
    Fig_3.set_xlabel('Valor de la panela en pesos')
    Fig.savefig("static/Graficas/RI_Anos.jpg")
    ############################################################################################
    ###########>>>>>>>>>>>>>>>>>Graficar Retorno a la inversión<<<<<<<<<<<<<<<<<################
    Fig = plt.Figure()
    Fig_4 = Fig.add_subplot(111)
    Fig_4.plot(lista_valor_panela,Meses)
    Fig_4.grid(color='k', linestyle='--', linewidth=1)
    Fig_4.set_ylabel('Meses')
    Fig_4.set_xlabel('Valor de la panela en pesos')
    Fig.savefig("static/Graficas/RI_Meses.jpg")
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