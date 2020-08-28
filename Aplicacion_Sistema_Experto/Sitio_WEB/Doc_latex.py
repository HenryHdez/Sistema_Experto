# -*- coding: utf-8 -*-

import numpy as np 
import pandas as pd
import shutil
from difflib import SequenceMatcher as SM
# importing from a pylatex module 
from pylatex import Document, Section, Subsection, Tabular, Command, MediumText, SmallText, HugeText, LargeText, TextColor, LineBreak, NewPage, Itemize
from pylatex import Math, TikZ, Axis, Plot, SubFigure, Figure, Matrix, Alignat, VerticalSpace, Center
from pylatex.utils import italic, NoEscape, bold
from pylatex.package import Package

class Documento_Latex():
    global doc
    
    def portada(Diccionario, eficiencia,T_Hornilla):
        global doc
        doc = Document()
        geometry_options = {"tmargin": "4cm", "rmargin": "2cm", "lmargin": "4cm", "bmargin": "3cm"} 
        doc = Document(geometry_options=geometry_options)
        doc.packages.append(Package('babel', options=['spanish']))
        doc.packages.append(Package('background', options=['pages=all']))
        doc.packages.append(NoEscape('\\backgroundsetup{placement=center,\n angle=0, scale=1, contents={\includegraphics{Membrete.pdf}}, opacity=1}\n'))   
        
        with doc.create(Center()) as centered:
                    centered.append(TextColor('white','HH')) 
                    for i in range(15):
                        centered.append(LineBreak())   
                    centered.append(HugeText('PROPUESTA DE VALOR PARA LA CONSTRUCCIÓN DE UNA HORNILLA'))
                    for i in range(10):
                        centered.append(LineBreak())
                    #centered.append(VerticalSpace('50')) 
                    centered.append(LargeText('Presentado por: AGROSAVIA'))
                    centered.append(LineBreak())
                    centered.append(SmallText('(Corporación Colombiana de Investigación Agropecuaria)'))
        doc.append(NewPage())
        
        with doc.create(MediumText(' ')) as tlg:
                    tlg.append(TextColor('white','HH')) 
                    tlg.append(LineBreak())
                    tlg.append('Bogotá D.C., ')
                    tlg.append(Command(' ',NoEscape('\\today')))
                    tlg.append('\n \n') #Salto de línea en parráfo
                    tlg.append(LineBreak()) #Salto de línea en parráfo
                    tlg.append('\nSeñor (es):') 
                    tlg.append('\n'+str(Diccionario['Nombre de usuario']))
                    tlg.append('\n'+str(Diccionario['Departamento'])+', '+str(Diccionario['Ciudad'])+'.')
                    tlg.append('\n \n') #Salto de línea en parráfo
                    tlg.append('\nApreciado(s) productor(es):')
                    tlg.append('\n \n') #Salto de línea en parráfo
                    Parrafo= ('Con base en la información suministrada, está aplicación ha tasado (ver Sección 1) la construcción de una hornilla '+
                              T_Hornilla+' con capacidad de '+ str(Diccionario['Capacidad estimada de la hornilla']) +' kg/h; adecuada para el procesamiento de hasta '+
                              str(Diccionario['Área cosechada al mes'])+
                              ' ha'+' de caña, con un rendimiento de '+ str(float(Diccionario['Caña molida al mes']))+
                              ' T/mes y un periodo vegetativo de '+ str(Diccionario['Periodo vegetativo'])+' meses. Teniendo en cuenta que'+
                              ' se realizan '+str(Diccionario['Número de moliendas'])+' moliendas al mes se establece una tiene una jornada laboral de '+
                              str(Diccionario['Días de trabajo a la semana'])+ ' días a la semana de '+str(Diccionario['Horas de trabajo al día'])+ ' horas laborables cada una. '+
                              '\n Además, la aplicación estima que para garantizar una operación apropiada de la hornilla durante la producción '+
                              'de panela se requiere de un área (ver Sección 3) disponible de al menos '+'320'+' m² con una configuración de pailas y molino que garantiza una producción de panela de '+
                              '50 toneladas al mes (ver Sección 2)'
                              )
                    tlg.append(Parrafo)                
                    Parrafo= (', cuya productividad puede aumentar al incorporar el sistema de recuperación de calor como se muestra en las tablas del análisis financiero.'
                              )
                    tlg.append(Parrafo)
                    Parrafo= ('\n Finalmente, está propuesta de valor se basa en condiciones del terreno ideales y estacionarias, por lo que, '+
                              'AGROSAVIA no se hace responsable de la reproducción total o parcial del material aquí suministrado sin una aprobación '+
                              'corporativa. No obstante, la corporación ofrece los siguientes servicios de asistencia técnica para ajustar los valores provistos en esta propuesta de valor:')           
                    tlg.append(Parrafo)
                    
                    with tlg.create(Itemize()) as itemize:
                        itemize.add_item('Estudio detallado para la construcción e instalación de la hornilla.')
                        itemize.add_item('Una visita técnica de dos funcionarios de AGROSAVIA para la puesta en marcha y '+
                                         'capacitación de los operarios en el manejo de la hornilla y en la producción de panela '+
                                         'saborizada, granulada o moldeada en presentación pastilla de chocolate.')
                        itemize.add_item('Entrega de un ejemplar de la guía tecnológica para el manejo integral del sistema '+
                                         'productivo de la caña panelera y una para el mantenimiento de la hornilla.')
                    Parrafo= ('Cualquier inquietud AGROSAVIA está presta a atenderla.\n'+
                              'Cordial saludo.\n'+
                              '\n \n \n \n'+
                              'AGROSAVIA (Corporación colombiana de investigación agropecuaria)')            
                    tlg.append(Parrafo)            
        doc.append(NewPage())
        
        with doc.create(MediumText(' ')) as tlg:
                    tlg.append(LargeText(bold('Contenido')))
                    with tlg.create(Itemize()) as itemize:
                                            itemize.add_item('Sección 1')
                                            with itemize.create(Itemize()) as item:
                                                        item.add_item('Información del usuario.')
                                                        item.add_item('Características de la caña sembrada.')
                                                        item.add_item('Características del molino.')
                                                        item.add_item('Análisis financiero.')
                                            itemize.add_item('Sección 2')
                                            with itemize.create(Itemize()) as item:
                                                        item.add_item('Diagramas mecánicos de las pailas.')
                                                        item.add_item('Diagramas mecánicos del recuperador de calor.')
                                            itemize.add_item('Sección 3')                    
                                            with itemize.create(Itemize()) as item:
                                                        item.add_item('Diagramas mecánicos de la chimenea.')
                                                        item.add_item('Diagramas mecánicos del ducto.')
                                                        item.add_item('Diagramas mecánicos de la chimenea.')
                                                        item.add_item('Diagramas mecánicos del proceso productivo.')
        doc.append(NewPage())
        
        with doc.create(Center()) as centered:
                    centered.append(TextColor('white','HH')) 
                    for i in range(15):
                        centered.append(LineBreak())   
                    centered.append(HugeText('SECCIÓN 1:'))
                    centered.append(LineBreak())
                    centered.append(HugeText('INFORMACIÓN TÉCNICA Y FINANCIERA')) 
        doc.append(NewPage())
                    
    def titulos_I (texto, Palabra):
        with texto.create(Center()) as centered:
                    centered.append(HugeText(Palabra))
                    centered.append(LineBreak()) 
        return texto
    
    #Cambiar formato a miles
    def Formato_Moneda(num, simbolo, n_decimales):
        n_decimales = abs(n_decimales) #abs asegura que los dec. sean positivos.
        num = round(num, n_decimales) #Redondear a los decimales indicados
        num, dec = str(num).split(".") #Se divide el numero en cadenas y convierte en String
        dec += "0" * (n_decimales - len(dec)) #Concatenar ceros a la cadena
        num = num[::-1] #Inversion del vector para agregar comas
        l = [num[pos:pos+3][::-1] for pos in range(0,50,3) if (num[pos:pos+3])] #Separador de miles
        l.reverse() #Invierte nuevamente
        num = str.join(",", l) #unir string por comas
        try: #eliminar parte negativa
            if num[0:2] == "-,":
                num = "-%s" % num[2:]
        except IndexError:
            pass
        #si no se especifican decimales, se retorna un numero entero.
        if not n_decimales:
            return "%s %s" % (simbolo, num)
        return "%s %s.%s" % (simbolo, num, dec)
    
    def seccion1(D1, D2):
        global doc
        '''>>>>>>>>>>>>>>>Presentación de los datos de usuario<<<<<<<<<<<<<<<<<'''        
        doc = Documento_Latex.titulos_I (doc, 'DATOS DEL USUARIO')         
        with doc.create(Tabular('lccccl')) as table:
            for i in D1:
                if(str(i)=='DATOS DE ENTRADA'):
                    break
                else:
                    if(SM(None, 'Variedad de Caña', i).ratio()<0.85):
                        T1=str(D1[i])
                        #Arreglo para asignar unidades y mostrarlas en el informe
                        if (str(i)=='Área caña sembrada'):
                            T1=str(D1[i])+" ha" 
                        elif (str(i)=='Crecimiento aproximado del área sembrada'):
                            T1=str(D1[i])+" ha"
                        elif (str(i)=='Caña esperada por hectárea'):
                            T1=str(D1[i])+" T/ha"
                        elif (str(i)=='Número de moliendas'):
                            T1=str(D1[i])+" semanal(es)"                    
                        elif (str(i)=='Periodo vegetativo'):
                            T1=str(D1[i])+" mes(es)"                   
                        elif (str(i)=='Caña molida al mes'):
                            T1=str(D1[i])+" T/mes" 
                        elif (str(i)=='Área cosechada al mes'):
                            T1=str(D1[i])+" ha/mes" 
                        elif (str(i)=='Caña molida a la semana'):
                            T1=str(D1[i])+" T/semana" 
                        elif (str(i)=='Caña molida por Hora'):
                            T1=str(D1[i])+" T/hora"
                        table.add_row((bold(str(i)), ' ', ' ', ' ', ' ',T1))
        doc.append(NewPage())
        
        '''>>>>>>>>>>>>>>>>>>>>Presentación de los datos de la caña<<<<<<<<<<<<<<<<<<<<<<<'''
        doc = Documento_Latex.titulos_I (doc, 'CARACTERÍSTICAS DE LAS VARIEDADES DE CAÑA SELECCIONADAS')
        Canas=pd.read_excel('static/Temp/Temp4.xlsx',skipcolumn = 0,)
        Carpe=pd.read_excel('static/Temp/Temp5.xlsx',skipcolumn = 0,)
        Eti = Canas.iloc[0].values
        Val = Canas.iloc[1].values
        Car = Carpe.iloc[0].values
        
        conta=1
        for i in range (len(Car)-1):
            with doc.create(Tabular('lcccccl')) as table:
                for j in range (1,9):
                    table.add_row((bold(str(Eti[conta])), ' ', ' ', ' ', ' ', ' ', str(Val[conta])))
                    conta=conta+1
                conta=conta+1
            doc.append(LineBreak())
            doc.append('\n')
            doc.append(LineBreak())
        
        for i in range (1,len(Car),3):
            with doc.create(Figure(position='h!')) as imagesRow1:
                for j in range(3):
                    if((i+j)<len(Car)):
                        with doc.create(
                            SubFigure(width=NoEscape(r'0.33\linewidth'))) as left_imagesRow1:
                            left_imagesRow1.add_image(Car[i+j], width=NoEscape(r'0.95\linewidth'))
                            left_imagesRow1.add_caption('Variedad de caña '+str(i+j))
                imagesRow1.append(LineBreak())
                imagesRow1.append(NewPage())  
        
        doc.append(NewPage())
        doc.append(TextColor('white','HH')) 
        doc.append(NewPage())
        
        '''>>>>>>>>>>>>>>>>>>>>Presentación de los molinos seleccionados<<<<<<<<<<<<<<<<<<<<<<<'''   
        doc = Documento_Latex.titulos_I (doc, 'MOLINOS PRESELECCIONADOS PARA ESTE DISEÑO')
        Molino=pd.read_excel('static/Temp/Temp.xlsx',skipcolumn = 0,)
        Carpe=pd.read_excel('static/Temp/Temp5.xlsx',skipcolumn = 0,)
        Eti = Canas.iloc[0].values
        Val = Canas.iloc[1].values
        Car = Carpe.iloc[0].values
        Marca=Molino['Marca'].values
        Modelo=Molino['Modelo'].values
        Kilos=Molino['kg/hora'].values
        Diesel=Molino['Diesel'].values
        Electrico=Molino['Electrico'].values
        Valor=Molino['Precio'].values

        with doc.create(Tabular('lcccccl')) as table:
                table.add_row((TextColor('red',bold('VALOR APROXIMADO DE UN MOLINO: ')),
                               ' ', ' ', ' ', ' ', ' ', 
                               TextColor('red', Documento_Latex.Formato_Moneda(sum(Valor)/len(Valor), "$", 2))))
        doc.append(LineBreak())
                
        with doc.create(Tabular('ccccc')) as table:  
            table.add_row("MARCA", "MODELO", "KG POR HORA", "DIESEL O GASOLINA (HP)", "ELÉCTRICO (HP)")
            table.add_empty_row()
            for i in range(len(Marca)):
                table.add_row(str(Marca[i]),
                              str(Modelo[i]), 
                              str(Kilos[i]), 
                              str(Diesel[i]), 
                              str(Electrico[i]))
                
            doc.append(LineBreak())
            doc.append('\n')
            doc.append(LineBreak())
        
        for i in range (1,len(Modelo),3):
            with doc.create(Figure(position='h!')) as imagesRow1:
                for j in range(3):
                    if((i-1)+j<len(Modelo)):
                        with doc.create(
                            SubFigure(width=NoEscape(r'0.33\linewidth'))) as left_imagesRow1:
                            left_imagesRow1.add_image('Molinos/'+str(Modelo[(i-1)+j]+'.jpg'), width=NoEscape(r'0.95\linewidth'))
                            left_imagesRow1.add_caption(str(Modelo[(i-1)+j]))
                imagesRow1.append(LineBreak())
                imagesRow1.append(NewPage()) 
        
        doc.append(NewPage())
        doc.append(TextColor('white','HH')) 
        doc.append(NewPage())                

            
    def generar_pdf():  
        global doc
        doc.generate_pdf('static/Latex/A0_Cotizacion', clean_tex=False) 
        shutil.copy('static/Latex/A0_Cotizacion.pdf', 'static/pdf01/A0_Cotizacion.pdf')



