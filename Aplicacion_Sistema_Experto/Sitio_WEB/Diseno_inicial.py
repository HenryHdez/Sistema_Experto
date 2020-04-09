# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 11:38:48 2020

@author: hahernandez
"""
import math

def datos_entrada(Diccionario):
    """Estos datos se toman directamente del archivo HTML"""
    #Area de Caña Sembrada al rededor			
    #Area de Caña Sembrada Propia			
    #Area de Caña Sembrada Para Calculo			
    #Periodo vegetatio			
    #Caña por Hectarea Esperada			
    #CSS de la Caña			
    #Jornada de Trabajo			
    #Dias de Trabajo			
    #Horas al Dia		
    #CSS Panela	
    #Altura del Sitio	
    
    """Ojo es un supuestos (Estas son otras variables de entrada)"""
    Porcentaje_extraccion=0.6 #60%
    Bagazillo_Prelimpiador=0.02 #2%
    Cachaza=0.04 #4%    
    CSS_Jugo_Clarificado=float(Diccionario['Grados Brix de la caña'])+5
    CSS_Jugo_Posevaporacion=float(Diccionario['Grados Brix de la caña'])+58
    Tipo_de_camara='Ward'
    Humedad_bagazo=0.15#15%			
    Exceso_Aire=0.018#1.8%	
    Extraccion=0.6#60%
    Porcentaje_Fibra=0.14#14%
    Temperatura_Ambiente=25#°C			
    Altura_sitio=float(Diccionario['Altura media sobre el nivel del mar'].replace(" m", ""))
    """Fin de los datos supuestos entrada"""
    
    """Calculo de la capacidad del molino"""		
    #Área de caña sembrada para el calculo
    Area_cana_calculo=(float(Diccionario['Área caña sembrada alrededor'])+float(Diccionario['Área caña sembrada propia']))/2
    Cana_esperada_hectarea=float(Diccionario['Caña esperada por hectárea'])
    P_vegetativo=float(Diccionario['Periodo vegetativo'])
    #Caña molida al mes = Area sembrada de caña para calculo*Caña esperada por hectarea/Periodo vegetativo
    Cana_molida_mes=(Area_cana_calculo*Cana_esperada_hectarea)/P_vegetativo
    # Area cosechada al mes = Caña esperada por hectarea/Caña molida al mes
    Area_Cosechada_mes=Cana_molida_mes/Cana_esperada_hectarea
    #Caña molida a la semana = Caña molida al mes/numero de moliendas
    Cana_molida_semana=Cana_molida_mes/float(Diccionario['Número de moliendas'])
    #Caña molida por hora = Caña molida a la semana/Dias de trabajo*Horas al dia
    Cana_molida_hora=Cana_molida_semana/(float(Diccionario['Días de trabajo a la semana'])*float(Diccionario['Horas de trabajo al día']))
    #Jugo Crudo=Caña molida por hora*porcentaje de extraccion
    Jugo_Crudo=Cana_molida_hora*Porcentaje_extraccion
    #Jugo Clarificado=Jugo_Crudo-((Jugo_Crudo*Bagazillo en Prelimpiador+((Jugo_Crudo-(Jugo_Crudo*Bagazillo en Prelimpiador))*(Cachaza))
    Jugo_Clarificado=Jugo_Crudo-((Jugo_Crudo*Bagazillo_Prelimpiador+((Jugo_Crudo-(Jugo_Crudo*Bagazillo_Prelimpiador))*(Cachaza))))
    #Masa de panela=((Jugo_Clarificado*CSS de la caña))/CCS de la panela)*1000
    CSS_Cana=float(Diccionario['Grados Brix de la caña'])
    CSS_Panela=float(Diccionario['Grados Brix de la panela'])
    Masa_panela = (Jugo_Clarificado*CSS_Cana/CSS_Panela)*1000
    #Capacidad del molino=constante*caña molida hora*1000
    Capacidad_molino=Cana_molida_hora*1.3*1000
    #Capacidad de la hornilla=Masa de panela
    Capacidad_Hornilla=Masa_panela
    
    #print(Cana_molida_mes)
    #print(Cana_esperada_hectarea)
    #print(Area_Cosechada_mes)
    #print(Cana_molida_semana)
    #print(Cana_molida_hora)
    #print(Jugo_Crudo)
    #print(Jugo_Clarificado)
    #print(Masa_panela)
    #print(Capacidad_molino)
    
    """Calculos para la masa"""
    Masa_Jugo_Clarificado=(CSS_Panela*Capacidad_Hornilla)/CSS_Cana
    Masa_Jugo_Prelimpiador=Masa_Jugo_Clarificado/(1-Cachaza)
    Masa_Cachaza=Masa_Jugo_Prelimpiador*Cachaza
    Masa_Jugo=Masa_Jugo_Prelimpiador/(1-Bagazillo_Prelimpiador)
    Masa_Bagazillo= Masa_Jugo*Bagazillo_Prelimpiador 
    Masa_Cana=Masa_Jugo/Extraccion
    
    Masa_Agua_Evaporar=Masa_Jugo_Prelimpiador-Capacidad_Hornilla
    Masa_A_clarificacion=Masa_Jugo_Prelimpiador
    Masa_A_Evaporacion=Masa_Jugo_Clarificado
    Masa_A_Concentracion=(CSS_Jugo_Clarificado*Masa_A_Evaporacion)/CSS_Jugo_Posevaporacion
    Masa_Bag_Humedo=Masa_Cana-Masa_Jugo
    Humedad_inicial_bagazo=((Masa_Jugo-Masa_Jugo*(Extraccion+Porcentaje_Fibra))-(Masa_Jugo-Masa_Jugo*(Extraccion+Porcentaje_Fibra))*(CSS_Cana/100))/(Masa_Jugo*(1-Extraccion))			
    Masa_Bag_Seco=Masa_Bag_Humedo*((1-Humedad_inicial_bagazo)/(1-Humedad_bagazo))
    Factor_consumo_bagazo=Masa_Bag_Seco/Capacidad_Hornilla
    Masa_Bag_Suministrado=Capacidad_Hornilla*Factor_consumo_bagazo
    Presion_atmosferica=760.0*math.exp(-0.0001158*Altura_sitio)
    Temperatura_Ebullicion_Agua=-227.03 + (3816.44/(18.3036 - math.log(7.5*(Presion_atmosferica*(133.3224/1000)))))
    
    """Calculos de las propiedades de los jugos"""
    T33=25 #NOTA: Esta es una caracteristica propia del molino (Tomarla del catálogo).
    Inicial_Clf=997.39+(4.46*CSS_Cana)   
    Inicial_Eva=997.39+(4.46*CSS_Jugo_Clarificado)
    Inicial_Con=997.39+(4.46*CSS_Jugo_Posevaporacion)
    Ebullicion_Clarificacion=Temperatura_Ebullicion_Agua + 0.2209*math.exp(0.0557*CSS_Jugo_Clarificado)	
    Ebullicion_Evaporacion=Temperatura_Ebullicion_Agua + 0.2209*math.exp(0.0557*CSS_Jugo_Posevaporacion)
    Ebullicion_Concentracion=Temperatura_Ebullicion_Agua + 0.2209*math.exp(0.0557*T33)	
    Entalpia_Clarificacion=2492.9-2.0523*((Temperatura_Ebullicion_Agua+Ebullicion_Clarificacion)/2)-0.0030752*((Temperatura_Ebullicion_Agua+Ebullicion_Clarificacion)/2)**2
    Entalpia_Evaporacion=2492.9-2.0523*((Ebullicion_Clarificacion+Ebullicion_Evaporacion)/2)-0.0030752*((Ebullicion_Clarificacion+Ebullicion_Evaporacion)/2)**2
    Entalpia_Concentracion=2492.9-2.0523*((Ebullicion_Evaporacion+Ebullicion_Concentracion)/2)-0.0030752*((Ebullicion_Evaporacion+Ebullicion_Concentracion)/2)**2
    Q_Especifico_Inicial=4.18*(1-0.006*CSS_Cana)
    Q_Especifico_Clarificado=4.18*(1-0.006*CSS_Jugo_Clarificado)	
    Q_Especifico_Eva=4.18*(1-0.006*CSS_Jugo_Posevaporacion)	
    Poder_Calorifico_bagazo=17.85-20.35*Humedad_bagazo
    Calor_Suministrado=(Capacidad_Hornilla*Factor_consumo_bagazo)*Poder_Calorifico_bagazo/3.6	
    Area_de_Parrilla=Calor_Suministrado/1000	    
    
    """Ampliación del diccionario"""
    Etiquetas=['DATOS DE ENTRADA',
               'Capacidad Estimada de la hornilla',			
               'Factor Consumo Bagazo',						
               'Bagazillo en Prelimpiador	',		
               'Cachaza',			
               'CSS del jugo de Caña',			
               'CSS del jugo clarificado',			
               'CSS del jugo posevaporación',		
               'CSS panela',			
               'Tipo de camara',			
               'Humedad del bagazo	',		
               'Exceso de Aire',			
               'Extraccion',			
               'Porcentaje de Fibra',			
               'Altura del Sitio',			
               'Temperatura Ambiente',			
               'Humedad inicial bagazo',			
               'Presion Atmosferica',			
               'Temperatura Ebullición Agua',
               'CAPACIDAD MOLINO',
               'Caña molida al mes	',	
               'Area Cosechada al mes',		
               'Caña molida a la semana',		
               'Caña Molida por Hora',		
               'Jugo Crudo',		
               'Jugo Clarificado',		
               'Masa de panela',		
               'Capacidad del Molino',		
               'DATOS DE LA MASA',
               'Caña',
               'Jugo',
               'Bagazillo',	
               'Jugo pre limpiador',	
               'Cachaza',	
               'Jugo clarificado',	
               'Agua a evaporar',	
               'A clarificación',	
               'A evaporación',
               'A concentración',	
               'Bag. suministrado',	
               'Bag. humedo',	
               'Bag. seco',	
               'PROPIEDADES DE LOS JUGOS',
               'Densidad',
               'Inicial P. Clf',
               'Inicial P. Eva',
               'Inicial P. Con',
               'Temperatura Ebullición (Clarificación)',
               'Temperatura Ebullición (Evaporación)',
               'Temperatura Ebullición (Concentración)',
               'Entalpia de Evaporización (Clarificación)',
               'Entalpia de Evaporización (Evaporación)',
               'Entalpia de Evaporización (Concentración)',
               'Calor especifico jugo',			
               'Inicial',
               'Clarificado',
               'Eva',
               'Otros datos',
               'Poder Calorifico Vagazo',
               'Calor Suministrado',
               'Area de Parrilla'               
               ]
    
    Valores=['DATOS DE ENTRADA',
             Capacidad_Hornilla,
             Factor_consumo_bagazo,
             Bagazillo_Prelimpiador,
             Cachaza,
             CSS_Cana,
             CSS_Jugo_Clarificado,
             CSS_Jugo_Posevaporacion,
             CSS_Panela,
             Tipo_de_camara,
             Humedad_bagazo,
             Exceso_Aire,
             Extraccion,
             Porcentaje_Fibra,
             Diccionario['Altura media sobre el nivel del mar'],
             Temperatura_Ambiente,
             Humedad_inicial_bagazo,
             Presion_atmosferica,
             Temperatura_Ebullicion_Agua,
             'CAPACIDAD MOLINO',
             Cana_molida_mes,
             Area_Cosechada_mes,
             Cana_molida_semana,
             Cana_molida_hora,
             Jugo_Crudo,
             Jugo_Clarificado,
             Masa_panela,
             Capacidad_molino,
             'DATOS DE LA MASA',
             Masa_Cana,
             Masa_Jugo,
             Masa_Bagazillo,
             Masa_Jugo_Prelimpiador,
             Masa_Cachaza,
             Masa_Jugo_Clarificado,
             Masa_Agua_Evaporar,
             Masa_A_clarificacion,
             Masa_A_Evaporacion,
             Masa_A_Concentracion,
             Masa_Bag_Suministrado,
             Masa_Bag_Humedo,
             Masa_Bag_Seco,
             'PROPIEDADES DE LOS JUGOS',
             'Densidad',
             Inicial_Clf,
             Inicial_Eva,
             Inicial_Con,
             Ebullicion_Clarificacion,
             Ebullicion_Evaporacion,
             Ebullicion_Concentracion,
             Entalpia_Clarificacion,
             Entalpia_Evaporacion,
             Entalpia_Concentracion,
             'Calor especifico jugo',
             Q_Especifico_Inicial,
             Q_Especifico_Clarificado,
             Q_Especifico_Eva,
             'Otros datos',
             Poder_Calorifico_bagazo,
             Calor_Suministrado,
             Area_de_Parrilla
            ]
    
    Dict_aux=dict(zip(Etiquetas,Valores))
    Diccionario.update(Dict_aux)
    return Diccionario