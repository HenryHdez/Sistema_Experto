# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 08:53:50 2020

@author: hahernandez
"""
import math
import random
import time
import os
import pandas as pd
from difflib import SequenceMatcher as SM
global Cantidad_pailas
global Lista_de_pailas
#Cantidad_pailas[0] es plana
#Cantidad_pailas[1] es plana sin aletas
#Cantidad_pailas[2] es pirotubular circular
#Cantidad_pailas[3] es pirotubular circular SA
#Cantidad_pailas[4] es semiesférica
#Cantidad_pailas[5] es semicilindrica
#Cantidad_pailas[6] es semicilindrica SA
#Cantidad_pailas[7] es cuadrada
#Cantidad_pailas[8] es cuadrada SA
#Cantidad_pailas[9] es acanalada
#Cantidad_pailas[10] es acanalada SA
Cantidad_pailas=[0,0,0,0,0,0,0,0,0,0,0]
Lista_de_pailas=[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']
"Librería para realizar los calculos de la geometría de las pailas de una hornilla"

"""--->>>Generar informe en pdf<<<<---"""
#Función para unir el informe generado en varias funciones
def Unir_Informe(nombre, ruta_carp, borrar_F):
    from PyPDF2 import PdfFileMerger, PdfFileReader
    from shutil import rmtree
    listaPdfs = os.listdir(ruta_carp)
    listaPdfs
    merger = PdfFileMerger()
    for file in listaPdfs:
        merger.append(PdfFileReader(ruta_carp+file))
    merger.write('static/'+nombre+'.pdf')
    """Borrar datos cargados temporalmente"""
    if(borrar_F==1):
        rmtree('static/Temp')
        rmtree('static/pdf01')
        rmtree('static/pdf02')
        os.mkdir('static/Temp')
        os.mkdir('static/pdf01')
        os.mkdir('static/pdf02')

#Layout del informe
def Fondo(canvas):
    #Dibujar logo y membrete de AGROSAVIA
    canvas.drawImage('static/Iconos/Agrosavia.jpg', 420, 720, width=150, height=40)
    canvas.drawImage('static/Iconos/Membrete.png' , 0, 0, width=650, height=240)
    canvas.drawImage('static/Iconos/Membrete2.png', 0, 650, width=150, height=150)   
    canvas.setLineWidth(.3)
    canvas.setFont('Helvetica-Bold', 20)
    tiempo = time.asctime(time.localtime(time.time()))
    canvas.setFont('Helvetica-Bold', 7)
    canvas.drawString(520,5,str(tiempo))
    #canvas.drawString(10,5,"Hoja: "+str(Hoja))
    return canvas

#Función para generar las portadas
def Generar_portada():
    #Espacio de trabajo disponible desde 20 hasta 650
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    #Portada
    canvas = canvas.Canvas("static/pdf01/A1_portada.pdf", pagesize=letter)
    Fondo(canvas)
    canvas.drawImage('static/Iconos/Fondo_portada.png', 80, 150, width=500, height=350)
    canvas.setFont('Helvetica-Bold', 30)
    canvas.drawString(20,550,'           PARÁMETROS DE DISEÑO     ') 
    canvas.drawString(20,515,'      Y ESQUEMAS MECÁNICOS PARA   ') 
    canvas.drawString(20,480,'LA CONSTRUCCIÓN DE UNA HORNILLA  ') 
    canvas.drawString(20,445,'   PARA LA PRODUCCIÓN DE PANELA  ')
    canvas.setFont('Helvetica', 24)
    canvas.drawString(220,280,' Presentado por:')
    canvas.drawString(220,255,'   AGROSAVIA') 
    canvas.setFont('Helvetica', 10)
    canvas.drawString(170,240,'(Corporación Colombiana de Investigación Agropecuaria)')
    canvas.save()
    #Sección 1
    from reportlab.pdfgen import canvas
    canvas = canvas.Canvas("static/pdf01/A2_portada.pdf", pagesize=letter)
    Fondo(canvas)
    canvas.drawImage('static/Iconos/Fondo_otros.png', 50, 220, width=500, height=350)
    canvas.setFont('Helvetica-Bold', 30)
    canvas.drawString(20,450,'                         SECCIÓN 1:     ') 
    canvas.drawString(20,415,'              DATOS DEL USUARIO E   ') 
    canvas.drawString(20,380,'          INFORMACIÓN FINANCIERA  ') 
    canvas.showPage() #Salto de página    
    canvas.save()
    #Sección 2
    from reportlab.pdfgen import canvas
    canvas = canvas.Canvas("static/pdf01/B0_portada.pdf", pagesize=letter)
    Fondo(canvas)
    canvas.drawImage('static/Iconos/Fondo_otros.png', 50, 220, width=500, height=350)
    canvas.setFont('Helvetica-Bold', 30)
    canvas.drawString(20,390,'                         SECCIÓN 2:     ') 
    canvas.drawString(20,355,'                PLANOS MECÁNICOS   ') 
    canvas.showPage() #Salto de página    
    canvas.save()
    #Sección 3
    from reportlab.pdfgen import canvas
    canvas = canvas.Canvas("static/pdf02/C0_portada.pdf", pagesize=letter)
    Fondo(canvas)
    canvas.drawImage('static/Iconos/Fondo_otros.png', 50, 220, width=500, height=350)
    canvas.setFont('Helvetica-Bold', 30)
    canvas.drawString(20,390,'                         SECCIÓN 1:     ') 
    canvas.drawString(20,355,'  INFORMACIÓN TÉCNICA DETALLADA   ') 
    canvas.showPage() #Salto de página    
    canvas.save()

def Dibujar_Molino(canvas, puntero):
    import pandas as pd
    #Estructura para publicar el molino seleccionado
    canvas.setFont('Helvetica-Bold', 14)
    canvas.drawString(200,puntero,'   ')
    canvas.drawString(200,puntero-20,'   ')
    canvas.drawString(190,puntero-20,'>>>MOLINOS DISPONIBLES<<<')
    Molino=pd.read_excel('static/Temp/Temp.xlsx',skipcolumn = 0,)
    
    Marca=Molino['Marca'].values
    Modelo=Molino['Modelo'].values
    Kilos=Molino['kg/hora'].values
    Diesel=Molino['Diesel'].values
    Electrico=Molino['Electrico'].values
    Valor=Molino['Precio'].values
    canvas.setFillColorRGB(1,0,0)
    canvas.setFont('Helvetica-Bold', 11)
    canvas.drawString(50,puntero-50,'VALOR APROXIMADO DE UN MOLINO: ')
    canvas.drawString(270,puntero-50,"$"+str(math.ceil(sum(Valor)/len(Valor))))
    canvas.setFillColorRGB(0,0,0)
    canvas.drawString(340,puntero-80,'POTENCIA DEL MOTOR')
    canvas.drawString(70,puntero-100,'MARCA')
    canvas.drawString(149,puntero-100,'MODELO')
    canvas.drawString(220,puntero-100,'KG/HORA')
    canvas.drawString(290,puntero-100,'DIESEL O GASOLINA [HP]')
    canvas.drawString(440,puntero-100,'ELÉCTRICO [HP]')
    canvas.setFont('Helvetica', 11)
    OF=115
    for i in range(len(Marca)):
        canvas.drawString(60,puntero-OF, str(Marca[i]))
        canvas.drawString(141,puntero-OF, str(Modelo[i]))
        canvas.drawString(230,puntero-OF, str(Kilos[i]))
        canvas.drawString(350,puntero-OF, str(Diesel[i]))
        canvas.drawString(470,puntero-OF, str(Electrico[i])) 
        OF=OF+15
    OF=(puntero-OF)-240
    for i in range(len(Modelo)):
        if((OF<200)or(i==0)):
            canvas.setFont('Helvetica-Bold', 11)
            canvas.drawString(300,OF+230,str(Modelo[i]))    
            canvas.drawImage('static/Molinos/'+str(Modelo[i]+'.jpg'), 150, OF, width=320, height=220)
            canvas.showPage() #Salto de página
            Fondo(canvas)
            OF=450
        else:
            canvas.setFont('Helvetica-Bold', 11)
            canvas.drawString(300,OF+230,str(Modelo[i]))    
            canvas.drawImage('static/Molinos/'+str(Modelo[i]+'.jpg'), 150, OF, width=320, height=220)  
            OF=OF-(320)
    return canvas   
    
#Función para presentar las variedades de caña en el pdf
def Dibujar_Canas(canvas, puntero):
    import pandas as pd
    #Estructura para publicar el molino seleccionado
    canvas.setFont('Helvetica-Bold', 14)
    canvas.drawString(200,puntero,'   ')
    canvas.drawString(200,puntero-20,'   ')
    canvas.drawString(50,puntero-20,'>>>CARACTERISTICAS DE LAS VARIEDADES DE CAÑA SEMBRADAS<<<')
    Canas=pd.read_excel('static/Temp/Temp4.xlsx',skipcolumn = 0,)
    Carpe=pd.read_excel('static/Temp/Temp5.xlsx',skipcolumn = 0,)
    Eti = Canas.iloc[0].values
    Val = Canas.iloc[1].values
    Car = Carpe.iloc[0].values
    puntero=600
    for i in range (1,len(Eti)):
        canvas.setFont('Helvetica-Bold', 12)
        canvas.drawString(80,puntero,str(Eti[i])) 
        canvas.setFont('Helvetica', 12)
        canvas.drawString(360,puntero,str(Val[i]))
        if(puntero<=110):
            canvas.showPage()
            Fondo(canvas)
            puntero=650            
        else:          
            puntero=puntero-20
            
    canvas.showPage()
    Fondo(canvas)            
    canvas.setFont('Helvetica-Bold', 12)
    puntero=650
    canvas.drawString(50,puntero,'Vista previa de la(s) variedad(es) de caña seleccionada(s)')
    puntero=600
    for i in range (1,len(Car),3):
        if(i<11):
            canvas.drawString(75,puntero+5,'Variedad de caña '+str(i))
            canvas.drawImage('static/'+Car[i], 55, puntero-150, width=150, height=150)
        if(((i+1)<len(Car)-1)and(i+1<11)):
            canvas.drawString(245,puntero+5,'Variedad de caña '+str(i+1))
            canvas.drawImage('static/'+Car[i+1], 225, puntero-150, width=150, height=150)
        if(((i+2)<=len(Car)-1)and(i+1<11)):
            canvas.drawString(415,puntero+5,'Variedad de caña '+str(i+2))
            canvas.drawImage('static/'+Car[i+2], 395, puntero-150, width=150, height=150)
        if((puntero<=200)and(i>6)):
            canvas.showPage()
            Fondo(canvas)
            canvas.setFont('Helvetica-Bold', 12)
            puntero=600            
        else:          
            puntero=puntero-200
    return canvas
    
#Función para generar la parte escrita del informe
def Generar_reporte(D1,D2):
    #Genera la vista previa
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    canvas = canvas.Canvas("static/pdf01/A3_informe.pdf", pagesize=letter)
    #Espacio de trabajo disponible desde 20 hasta 650
    puntero=630
    Fondo(canvas)
    for i in D1:
        if(str(i)=='DATOS DE ENTRADA' or str(i)=='CAPACIDAD MOLINO' or 
           str(i)=='DATOS DE LA MASA' or str(i)=='PROPIEDADES DE LOS JUGOS'):
            if(str(i)=='DATOS DE ENTRADA'):
                canvas.setFont('Helvetica-Bold', 14)
                canvas.drawString(200,650,'--->>>DATOS DEL USUARIO<<<---')
                canvas.setFont('Helvetica-Bold', 12)
                canvas.showPage() #Salto de página
                #Cortar pdf
                canvas.save()
                from reportlab.pdfgen import canvas
                canvas = canvas.Canvas("static/pdf02/C1_informe.pdf", pagesize=letter)
                #-----
                Fondo(canvas)
                puntero=650
                canvas.setFont('Helvetica-Bold', 14)
                canvas.drawString(90,puntero,'--->>>DATOS USADOS PARA EL CÁLCULO DE LA HORNILLA<<<---')
            elif(str(i)=='CAPACIDAD MOLINO'):
                canvas.showPage() #Salto de página
                #Cortar pdf
                canvas.save()
                from reportlab.pdfgen import canvas
                canvas = canvas.Canvas("static/pdf01/A5_informe.pdf", pagesize=letter)
                #-----
                Fondo(canvas)
                puntero=650
                canvas.setFont('Helvetica-Bold', 14)
                canvas.drawString(180,puntero,'--->>>MOLINO PRE-SELECCIONADO<<<---')                
            elif(str(i)=='DATOS DE LA MASA'):
                canvas=Dibujar_Molino(canvas, puntero)
                #Cortar pdf                
                canvas.save()

                from reportlab.pdfgen import canvas
                canvas = canvas.Canvas("static/pdf01/A4_informe.pdf", pagesize=letter)
                #-----
                Fondo(canvas)
                puntero=650
                canvas.setFont('Helvetica-Bold', 14)
                #Variedades de caña sembradas
                Dibujar_Canas(canvas, puntero)
                
                ##Sección C
                canvas.save()
                from reportlab.pdfgen import canvas
                canvas = canvas.Canvas("static/pdf02/C2_informe.pdf", pagesize=letter)
                #-----
                Fondo(canvas)
                puntero=650
                canvas.setFont('Helvetica-Bold', 12)
                canvas.drawString(200,puntero,'--->>>PROPIEDADES DE LA MASA<<<---')
            else:
                canvas.setFont('Helvetica-Bold', 12)
                canvas.drawString(200,puntero,'--->>>PROPIEDADES DE LOS JUGOS<<<---')                
        else:
        #rutina para filtrar string a publicar
            if(SM(None, 'Variedad de Caña', i).ratio()<0.85):
                canvas.setFont('Helvetica-Bold', 12)
                canvas.drawString(50,puntero,str(i))
                canvas.setFont('Helvetica', 12)
                canvas.drawString(350,puntero,str(D1[i]))   
            else:
                puntero=puntero+20
        if(puntero<=110):
            canvas.showPage()
            Fondo(canvas)
            puntero=650            
        else:          
            puntero=puntero-20
    
    """----------->>>>>>> Publicar Calculos por etapa<<<<<<<<<<<------------"""
    #Estructura para imprimir los calculos por Etapa
    canvas.showPage()
    Fondo(canvas)
    puntero_v=450
    canvas.setFont('Helvetica-Bold', 12)
    canvas.drawString(200,700,'--->>>PARÁMETROS DE DISEÑO<<<---')  
    Etiquetas=list(dict.keys(D2))
    Etiquetas.insert(0,'Orden de las pailas según el flujo del gas')
    for i in range(len(Etiquetas)-1):
        canvas.saveState()
        canvas.translate(puntero_v, 680)
        canvas.rotate(-90)
        canvas.setFont('Helvetica-Bold', 12)
        canvas.drawString(0, 0, str(Etiquetas[i]))
        puntero_v=puntero_v-25
        canvas.restoreState()     
    #Función para dibujar los valores de la Tabla    
    Valores=list(dict.values(D2))
    puntero_h=400
    for i in range(int(D2['Etapas'])): #Etapas
        puntero_v=450
        canvas.saveState()
        canvas.translate(puntero_v, puntero_h)
        canvas.rotate(-90)
        canvas.setFont('Helvetica-Bold', 12)
        canvas.drawString(0, 0, str(int(D2['Etapas'])-i)) #orden segun el flujo
        puntero_v=puntero_v-25
        canvas.restoreState()
        for j in range(13):#Literales de la tabla
            canvas.saveState()
            canvas.translate(puntero_v, puntero_h)
            canvas.rotate(-90)
            canvas.drawString(0, 0, str(Valores[j][i]))
            puntero_v=puntero_v-25
            canvas.restoreState()
        if(puntero_h<200):
            puntero_h=700
            canvas.showPage()
            Fondo(canvas)
            canvas.setFont('Helvetica-Bold', 12)
        else:
            puntero_h=puntero_h-80
    #Gruardas informe en pdf
    Generar_portada()
    canvas.save()
    Unir_Informe('Informe', 'static/pdf01/', 0)
    Unir_Informe('Calculos', 'static/pdf02/', 1)

def Dibujar_planta():
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    canvas = canvas.Canvas("static/B2_Planos_planta.pdf", pagesize=letter)
    canvas.drawImage('static/Planta/Camara.png', 0, 0, width=610, height=790)
    canvas.showPage()
    canvas.drawImage('static/Planta/Chimenea.png', 0, 0, width=610, height=790)
    canvas.showPage()
    canvas.drawImage('static/Planta/Ducto.png', 0, 0, width=610, height=790)
    canvas.showPage()
    canvas.drawImage('static/Planta/Planta.png', 0, 0, width=610, height=790)
    canvas.save()
    
#Funcion para dibujar planos acotados
def Crear_plano_pdf(directorio_imagen, Nombre_archivo, Nombre_Usuario, Nombre_Paila, Valores_plano, valores_eliminar):
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    Etiquetas=['Altura de la falca','Altura del fondo','Ancho', 'Ancho del fondo', 'Longitud',
               'Longitud del fondo', 'Angulo', 'Altura aletas', 'Separación entre aletas', 
               'Número de aletas', 'Alto del casco', 'Ancho del casco',
               'Cantidad de tubos', 'Diametro del tubo', 'Diametro del tubo',
               'Grosor del canal', 'Cantidad de canales']
    Conv=['A','B','C','D','E','G','I','F','H','J','K','L','M','N','O','P','Q']
    for i in range(len(valores_eliminar)-1,-1,-1):
        Valores_plano.pop(valores_eliminar[i])
        Etiquetas.pop(valores_eliminar[i])
        Conv.pop(valores_eliminar[i])
    canvas = canvas.Canvas(Nombre_archivo+".pdf", pagesize=letter)
    canvas.drawImage(directorio_imagen, 0, 0, width=610, height=790)
    canvas.setLineWidth(0.5)
    canvas.line(55,134,300,134)
    for i in range(len(Etiquetas)):
        Puntero=126-(i*9)
        canvas.setFont('Helvetica-Bold', 9)
        canvas.drawString(57, Puntero, Etiquetas[i])
        canvas.setFont('Helvetica-Bold', 9)
        canvas.drawString(195, Puntero, Conv[i])
        canvas.setFont('Helvetica', 9)
        canvas.drawString(250, Puntero, str(round(Valores_plano[i],3)))
        canvas.line(55,Puntero-2,300,Puntero-2)
    canvas.setFont('Helvetica-Bold', 9)
    canvas.drawString(150, 136, 'CONVENCIONES') 
    canvas.setFont('Helvetica-Bold', 7)
    canvas.drawString(370, 76, Nombre_Usuario)   
    canvas.drawString(370, 67, Nombre_Paila)  
    canvas.drawString(370, 60, 'AGROSAVIA') 
    canvas.setFont('Helvetica-Bold', 5)
    tiempo = time.asctime(time.localtime(time.time()))
    canvas.drawString(460,35,str(tiempo))
    canvas.line(55,134,55,Puntero-2)
    canvas.line(180,134,180,Puntero-2)
    canvas.line(220,134,220,Puntero-2)
    canvas.line(300,134,300,Puntero-2)
    canvas.save()

"""--->>>Está función convierte en milimetros las dimensiones y envia los 
parámetros de salida a la función para exportar a pdf<<<<----"""   
    #Hfn        Altura de fondo
    #Hfa o hfl  Altura falca
    #hal        Altura aletas
    #An o A     Ancho de paila
    #Hc         Altura de casco
    #H          Altura total     
def Dibujar_plano(Nombre_Sitio,Nombre_archivo,Tipo_paila,H_fl,H_fn,Ancho,L,Ho,Hc,N_Aletas,h_Aletas,Angulo,nT,dT,lT,lC,Cantidad_canales,Activar_Aletas):
    global Cantidad_pailas
    global Lista_de_pailas
    #Convertir medidas en milimetros
    A=H_fl*1000                             #0
    B=H_fn*1000                             #1
    C=Ancho*1000                            #2
    G=L*1000                                #3
    E=(L*1000)+100                          #4
    D=2*(math.sin((math.pi/2)-Angulo)*H_fl)+Ancho    #5
    D=D*1000
    I=(180*Angulo)/math.pi                                #6
    F=h_Aletas*1000                         #7
    H=0.07*1000                             #8- 0.07 es la separación entre aletas
    J=N_Aletas                              #9
    K=Hc*1000                               #10
    L=Ho*1000                               #11 ACDIK
    M=nT                                    #12
    N=dT*1000                               #13
    O=lT*1000                               #14
    P=lC*1000                               #15
    Q=Cantidad_canales                      #16
    Valores_plano=[A,B,C,D,E,G,I,F,H,J,K,L,M,N,O,P,Q] 
    if Tipo_paila==1:
        if Activar_Aletas==True:
            Cantidad_pailas[0]=Cantidad_pailas[0]+1
            Lista_de_pailas[0]='Plana'
            Crear_plano_pdf('static/Pailas/Plana_con_aletas.png', Nombre_archivo,
                            Nombre_Sitio, 'Diagrama de una paila plana con aletas', Valores_plano, [10,11,12,13,14,15,16])
        else:
            Cantidad_pailas[1]=Cantidad_pailas[1]+1
            Lista_de_pailas[1]='Plana SA'
            Crear_plano_pdf('static/Pailas/Plana_sin_aletas.png', Nombre_archivo,
                            Nombre_Sitio, 'Diagrama de una paila plana sin aletas', Valores_plano, [7,8,9,10,11,12,13,14,15,16])
    
    elif Tipo_paila==2: 
        if Activar_Aletas==True:
            Cantidad_pailas[2]=Cantidad_pailas[2]+1
            Lista_de_pailas[2]='Pirotubular'
            Crear_plano_pdf('static/Pailas/Pirotubular_circular_con_aletas.png', Nombre_archivo,
                            Nombre_Sitio, 'Diagrama de una paila pirotubular circular con aletas', Valores_plano, [10,11,14,15,16])
        else:
            Cantidad_pailas[3]=Cantidad_pailas[3]+1
            Lista_de_pailas[3]='Pirotubular SA'
            Crear_plano_pdf('static/Pailas/Pirotubular_circular_sin_aletas.png', Nombre_archivo,
                            Nombre_Sitio, 'Diagrama de una paila pirotubular circular sin aletas', Valores_plano, [7,8,9,10,11,14,15,16])
    
    elif Tipo_paila==3:
        Cantidad_pailas[4]=Cantidad_pailas[4]+1
        Lista_de_pailas[4]='Semiesferica'
        Crear_plano_pdf('static/Pailas/Semiesferica.png', Nombre_archivo,
                        Nombre_Sitio, 'Diagrama de una paila semiesférica', Valores_plano, [1,4,5,7,8,9,11,12,13,14,15,16])   
        
    elif Tipo_paila==4:
        if Activar_Aletas==True:
            Cantidad_pailas[5]=Cantidad_pailas[5]+1
            Lista_de_pailas[5]='Semicilindria'
            Crear_plano_pdf('static/Pailas/Semicilindrica_con_aletas.png', Nombre_archivo,
                            Nombre_Sitio, 'Diagrama de una paila semicilindrica con aletas', Valores_plano, [1,12,13,14,15,16])
        else:
            Cantidad_pailas[6]=Cantidad_pailas[6]+1
            Lista_de_pailas[6]='Semicilindrica SA'
            Crear_plano_pdf('static/Pailas/Semicilindrica_sin_aletas.png', Nombre_archivo,
                            Nombre_Sitio, 'Diagrama de una paila semicilindrica sin aletas', Valores_plano, [1,7,8,9,12,13,14,15,16])

    elif Tipo_paila==5:
        if Activar_Aletas==True:
            Cantidad_pailas[7]=Cantidad_pailas[7]+1
            Lista_de_pailas[7]='Pirotubular cuadrada'
            Crear_plano_pdf('static/Pailas/Pirotubular_cuadrada_con_aletas.png', Nombre_archivo,
                            Nombre_Sitio, 'Diagrama de una paila pirotubular cuadrada con aletas', Valores_plano, [10,11,13,15,16])
        else:
            Cantidad_pailas[8]=Cantidad_pailas[8]+1
            Lista_de_pailas[8]='Pirotubular cuadrada SA'
            Crear_plano_pdf('static/Pailas/Pirotubular_cuadrada_sin_aletas.png', Nombre_archivo,
                            Nombre_Sitio, 'Diagrama de una paila pirotubular cuadrada sin aletas', Valores_plano, [7,8,9,10,11,13,15,16])    

    elif Tipo_paila==6:
        if Activar_Aletas==True:
            Cantidad_pailas[9]=Cantidad_pailas[9]+1
            Lista_de_pailas[9]='Cuadrada acanalada'
            Crear_plano_pdf('static/Pailas/Cuadrada_acanalada_con_aletas.png', Nombre_archivo,
                            Nombre_Sitio, 'Diagrama de una paila cuadrada acanalada con aletas', Valores_plano, [10,11,12,13,14])
        else:
            Cantidad_pailas[10]=Cantidad_pailas[10]+1
            Lista_de_pailas[10]='Cuadrada acanalada SA'
            Crear_plano_pdf('static/Pailas/Cuadrada_acanalada_sin_aletas.png', Nombre_archivo,
                            Nombre_Sitio, 'Diagrama de una paila cuadrada acanalada sin aletas', Valores_plano, [7,8,9,10,11,12,13,14])     


"""**************************************************************************"""
"""--->>>Este grupo de funciones estima las dimensiones de la geometria de la 
paila<<<----"""
def Cantidad_Aletas(A,B_Aletas):
    #El numero de aletas es un parámetro que varia en función del 
    #ancho de la paila.Lla separación minima entre ellas es de 7cm
    if(B_Aletas==True):
        Separacion_Aletas=0.07
        return round(A/Separacion_Aletas,0), Separacion_Aletas	
    else:
        return 0, 0
    
#Orden de las variables de salida
#Volumen_Total, Ang, N_Aletas_Canal ó N_Aletas, h_Aletas, Seperacion_Aletas, dT, nT, lT, N_Canales
                
def Semiesferica(H_fn,A,H_fl):
    R=(((A/2)**2)+(H_fn**2))/(2*H_fn)	
    Ang=68*math.pi/180
    VTJ=(math.pi*(H_fn**2)*(3*R-H_fn))/3
    A1=math.pi*((A/2)**2)
    x=A+2*(H_fl/math.tan(Ang))
    A2=x**2
    VFA=(H_fl*(A1+A2+math.sqrt(A1*A2)))/3
    Volumen_Total=VFA+VTJ	
    return [Volumen_Total, Ang, 0, 0, 0, 0, 0, 0, 0, 0]

def Semicilindrica(H,Hc,A,L,Hfa,B_Aletas):
    #la altura de las aletas es fijo por ahora 10cm
    N_Aletas_Canal, Separacion_Aletas=Cantidad_Aletas(A,B_Aletas)
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
    return [Volumen_Total, Ang, N_Aletas_Canal, h_Aletas, Separacion_Aletas, 0, 0, 0, 0, 0]
       
def Plana(H_fl,H_fn,A,L,B_Aletas): 
    #La altura de las aletas es fijo por ahora 10cm
    N_Aletas, Separacion_Aletas=Cantidad_Aletas(A,B_Aletas)
    h_Aletas=0.01
    Ang=68*math.pi/180
    Area=(A*L)+(2*A*H_fn)+(2*H_fn*L)	
    Volumen_Fon=(H_fn*A*L)	
    Volumen_Total=(A*H_fn*L)+(A+H_fl/math.tan(Ang))*H_fl*L
    """Otros parámetros"""
    Porcentaje_Llenado=Volumen_Fon/Volumen_Total
    Area_TCC=(2*h_Aletas*L*N_Aletas)+Area
    return [Volumen_Total, Ang, N_Aletas, h_Aletas, Separacion_Aletas, 0, 0, 0, 0, 0]
	
def Pirotubular_Circular(H_fl,H_fn,A,L,B_Aletas):   
    #dT es el diametro del tubo
    #nT es el numero de tubos
    #La altura de las aletas es fijo por ahora 10cm
    N_Aletas, Separacion_Aletas=Cantidad_Aletas(A,B_Aletas)
    h_Aletas=0.01
    Ang=68*math.pi/180
    dT=H_fn/3
    nT=round((A+dT)/(dT*2))
    Volumen_Fon=((H_fn*A)-(((math.pi/4)*(dT**2))*nT))*L
    Volumen_Total=Volumen_Fon+(L*H_fl*(A+H_fl/math.tan(Ang)))
    """Otros parámetros"""
    Porcentaje_Llenado=Volumen_Fon/Volumen_Total
    Area_TCC=((((H_fn)*(A))-(2*((math.pi/4)*dT**2)*nT))+(2*(H_fn*L)+(A*L)))+(math.pi*dT*L*nT)+(2*(L*h_Aletas)+(2*(h_Aletas))*N_Aletas)
    return [Volumen_Total, Ang, N_Aletas, h_Aletas, Separacion_Aletas, dT, nT, 0, 0, 0]

def Pirotubular_Cuadrada(H_fl,H_fn,A,L,B_Aletas):           
    #lT es la medida de un lado de un tubo cuadrado
    #nT es el numero de tubos
    #La altura de las aletas es fijo por ahora 10cm
    N_Aletas, Separacion_Aletas=Cantidad_Aletas(A,B_Aletas)
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
    return [Volumen_Total, Ang, N_Aletas, h_Aletas, Separacion_Aletas, 0, nT, lT, 0, 0]
    
def Acanalada_Cuadrada(H_fl,H_fn,A,L,B_Aletas):
    #la altura de las aletas es fijo por ahora 10cm
    #lC es la medida de un lado de un canal cuadrado y las aletas van el
    #ducto del canal
    lC=H_fn/3
    N_Aletas_Canal, Separacion_Aletas=Cantidad_Aletas(lC,B_Aletas)
    h_Aletas=0.01
    Ang=68*math.pi/180
    N_Canales=round((A+lC)/(lC*2))
    Area=(A*L+2*L*H_fn+2*A*H_fn)-2*(N_Canales-1)*(lC**2)
    Volumen_Fon=((A*(H_fn-lC))+N_Canales*(lC**2))*L
    Volumen_Total=Volumen_Fon+(L*H_fl*(A+H_fl/math.tan(Ang)))
    """Otros parámetros"""
    Porcentaje_Llenado=Volumen_Fon/Volumen_Total
    Area_TCC=(h_Aletas*L*N_Aletas_Canal*N_Canales*2)+Area
    return [Volumen_Total, Ang, N_Aletas_Canal, h_Aletas, Separacion_Aletas, 0, 0, 0, N_Canales, lC]

"""--->>>-------------------------------------------------------------<<<----"""
"""**************************************************************************"""

"""--->>>Está función mide el valor de aptitud del individuo (Paila)<<<---"""
def Valor_Aptitud(Vol_objetivo,Tipo_paila,H_fl,H_fn,A,L,H,Hc,Activar_Aletas):
    #Semiesferica(H_fn,A,H_fl)
    #Semicilindrica(H,Hc,A,L,Hfa,B_Aletas)
    #Plana(H_fl,H_fn,A,L,B_Aletas)
    #Pirotubular_Circular(H_fl,H_fn,A,L,B_Aletas)
    #Pirotubular_Cuadrada(H_fl,H_fn,A,L,B_Aletas)
    #Acanalada_Cuadrada(H_fl,H_fn,A,L,lC,B_Aletas)
    f=100.0
    if Tipo_paila==1:
        lista_par=Plana(H_fl,H_fn,A,L,Activar_Aletas)
        f=abs(Vol_objetivo-lista_par[0])
        f=(f/Vol_objetivo)*100.0
    elif Tipo_paila==2:
        lista_par=Pirotubular_Circular(H_fl,H_fn,A,L,Activar_Aletas)
        f=abs(Vol_objetivo-lista_par[0])
        f=(f/Vol_objetivo)*100.0
    elif Tipo_paila==3:
        lista_par=Semiesferica(H_fn,A,H_fl)
        f=abs(Vol_objetivo-lista_par[0])
        f=(f/Vol_objetivo)*100.0
    elif Tipo_paila==4:
        lista_par=Semicilindrica(H,Hc,A,L,H_fl,Activar_Aletas)
        f=abs(Vol_objetivo-lista_par[0])
        f=(f/Vol_objetivo)*100.0
    elif Tipo_paila==5:
        lista_par=Pirotubular_Cuadrada(H_fl,H_fn,A,L,Activar_Aletas)
        f=abs(Vol_objetivo-lista_par[0])
        f=(f/Vol_objetivo)*100.0    
    elif Tipo_paila==6:
        lista_par=Acanalada_Cuadrada(H_fl,H_fn,A,L,Activar_Aletas)
        f=abs(Vol_objetivo-lista_par[0])
        f=(f/Vol_objetivo)*100.0 
    return [f, lista_par[0:10]]

"""--->>>>Está funcion esta oculta pero retorna el margen de error del algoritmo
por consola<<<----"""
def Comprobar_diseno(Vol,i,Tipo_paila,H_fl,H_fn,A,L,H,Hc,Activar_Aletas):
    print("Etapa: "+str(i+1))
    print("Capacidad en m^3/kg esperada: "+str(Vol))
    if Tipo_paila==1:
        lista_par=Plana(H_fl,H_fn,A,L,Activar_Aletas)
        print("Capacidad en m^3/kg estimada: "+str(lista_par[0]))
        if(Activar_Aletas==True):
            print("Tipo seleccionado: Plana con aletas")
        else:
            print("Tipo seleccionado: Plana sin aletas")
        print("H_fl: "+str(H_fl))
        print("H_fn: "+str(H_fn))
        print("A: "+str(A))
        print("L: "+str(L))
    elif Tipo_paila==2:
        lista_par=Pirotubular_Circular(H_fl,H_fn,A,L,Activar_Aletas)
        print("Cantidad en Litros estimada: "+str(lista_par[0]))
        if(Activar_Aletas==True):
            print("Tipo seleccionado: Pirotubular circular con aletas")
        else:
            print("Tipo seleccionado: Pirotubular circular sin aletas")
        print("H_fl: "+str(H_fl))
        print("H_fn: "+str(H_fn))
        print("A: "+str(A))
        print("L: "+str(L))
    elif Tipo_paila==3:
        lista_par=Semiesferica(H_fn,A,H_fl)
        print("Cantidad en Litros estimada: "+str(lista_par[0]))
        print("Tipo seleccionado: Semiesferica")
        print("H_fl: "+str(H_fl))
        print("H_fn: "+str(H_fn))
        print("A: "+str(A))
    elif Tipo_paila==4:
        lista_par=Semicilindrica(H,Hc,A,L,H_fl,Activar_Aletas)
        print("Cantidad en Litros estimada: "+str(lista_par[0]))
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
        lista_par=Pirotubular_Cuadrada(H_fl,H_fn,A,L,Activar_Aletas)
        print("Cantidad en Litros estimada: "+str(lista_par[0]))
        if(Activar_Aletas==True):
            print("Tipo seleccionado: Pirotubular cuadrada con aletas")
        else:
            print("Tipo seleccionado: Pirotubular cuadrada sin aletas")
        print("H_fl: "+str(H_fl))
        print("H_fn: "+str(H_fn))
        print("A: "+str(A))
        print("L: "+str(L))        
    elif Tipo_paila==6:
        lista_par=Acanalada_Cuadrada(H_fl,H_fn,A,L,Activar_Aletas)
        print("Cantidad en Litros estimada: "+str(lista_par[0]))
        if(Activar_Aletas==True):
            print("Tipo seleccionado: Acanalada cuadrada con aletas")
        else:
            print("Tipo seleccionado: Acanalada cuadrada sin aletas")
        print("H_fl: "+str(H_fl))
        print("H_fn: "+str(H_fn))
        print("A: "+str(A))
        print("L: "+str(L))

"""--------->>>>limitador de los valores asignados a las dimensiones<<------"""
def comprobar_individuo(Lim_inf,Lim_sup,valor_actual):
    if(valor_actual>=Lim_sup):
        return Lim_sup
    elif (valor_actual<=Lim_inf):
        return Lim_inf
    else:
        return valor_actual

"""--------->>>Función que optimiza las dimensiones de la paila a partir de los,
pesos<<-------------""" 
#Dimensiones de la lamina 4*10 pies o 1.21*3.04 metros (Restricción del sistema)
def Mostrar_pailas(Vol_aux, Etapas, Sitio):
    global Cantidad_pailas
    global Lista_de_pailas
    Tipo_paila=[[],[]]
    Total_pailas=6
    for i in range(Etapas):
        Tipo_paila[0].append(random.randint(1,Total_pailas))
        if(i==0):
            Tipo_paila[1].append(False)
        else:
            Tipo_paila[1].append(random.choice([True,False]))  
    """---->>>>Algoritmo de optimización (Ascenso a la colina)<<<<----"""
    for i in range(Etapas-1,-1,-1):
        f_1=10000000
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
        f_tem=Valor_Aptitud(Volumen,int(Tipo_paila[0][i]),H_fl,H_fn,A,L,H,Hc,bool(Tipo_paila[1][i]))
        f=f_tem[0]
        #Memorias tempales
        H_fl_1 = 0
        H_fn_1 = 0
        A_1 = 0
        L_1 = 0
        H_1 = 0
        Hc_1 = 0
        while ((0.2<f)and(iteraciones<50000)):
            if(f_1<f):
                H_fl = H_fl_1
                H_fn = H_fn_1
                A    = A_1
                L    = L_1
                H    = H_1
                Hc   = Hc_1
                f_tem=Valor_Aptitud(Volumen,int(Tipo_paila[0][i]),H_fl,H_fn,A,L,H,Hc,bool(Tipo_paila[1][i]))
                f=f_tem[0]
                lista_par=f_tem[1][1:10]   
            H_fl_1 = comprobar_individuo(0.05, 1.00, abs(random.uniform(0.05, 1.00)))
            H_fn_1 = comprobar_individuo(0.05, 0.50, abs(random.uniform(0.05, 0.50)))
            A_1    = comprobar_individuo(0.15, 1.00, abs(random.uniform(0.15, 1.00)))
            L_1    = comprobar_individuo(0.30, 3.00, abs(random.uniform(0.40, 3.00)))
            H_1    = comprobar_individuo(0.02, 1.50, abs(random.uniform(0.02, 1.50)))
            Hc_1   = comprobar_individuo(0.05, 0.50, abs(random.uniform(0.05, 0.50)))
            f_tem=Valor_Aptitud(Volumen,int(Tipo_paila[0][i]),H_fl_1,H_fn_1,A_1,L_1,H_1,Hc_1,bool(Tipo_paila[1][i]))
            f_1=f_tem[0]
            iteraciones=iteraciones+1
        """--->>>Llamado a la función para esquematizar un plano en archivo pdf<<<----"""
        #lista_par[0]>>>Ang
        #lista_par[1]>>>N_Aletas_Canal ó N_Aletas
        #lista_par[2]>>>h_Aletas
        #lista_par[3]>>>Seperacion_Aletas
        #lista_par[4]>>>dT
        #lista_par[5]>>>nT
        #lista_par[6]>>>lT
        #lista_par[7]>>>N_Canales
        #lista_par[8]>>>lC
        if(i<9):
            Texto_etapa= "0"+str(i+1)
        else:
            Texto_etapa= str(i+1)
        Dibujar_plano(Sitio+" [Paila: "+Texto_etapa+"]","static/pdf01/B1_Etapa_"+Texto_etapa,int(Tipo_paila[0][i]),
                      H_fl,H_fn,A,L,H,Hc,lista_par[1],lista_par[2],lista_par[0],lista_par[5],
                      lista_par[4],lista_par[6],lista_par[8],lista_par[7],bool(Tipo_paila[1][i])
                      )
        """Eliminar comentarios para probar el algoritmo de optimización"""
        #Comprobar_diseno(Volumen,i,int(Tipo_paila[0][i]),H_fl,H_fn,A,L,H,Hc,bool(Tipo_paila[1][i]))
        #print("________>>>>>>>>>>>>>____________")
        #print(str(iteraciones))
        #print(str(f)) 
    Dibujar_planta()
    df = pd.DataFrame([Lista_de_pailas, Cantidad_pailas])
    df.to_excel('static/Temp/Temp2.xlsx')
    Cantidad_pailas=[0,0,0,0,0,0,0,0,0,0,0]
    Lista_de_pailas=[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']