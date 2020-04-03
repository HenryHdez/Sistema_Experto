from flask import Flask, request, render_template
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import smtplib
import os
from werkzeug import secure_filename

app = Flask(__name__)
uploads_dir = os.path.join(app.instance_path, 'uploads')
try:
    os.makedirs(uploads_dir, True)
    print('Directorio Creado')
except OSError: 
    print('Directorio existente')

@app.route('/')
def index():
   return render_template('principal.html')

@app.route('/usuario')
def usua():
    global df
    df = pd.read_json("Colombia.json")
    #print(df.departamento)
    #print(df.ciudades)
    return render_template('usuario.html', departamentos=df.departamento, provincia=df.ciudades)      

@app.route('/informe', methods = ['POST','GET'])
def infor():
    global df
    if request.method == 'POST':
        result = request.form
        Dept=result.get('Departamento')
        D_aux=df.departamento
        D_aux=D_aux.tolist()
        amsnm=df.altura
        amsnm=amsnm.tolist()
        H2O=df.aguasubterranea
        H2O=H2O.tolist()
        altura_media=amsnm[D_aux.index(Dept)]
        NivelFre=H2O[D_aux.index(Dept)]
        return render_template('informe.html', result = result, value=Dept, altu=altura_media, Freatico=NivelFre)    

@app.route('/referencias')
def refe():
   return render_template('referencias.html')

@app.route('/nosotros')
def nosot():
   return render_template('nosotros.html')

@app.route('/contacto', methods = ['GET'])
def contac_form():
   return render_template('contacto.html')

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
             
            mensaje['de']     = 'agropru1@gmail.com'       #Correo de prueba
            mensaje['para']   = 'hahernandez@agrosavia.co' #Correo funcionario
            
            #Construcción del mensaje
            msn = ('Este mensaje fue enviado por: '+Nombre+'\n'
                  +'Responder al correo electronico: '+Correo+'\n'
                  +'Contenido: '+Mensaje_HTML)
            
            mensaje.attach(MIMEText(msn, 'plain'))
            
            #Adjuntar el archivo .pdf
            # Estructura para adjuntar un archivo usando flask y HTML desde la raiz del directorio
            if(request.files['adjunto'].filename!=''):
                archivo = request.files['adjunto']
                nombre_archivo_pdf=os.path.join(uploads_dir, secure_filename(archivo.filename))
                archivo.save(nombre_archivo_pdf)            
                archivo_pdf = MIMEApplication(open(nombre_archivo_pdf,"rb").read())
                archivo_pdf.add_header('Content-Disposition', 'attachment', filename=nombre_archivo_pdf)
                mensaje.attach(archivo_pdf)            
            # parámetros fijos de la cuenta de correo
            usuario   ='agropru1'
            contrasena='Agrosavia123'
            #msg.attach(MIMEImage(file("google.jpg").read()))
            
            
            servidor = smtplib.SMTP('smtp.gmail.com:587')
            servidor.starttls()
            servidor.login(usuario, contrasena)
            servidor.sendmail(mensaje['de'], mensaje['para'], mensaje.as_string())
            servidor.quit()  
            return render_template('respuesta.html',rta="MENSAJE ENVIADO CON EXITO.")
    except:
        return render_template('respuesta.html',rta="ERROR AL ENVIAR EL MENSAJE (INTENTE NUEVAMENTE).")
    

if __name__ == '__main__':
   app.run()