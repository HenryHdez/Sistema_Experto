# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 11:53:34 2020

@author: hahernandez
"""


from firebase import firebase

basedatos=firebase.FirebaseApplication('https://panela-ac2ce.firebaseio.com/',None)

def Crear_archivo_base_64(ruta):
    with open(ruta, 'rb') as Archivo_codificado_1:
        Archivo_binario_1 = Archivo_codificado_1.read()
        Archivo_binario_64_1 = base64.b64encode(Archivo_binario_1)
        Mensaje_base_64_1 = Archivo_binario_64_1.decode('utf-8')
        return Mensaje_base_64_1
    
datos={
       'Nombre':"NO_BORRAR",
       'Correo':"NO_BORRAR",
       'Telefono':"NO_BORRAR",
       'Departamento':"NO_BORRAR",
       'Ciudad':"NO_BORRAR",
       'Usuario': Crear_archivo_base_64("static/Informe_WEB.pdf"),
       'Planos': Crear_archivo_base_64("static/Planos_WEB.pdf"),
       'Recinto': Crear_archivo_base_64("static/Planta_WEB.pdf"),
       'Calculos': Crear_archivo_base_64("static/Calculos_WEB.pdf")
       }

resultado=basedatos.post('https://panela-ac2ce.firebaseio.com/Clientes',datos)

print(resultado)#https://console.firebase.google.com/u/3/project/panela-ac2ce/database/panela-ac2ce/data/