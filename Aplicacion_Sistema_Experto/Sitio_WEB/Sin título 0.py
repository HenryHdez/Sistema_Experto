# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 16:27:12 2020

@author: hahernandez
"""
import time

def Fondo(canvas, Hoja):
    from reportlab.lib import utils
    from reportlab.lib.pagesizes import letter
    #Dibujar logo y membrete de AGROSAVIA
    
    canvas.drawImage('static/Iconos/Agrosavia.jpg', 240, 720, width=150, height=40)
    canvas.drawImage('static/Iconos/Membrete.png' , 0, 0, width=650, height=15)
    canvas.drawImage('static/Iconos/Membrete2.png', 0, 650, width=150, height=150)   
    canvas.setLineWidth(.3)
    canvas.setFont('Helvetica-Bold', 20)
    if(Hoja==1):
        canvas.drawString(265,700,"INFORME:")
        canvas.drawString(155,678,"--------DISEÑO PRELIMINAR--------")
        canvas.line(0,670,680,670)
        canvas.line(0,665,680,665)
        #canvas.setFont('Helvetica-Bold', 14)
        #canvas.drawString(200,650,'--->>>DATOS DEL USUARIO<<<---')
    tiempo = time.asctime(time.localtime(time.time()))
    canvas.setFont('Helvetica-Bold', 7)
    canvas.drawString(520,5,str(tiempo))
    canvas.drawString(10,5,"Hoja: "+str(Hoja))
    return canvas

def Generar_portada():
    #Espacio de trabajo disponible desde 20 hasta 650
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    #Portada
    canvas = canvas.Canvas("A_portada.pdf", pagesize=letter)
    Fondo(canvas,"--")
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
    canvas = canvas.Canvas("B_portada.pdf", pagesize=letter)
    Fondo(canvas,"--")
    canvas.drawImage('static/Iconos/Fondo_otros.png', 50, 220, width=500, height=350)
    canvas.setFont('Helvetica-Bold', 30)
    canvas.drawString(20,450,'                         SECCIÓN 1:     ') 
    canvas.drawString(20,415,'              DATOS DEL USUARIO E   ') 
    canvas.drawString(20,380,'          INFORMACIÓN FINANCIERA  ') 
    canvas.drawString(20,345,'                   DE LA HORNILLA  ')
    canvas.showPage() #Salto de página    
    canvas.save()
    #Sección 2
    from reportlab.pdfgen import canvas
    canvas = canvas.Canvas("C_portada.pdf", pagesize=letter)
    Fondo(canvas,"--")
    canvas.drawImage('static/Iconos/Fondo_otros.png', 50, 220, width=500, height=350)
    canvas.setFont('Helvetica-Bold', 30)
    canvas.drawString(20,390,'                         SECCIÓN 2:     ') 
    canvas.drawString(20,355,'                PLANOS MECÁNICOS   ') 
    canvas.showPage() #Salto de página    
    canvas.save()
    #Sección 3
    from reportlab.pdfgen import canvas
    canvas = canvas.Canvas("D_portada.pdf", pagesize=letter)
    Fondo(canvas,"--")
    canvas.drawImage('static/Iconos/Fondo_otros.png', 50, 220, width=500, height=350)
    canvas.setFont('Helvetica-Bold', 30)
    canvas.drawString(20,390,'                         SECCIÓN 3:     ') 
    canvas.drawString(20,355,'  INFORMACIÓN TÉCNICA DETALLADA   ') 
    canvas.showPage() #Salto de página    
    canvas.save()
    
Generar_portada()