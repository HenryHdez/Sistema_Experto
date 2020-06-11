# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 11:53:34 2020

@author: hahernandez
"""


from firebase import firebase
import base64

with open("Informe.pdf", 'rb') as binary_file:
    binary_file_data = binary_file.read()
    base64_encoded_data = base64.b64encode(binary_file_data)
    base64_message = base64_encoded_data.decode('utf-8')

#base64_img_bytes = base64_message.encode('utf-8')
#with open('hola.pdf', 'wb') as file_to_save:
#    decoded_image_data = base64.decodebytes(base64_img_bytes)
#    file_to_save.write(decoded_image_data)
    
#a = open("Informe.pdf", "rb").read().encode("base64")
#print(a) 

basedatos=firebase.FirebaseApplication('https://agrosavia-f8fd5.firebaseio.com/',None)

datos={
       'Nombre':'Archivo_prueba_2',
       'Correo':'Uno@hot',
       'Telefono':'314499596',
       'Departamento':'Bogota22',
       'Ciudad':'Bogota',
       'Normal': base64_message,
       'Tecnico': base64_message
       }

resultado=basedatos.post('/agrosavia-f8fd5/Clientes',datos)

print(resultado)