'''----Definición de las librerías requeridas para la ejecución de la aplicación---'''
from flask import Flask, request, render_template        #Interfaz gráfica WEB
from difflib import SequenceMatcher as SM                #Detección de secuencias en estructuras de texto
from werkzeug.utils import secure_filename               #Encriptar información archivos de pdf
from email.mime.multipart import MIMEMultipart           #Creación del cuerpo del correo electrónico 1
from email.mime.application import MIMEApplication       #Creación del cuerpo del correo electrónico 2            
from email.mime.text import MIMEText                     #Creación del cuerpo del correo electrónico 3
from shutil import rmtree                                #Gestión de directorios en el servidor
import smtplib                                           #Conexión con el servidor de correo
from rpy2.robjects import r                              #Interfaz entre PYTHON y R
from rpy2.robjects import numpy2ri                       #Interfaz entre PYTHON y R
from time import sleep                                   #Suspensión temporal
import pandas as pd                                      #Gestión de archivos de texto
import os                                                #Hereda funciones del sistema operativo para su uso en PYTHON
import math                                              #Operaciones matemáticas                    
import base64                                            #Codifica contenido en base64 para su almacenamiento en una WEB
import pyodbc                                            #Interfaz de conexión con la base de datos
import Doc_latex                                         #Gestión de documentos en LATEX en PYTHON debe tener preinstalado MIKTEX
'''---Componentes y lbrería de elaboración propia---'''
import Diseno_inicial                                    #Calculo preliminar de la hornilla
import Costos_funcionamiento                             #Calculo del costo financiero de la hornilla
import Pailas                                            #Calculo de las dimensiones de las pailas
import Gases                                             #Calculo de las propiedades de los gases

#Generación de la interfaz WEB
app = Flask(__name__)
#Creación de directorio temporal para almacenar archivos
uploads_dir = os.path.join(app.instance_path, 'uploads')
try:
    os.makedirs(uploads_dir, True)
except OSError: 
    print('Directorio existente')
   
'''---Funciones de direccionamiento en la interfaz WEB---'''
#Eliminar datos cargados en cache al actualizar la página.
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = '0'
    response.headers["Pragma"] = "no-cache"
    return response
#Directorio raíz (página principal)
@app.route('/')
def index():
    try:
        rmtree('static/pdf2')
    except OSError: 
        print('Directorio eliminado')
    return render_template('principal.html')

#Formulario para el ingreso de datos de usuario
@app.route('/usuario')
def usua():
    global df  
    global paises
    global Deptos_cana
    global Ciudad_cana
    global Tipo_cana
    global Grados_Bx
    global Nivel_pH
    global Nivel_azucar
    global Nivel_Sacarosa
    global Nivel_pureza
    global Nivel_Fosforo
    global Nivel_Calidad
    global Nivel_brpane 
    global Cana_ha
    df             = pd.read_json("static/Catalogos/Colombia.json")
    paises         = pd.read_excel("static/Catalogos/Paises.xlsx") 
    cana           = pd.read_excel("static/Catalogos/Variedades.xlsx")
    Deptos_cana    = cana['Depto'].values
    Ciudad_cana    = cana['Ciudad'].values
    Tipo_cana      = cana['Tipo'].values
    Grados_Bx      = cana['Br'].values
    Nivel_pH       = cana['pH'].values
    Nivel_azucar   = cana['Azucares'].values
    Nivel_Sacarosa = cana['Sacarosa'].values
    Nivel_pureza   = cana['Pureza'].values
    Nivel_Fosforo  = cana['Forforo'].values
    Nivel_Calidad  = cana['Calidad'].values 
    Nivel_brpane   = cana['BrPanela'].values
    Cana_ha        = cana['ProduccionCana'].values
    Variedad_cana  = []
    for i in range(0, len(Deptos_cana)):
        if(i==0):
            Variedad_cana.append(Tipo_cana[i]+", -Valor por defecto-, °Brix= "+str(Grados_Bx[i]))
        else:
            Variedad_cana.append(Tipo_cana[i]+", Disponible en: "+Deptos_cana[i]+"-"+Ciudad_cana[i]+", °Brix= "+str(Grados_Bx[i]))
    return render_template('usuario.html', 
                           paises_lista=paises['Nombre'],
                           departamentos=df.departamento, 
                           provincia=df.ciudades,
                           Ciudad_cana_1=Ciudad_cana,
                           Variedad_cana_1=Variedad_cana,
                           )      

#Codificar los pdf en formato de texto plano
def Crear_archivo_base_64(ruta):
    with open(ruta, 'rb') as Archivo_codificado_1:
        Archivo_binario_1 = Archivo_codificado_1.read()
        Archivo_binario_64_1 = base64.b64encode(Archivo_binario_1)
        Mensaje_base_64_1 = Archivo_binario_64_1.decode('utf-8')
        return Mensaje_base_64_1
    
#De-codificar los pdf en formato de texto plano
def Leer_pdf_base64(Nombre_pdf, Texto_base64):
    PDF_Base64 = Texto_base64.encode('utf-8')
    with open(Nombre_pdf, 'wb') as Archivo_Normal:
        Archivo_deco = base64.decodebytes(PDF_Base64)
        Archivo_Normal.write(Archivo_deco)
        
#Función para crear los diccionarios a partir de los calculos de la aplicación
def generar_valores_informe():
    #----------->>>>>>>>>>>Variables globales<<<<<<<<<<<<<<<---------
    global df
    global result
    global altura_media
    global NivelFre
    global Diccionario
    global Formulario_1_Etiquetas
    global Formulario_1_Valores
    global Formulario_2_Etiquetas
    global Formulario_2_Valores
    global Formulario_2a_Etiquetas
    global Formulario_2a_Valores
    global Directorio
    global Deptos_cana
    global Ciudad_cana
    global Tipo_cana
    global Grados_Bx
    global Nivel_pH
    global Nivel_azucar
    global Nivel_Sacarosa
    global Nivel_pureza
    global Nivel_Fosforo
    global Nivel_Calidad
    global Nivel_brpane
    global Cana_ha
    global Diccionario 
    global Diccionario_2
    global Diccionario_3
    global Diccionario_4
    """Creación de la primer parte del diccionario (leer del formulario de usuario)"""
    Pais_sel=result.get('Pais')
    if(Pais_sel=='Colombia'):
        a=result.to_dict() 
        Dept=result.get('Departamento')
        D_aux=df.departamento
        D_aux=D_aux.tolist()
        amsnm=df.altura
        amsnm=amsnm.tolist()
        H2O=df.aguasubterranea
        H2O=H2O.tolist()
        altura_media=amsnm[D_aux.index(Dept)]
        NivelFre=H2O[D_aux.index(Dept)]
        Nombre_Rot="Hornilla: "+a['Nombre de usuario']+" ("+a['Departamento']+'-'+a['Ciudad']+")"
    else:
        a=result.to_dict() 
        altura_media=200
        NivelFre='desde 100 m'   
        a['Departamento']='--'
        a['Ciudad']='--'
        Nombre_Rot="Hornilla: "+a['Nombre de usuario']+" ("+a['Pais']+")"
    
    #---------------->>>>>>>>>"""Cálculo del periodo vegetativo"""<<<<<<<<<<<<<<<<<<<
    Formulario_1_Etiquetas=[]
    Formulario_1_Valores=[]
           
    for i in a:
        Formulario_1_Etiquetas.append(i)
        Formulario_1_Valores.append(a[i])
    Formulario_1_Etiquetas.append('Altura media sobre el nivel del mar')
    Formulario_1_Valores.append(str(altura_media)+' m')
    Formulario_1_Etiquetas.append('Nivel freático')
    Formulario_1_Valores.append(str(NivelFre))    
    """Creación de la segunda parte del diccionario"""
    a=result.to_dict()
    cantidadcanas=int(a['Variedades de caña sembrada'])+1
    Formulario_2_Etiquetas=[]
    Formulario_2_Valores=[] 
    Formulario_2a_Etiquetas=[]
    Formulario_2a_Valores=[]
    Directorio =[]
    G_brix_cana=0.0;
    G_brix_panela=0.0;    
    ha_cana_conta=0.0;
    for contacana in range(1,cantidadcanas):
        try:
            Valor_cana_buscar='Variedad de Caña '+str(contacana)
            index=int(a[Valor_cana_buscar])-1 
            Formulario_2_Etiquetas.append(Valor_cana_buscar)
            Formulario_2_Valores.append(Tipo_cana[index])    
            Formulario_2_Etiquetas.append('Grados Brix de la caña '+str(contacana))
            Formulario_2_Valores.append(Grados_Bx[index]) 
            Formulario_2_Etiquetas.append('pH')
            Formulario_2_Valores.append(Nivel_pH[index])    
            Formulario_2_Etiquetas.append('Azúcares reductores (%)')
            Formulario_2_Valores.append(Nivel_azucar[index]) 
            Formulario_2_Etiquetas.append('Sacarosa (%)')
            Formulario_2_Valores.append(Nivel_Sacarosa[index])    
            Formulario_2_Etiquetas.append('Pureza (%)')
            Formulario_2_Valores.append(Nivel_pureza[index])  
            Formulario_2_Etiquetas.append('Fósforo (ppm)')
            Formulario_2_Valores.append(Nivel_Fosforo[index])    
            #Formulario_2_Etiquetas.append('Grados Brix de la panela '+str(contacana))
            #Formulario_2_Valores.append(Nivel_brpane[index])
            Formulario_2_Etiquetas.append('>---------------------------------<')
            Formulario_2_Valores.append('>---------------------------------<')
            G_brix_cana=G_brix_cana+float(Grados_Bx[index])
            G_brix_panela=G_brix_panela+float(Nivel_brpane[index])
            Directorio.append('Cana/'+Tipo_cana[index]+'.png')
            ha_cana_conta=ha_cana_conta+float(Cana_ha[index])
        except:
            print("Variedad no disponible")
    #FORMULARIO 1
    #Agregar caña esperada por ha
    if(a['Usa fertilizante']=='NO'):
        ha_cana_conta=round((ha_cana_conta/cantidadcanas)*0.5,3)
    else:
        ha_cana_conta=round((ha_cana_conta/cantidadcanas)*0.8,3)
    Formulario_1_Etiquetas.append('Caña producida por hectárea (t/ha)')
    Formulario_1_Valores.append(str(ha_cana_conta))
    #Determinar periodo vegetativo
    Formulario_1_Etiquetas.append('Periodo vegetativo')
    Formulario_1_Valores.append(str(round(math.exp((altura_media+5518.9)/2441.1),0)))
    Diccionario=dict(zip(Formulario_1_Etiquetas,Formulario_1_Valores))  
    #FORMULARIO 2
    #Exportar variedades de caña seleccionadas
    datos_temp=[Formulario_2_Etiquetas,Formulario_2_Valores]
    df1 = pd.DataFrame(datos_temp)
    df1.to_excel('static/Temp/Temp4.xlsx')   
    datos_temp=[Directorio]
    df1 = pd.DataFrame(datos_temp)
    df1.to_excel('static/Temp/Temp5.xlsx')  
    #Grados brix promedio para publicar en el informe
    G_brix_cana=round(G_brix_cana/len(Directorio),3)       
    G_brix_panela=round(G_brix_panela/len(Directorio),3)
    Formulario_2a_Etiquetas.append('Grados Brix de la caña (promedio)')
    Formulario_2a_Valores.append(G_brix_cana)
    Formulario_2a_Etiquetas.append('Grados Brix de la panela (promedio)')
    Formulario_2a_Valores.append(G_brix_panela)    
    Dict_aux=dict(zip(Formulario_2a_Etiquetas,Formulario_2a_Valores))
    Diccionario.update(Dict_aux)
    """------------>>>>>>>>>>HORNILLA<<<<<<<<<<<<<<<<----------------"""
    """Calculo de la hornilla"""
    Diccionario   = Diseno_inicial.datos_entrada(Diccionario,0,0)
    Diccionario_2 = Diseno_inicial.Calculo_por_etapas(Diccionario)

    """Estimar propiedades de los gases"""
    Gases.Optimizacion(Diccionario,Diccionario_2)
    """Optimizar tamaño de las pailas"""
    Pailas.Mostrar_pailas(
            Diccionario_2['Volumen de jugo [m^3/kg]'],
            int(Diccionario_2['Etapas']),
            Nombre_Rot,
            Diccionario['Tipo de hornilla'],
            Diccionario['Capacidad estimada de la hornilla']
            )
    """Presentar información del molino"""
    Formulario_3_Etiquetas=['Caña molida al mes', 'Área cosechada al mes',	 'Caña molida a la semana',		
                            'Caña molida por Hora', 'Jugo crudo',	 'Jugo clarificado', 'Masa de panela',		
                            'Capacidad del Molino']
    Formulario_3_Valores=[]
    for i in Formulario_3_Etiquetas:
        Formulario_3_Valores.append(Diccionario[i])
        
    Molino=pd.read_excel('static/Temp/Temp.xlsx',skipcolumn = 0,)
    Marca=Molino['Marca'].values
    Modelo=Molino['Modelo'].values
    Kilos=Molino['kg/hora'].values
    Valor=Molino['Precio'].values
    Enlaces=Molino['Link'].values
    Diccionario_4={'Marca':Marca,
                   'Modelo':Modelo,
                   'Capacidad':Kilos,
                   'Disponible en':Enlaces
            }

    Formulario_3_Etiquetas.append('Valor aproximado de un molino')
    Formulario_3_Valores.append(Costos_funcionamiento.Formato_Moneda(sum(Valor)/len(Valor), "$", 2))
    Diccionario_3=dict(zip(Formulario_3_Etiquetas,Formulario_3_Valores))
    """Analisis financiero"""
    Costos_funcionamiento.Variables(float(Diccionario['Capacidad estimada de la hornilla']),
                                    float(Diccionario['Horas de trabajo de la hornilla al día']), 
                                    float(Diccionario['Días de trabajo de la hornilla a la semana']), 
                                    float(Diccionario['Número de moliendas al mes']),
                                    float(Diccionario['Caña molida al mes']))
    Costos_funcionamiento.costos()
    
    """Generar portada"""
    Eficiencia_hornilla="20" #Cambiar
    Doc_latex.Documento_Latex.portada(Diccionario,Eficiencia_hornilla,Diccionario['Tipo de hornilla'])
    Doc_latex.Documento_Latex.seccion1(Diccionario,Diccionario_2)
    Doc_latex.Documento_Latex.generar_pdf()
    sleep(1)
    """Creación del pdf"""
    Pailas.Generar_reporte(Diccionario,Diccionario_2)

    """>>>>>>>>>>>>>>>>Actualizar base de datos<<<<<<<<<<<<<<"""        
    usuarios = (Diccionario['Nombre de usuario'],
                Diccionario['Correo'],
                int(Diccionario['Telefono']),
                Diccionario['Pais'], 
                Diccionario['Departamento'],
                Diccionario['Ciudad'], 
                Crear_archivo_base_64("static/Informe_WEB.pdf"), 
                Crear_archivo_base_64("static/Planos_WEB.pdf"), 
                Crear_archivo_base_64("static/B3_Etapa_Planta_WEB.pdf"), 
                Crear_archivo_base_64("static/Calculos_WEB.pdf"))
    Operaciones_db(2,usuarios)        #Usar base de datos

#Filtrar caracteres desconocidos de las cadenas de texto de los archivos temporales
def Convertir(string): 
    li = list(string.split(",")) 
    lista_vacia=[]
    for i in li:
        i=i.strip(' ')
        i=i.strip('[')
        i=i.strip(']')
        i=i.strip('\'')
        lista_vacia.append(i)
    return lista_vacia 

#Función para poner formato de moneda en pesos a un número
def Convertir_lista(li,ini):
    for i in range(ini,len(li)):
        try:
            li[i]=Costos_funcionamiento.Formato_Moneda(float(li[i]), "$", 2)
        except:
            li[i]
    return(li)
    
#>>>>>>>>>>>------------Enlaces para la generación del informe------<<<<<<<<<<
#Segmento 5 del informe (presentación de la vista previa del pdf)
@app.route('/informe5')
def infor5():
    return render_template('informe5.html') 

#Segmento 4 del informe (presentación de la vista previa del informe financiero)
@app.route('/informe4')
def infor4():
    Valores_Informe=pd.read_excel('static/Graficas/Temp6.xlsx',skipcolumn = 0,)
    Consolidado = Valores_Informe.iloc[0].values
    l1=Convertir(Consolidado[1])
    l2=Convertir(Consolidado[2])
    Funcionamie = Valores_Informe.iloc[1].values
    l5=Convertir(Funcionamie[1])
    l6=Convertir(Funcionamie[2])
    l6a=l6[0::2]
    l6b=l6[1::2]
    Depreciacio = Valores_Informe.iloc[2].values
    l3=Convertir(Depreciacio[1])
    l4=Convertir(Depreciacio[2])
    l4a=l4[0::2]
    l4b=l4[1::2]
    l2=Convertir_lista(l2,1)
    l4a[1:7]=Convertir_lista(l4a[1:7],3)
    l4b[1:7]=Convertir_lista(l4b[1:7],3)
    l4a[8:11]=Convertir_lista(l4a[8:11],1)
    l4b[8:11]=Convertir_lista(l4b[8:11],1)
    l6a=Convertir_lista(l6a,2)
    l6b=Convertir_lista(l6b,2)
    return render_template('informe4.html',eti1=l1,eti2=l2,L1=len(l1),
                                           eti3=l3,eti4=l4a,eti5=l4b,L2=len(l3),
                                           eti6=l5,eti7=l6a,eti8=l6b,L3=len(l5)) 
    
#Segmento 3 del informe (presentación de los modelos de molino)
@app.route('/informe3')
def infor3():
    global Diccionario_3
    global Diccionario_4
    return render_template('informe3.html',result=Diccionario_3, Molinos=Diccionario_4) 

#Segmento 2 del informe (presentación de las caracteristicas de la caña)
@app.route('/informe2')
def infor2():
    global Formulario_2_Etiquetas
    global Formulario_2_Valores
    global Directorio
    return render_template('informe2.html', 
                           Etiquetas = Formulario_2_Etiquetas, 
                           Valores = Formulario_2_Valores,
                           Dir = Directorio,
                           Cant_fotos=len(Directorio))  

#Segmento 2 del informe (presentación de las caracteristicas de la caña)
@app.route('/informe1')
def infor1():
    global Formulario_1_Etiquetas
    global Formulario_1_Valores
    #rutina para filtrar y eliminar la palabra variedad de caña
    lista_etiquetas_filtradas=[]
    lista_valores_filtrados=[]
    for i in range(len(Formulario_1_Etiquetas)):
        if((SM(None, 'Variedad de Caña', Formulario_1_Etiquetas[i]).ratio()<0.85) and 
           (SM(None, 'Usa fertilizante', Formulario_1_Etiquetas[i]).ratio()<0.85) and
           (SM(None, '--', Formulario_1_Valores[i]).ratio()<0.85)):
            lista_etiquetas_filtradas.append(Formulario_1_Etiquetas[i])
            lista_valores_filtrados.append(Formulario_1_Valores[i])    
    return render_template('informe1.html', 
                           Etiquetas = lista_etiquetas_filtradas, 
                           Valores = lista_valores_filtrados)     

#Segmento 1 del informe (presentación de los datos del usuario)    
@app.route('/informe', methods = ['POST','GET'])
def infor():
    global result
    #Limpiar directorios de uso temporal
    try:
        rmtree('static/Temp')
        os.mkdir('static/Temp')
    except:
        os.mkdir('static/Temp')
    try:    
        rmtree('static/pdf01')
        rmtree('static/pdf02')
        os.mkdir('static/pdf01')
        os.mkdir('static/pdf02')
    except:
        os.mkdir('static/pdf01')
        os.mkdir('static/pdf02')
    #Continuar ejecución
    if request.method == 'POST':
        result = request.form
#        print(result)
        generar_valores_informe()
        return render_template('informe.html') 

#------->>>>>>>>Operaciones básicas con la base de datos<<<<<<<<--------
def Operaciones_db(Operacion, usuarios):
    db_1=[]
    r_b=[]
    Cadena_sql= "DELETE FROM Clientes WHERE ID IN "
    try:
        cnxn = pyodbc.connect(driver='{SQL Server Native Client 11.0}', 
                      host='COMOSDSQL08\MSSQL2016DSC', 
                      database='SistemaExpertoPanela', 
                      user='WebSisExpPanela', 
                      password='sIuusnOsE9bLlx7g60Mz')
        cursor = cnxn.cursor()
        #Consulta
        if(Operacion==0):               
            base_temp=cursor.execute("SELECT * FROM Clientes")
            for tdb in base_temp:
                    db_1.append(tdb)
        #Borrar
        elif(Operacion==1):
            cursor.execute("DELETE FROM Clientes WHERE CONVERT(NVARCHAR(MAX), Nombre)!='NO_BORRAR'")
        #Insertar
        elif(Operacion==2):
            cursor.execute("INSERT INTO Clientes (Nombre, Correo, Telefono, Pais, Departamento, Ciudad, Usuario, Planos, Recinto, Calculos) VALUES (?,?,?,?,?,?,?,?,?,?)", usuarios)
        #Busqueda
        elif(Operacion==3):
            base_temp=cursor.execute("SELECT * FROM Clientes")
            for i,tdb in enumerate(base_temp, start=0):
                try:
                    if(usuarios.get('CH_'+str(tdb[0]))=='on'):
                        r_b.append(str(tdb[0]))
                except:
                    print('No existe')
            T1=str(r_b).replace("[","(")
            T1=T1.replace("]",")")
            Cadena_sql=Cadena_sql+T1
            cursor.execute(Cadena_sql)
        cnxn.commit()
        cnxn.close()
        return db_1
    except:
        print('Error db') 

#Formulario para borrar usuarios completamente
@app.route('/borrar')
def borrar_base_1():
    Operaciones_db(1,0)
    return render_template('principal.html')

#Formulario para borrar usuarios seleccioandos
@app.route('/borrar2', methods = ['POST','GET'])
def borrar_base_2():
    if request.method == 'POST':
        Eliminar = request.form    
        Operaciones_db(3,Eliminar)
    return render_template('principal.html')

#---------->>>>>>>>>Formularios para la presentación de mapas<<<<<<---------
#Calculo de la estadistica para presentar los mapas
@app.route('/presentar')
def mineria():   
    numpy2ri.activate()
    x = "c(1,2,3,3,3,2,2,2,2,1,3,3,3,3,3,3,3,3,2,2,3,3,2,2,1,4,4,2,3,1,2,2)"
    r('''      
        rm(list = ls())        
        library(ggplot2) 
        library(sf)
        library(GADMTools)
        library(mapview)
        COL <- gadm_sf_loadCountries("COL", level=1 )'''+"\n"+
        'COL[["sf"]][["Cantidad de hornillas"]]<-'+x+"\n"+
     '''
        m1=COL$sf %>% mapview(zcol = "Cantidad de hornillas", legend = TRUE, col.regions = COL[["sf"]][["Cantidad de hornillas"]])
        mapshot(m1, url = paste0(getwd(), "/static/mapas/map1A.html"))
     '''
    )
    return render_template('presentar.html')

#Mapa de cantidad de hornillas por departamento
@app.route('/presentar1')
def mineria1():
    return render_template('presentar1.html')

#Variedades de caña conocidas por departamento
@app.route('/presentar2')
def mineria2():   
   return render_template('presentar2.html')

#Productores por departamento
@app.route('/presentar3')
def mineria3():   
   return render_template('presentar3.html')

#Formulario de bienvenida para el acceso a la base de datos
@app.route('/acceso')
def acceso_base():
   return render_template('acceso.html', aviso="Por favor, complete los siguientes campos.")

#Formulario de respuesta al acceder a la base de datos
@app.route('/base', methods = ['POST','GET'])
def base_batos():
    if request.method == 'POST':
        datos_usuario = request.form
        Nombre_Usuario=datos_usuario.get('Documentoa')
        Clave_Usuario=datos_usuario.get('Clavea')
        if(Nombre_Usuario=="12345" and Clave_Usuario=="0000"):
            #Listas para almacenamiento temporal de los datos de usuario
            Etiquetas_ID=[]
            Etiquetas_Nombres=[]
            Etiquetas_Correo=[]
            Etiquetas_Telefono=[]
            Etiquetas_Pais=[]
            Etiquetas_Departamento=[]
            Etiquetas_Ciudad=[]
            Etiquetas_U=[]
            Etiquetas_P=[]
            Etiquetas_R=[]
            Etiquetas_C=[]
            Cantidad_Clientes=0
            try:
                os.mkdir('static/pdf2')
            except OSError: 
                print('Directorio existente') 
            #Consulta de la base de datos
            db=Operaciones_db(0,0)
            #Creación de listas con los datos de usuario
            for listas_1 in db:
                Etiquetas_ID.append(listas_1[0])
                Etiquetas_Nombres.append(listas_1[1])
                Etiquetas_Correo.append(listas_1[2])
                Etiquetas_Telefono.append(listas_1[3])
                Etiquetas_Pais.append(listas_1[4])
                Etiquetas_Departamento.append(listas_1[5])
                Etiquetas_Ciudad.append(listas_1[6])
                Etiquetas_U.append("pdf2/U_"+str(Cantidad_Clientes)+".pdf")
                Etiquetas_P.append("pdf2/P_"+str(Cantidad_Clientes)+".pdf")
                Etiquetas_R.append("pdf2/R_"+str(Cantidad_Clientes)+".pdf")
                Etiquetas_C.append("pdf2/C_"+str(Cantidad_Clientes)+".pdf")
                Cantidad_Clientes=Cantidad_Clientes+1
                try:
                    Leer_pdf_base64("static/pdf2/U_"+str(Cantidad_Clientes)+".pdf", listas_1[7])
                    Leer_pdf_base64("static/pdf2/P_"+str(Cantidad_Clientes)+".pdf", listas_1[8])
                    Leer_pdf_base64("static/pdf2/R_"+str(Cantidad_Clientes)+".pdf", listas_1[9])
                    Leer_pdf_base64("static/pdf2/C_"+str(Cantidad_Clientes)+".pdf", listas_1[10])         
                except:
                    print('Error archivo')
            return render_template('base.html',
                                   Eti0=Etiquetas_ID,
                                   Eti1=Etiquetas_Nombres,
                                   Eti2=Etiquetas_Correo,
                                   Eti3=Etiquetas_Telefono,
                                   Eti3a=Etiquetas_Pais,
                                   Eti4=Etiquetas_Departamento,
                                   Eti5=Etiquetas_Ciudad,
                                   Eti6=Etiquetas_U,
                                   Eti7=Etiquetas_P,
                                   Eti8=Etiquetas_R,
                                   Eti9=Etiquetas_C,
                                   Cant=Cantidad_Clientes)
        else:
            return render_template('acceso.html', aviso="Verifique su nombre de usuario o contraseña.")
        
#Enlaces para las otras páginas referencias, nosotros, presentación, etc.        
@app.route('/referencias')
def refe():
   return render_template('referencias.html')

@app.route('/nosotros')
def nosot():
   return render_template('nosotros.html')

@app.route('/contacto', methods = ['GET'])
def contac_form():
   return render_template('contacto.html')

#Página de contacto.
@app.route('/contacto', methods = ['POST'])
def contac_rta():
    try:
        if request.method == 'POST':
            #Datos del correo eléctronico            
            Nombre       = request.form['nombre']
            Correo       = request.form['correo_electronico']
            Mensaje_HTML = request.form['mensaje_usuario']
            # Crear el objeto mensaje
            mensaje = MIMEMultipart()             
            mensaje['de']     = 'agropru1@gmail.com'       #Correo de prueba para enviar algo desde la página
            mensaje['para']   = 'hahernandez@agrosavia.co' #Correo funcionario a cargo            
            #Cuerpo del mensaje
            msn = ('Este mensaje fue enviado por: '+Nombre+'\n'
                  +'Responder al correo electronico: '+Correo+'\n'
                  +'Contenido: '+Mensaje_HTML)
            mensaje.attach(MIMEText(msn, 'plain'))
            # Adjuntar el archivo dado por el usuario
            # Estructura para adjuntar un archivo usando flask y HTML desde la raiz del directorio
            if(request.files['adjunto'].filename!=''):
                archivo = request.files['adjunto']
                nombre_archivo_pdf=os.path.join(uploads_dir, secure_filename(archivo.filename))
                archivo.save(nombre_archivo_pdf)            
                archivo_pdf = MIMEApplication(open(nombre_archivo_pdf,"rb").read())
                archivo_pdf.add_header('Content-Disposition', 'attachment', filename=nombre_archivo_pdf)
                mensaje.attach(archivo_pdf) 
                os.remove(nombre_archivo_pdf)
            # Datos de acceso a la cuenta de usuario
            usuario   ='agropru1'
            contrasena='Agrosavia123'          
            #Interfaz de conexión con el servidor de gmail
            servidor = smtplib.SMTP('smtp.gmail.com:587')
            servidor.starttls()
            servidor.login(usuario, contrasena)
            servidor.sendmail(mensaje['de'], mensaje['para'], mensaje.as_string())
            servidor.quit()  
            return render_template('respuesta.html',rta="MENSAJE ENVIADO CON EXITO.")
    except:
        return render_template('respuesta.html',rta="ERROR AL ENVIAR EL MENSAJE (INTENTE NUEVAMENTE).")

#Función principal    
if __name__ == '__main__':
    app.run()