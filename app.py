from flask import Flask, request, render_template, url_for, redirect, flash
from flask_mysqldb import MySQL

app = Flask(__name__)



app.config['MYSQL_HOST'] = 'localhost'

app.config['MYSQL_USER'] = 'root'

app.config['MYSQL_PASSWORD'] = ''

app.config['MYSQL_DB'] = 'bdMediclin'

app.secret_key= 'llave'

mysql = MySQL(app)


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/rec')
def rec():
    return render_template('vistas/recetasAdmin.html')

@app.route('/usu')
def usu():
    return render_template('vistas/usuariosAdmin.html')

@app.route('/citas')
def citas():
    return render_template('vistas/citasAdmin.html')

@app.route('/ex')
def ex():
    return render_template('vistas/expedientesAdmin.html')

if __name__ == '__main__':  
    app.run(port=3000, debug=True)