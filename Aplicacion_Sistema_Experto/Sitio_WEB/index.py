from flask import Flask, redirect, url_for, request, render_template
import json, pandas as pd
app = Flask(__name__)

@app.route('/')
def index():
   return render_template('principal.html')

@app.route('/usuario')
def usua():
    df = pd.read_json("Colombia.json")
    #print(df.departamento)
    #print(df.ciudades)
    return render_template('usuario.html', departamentos=df.departamento, provincia=df.ciudades)      

@app.route('/informe', methods = ['POST','GET'])
def infor():
   if request.method == 'POST':
      result = request.form
      print(result)
      return render_template('informe.html', result = result)    

@app.route('/nosotros')
def nosot():
   return render_template('nosotros.html')

@app.route('/contacto')
def contac():
   return render_template('contacto.html')

if __name__ == '__main__':
   app.run()