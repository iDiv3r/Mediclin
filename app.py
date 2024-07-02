from flask import Flask, request, render_template, url_for, redirect, flash, make_response,jsonify
from flask_mysqldb import MySQL
import datetime
import json

app = Flask(__name__)



app.config['MYSQL_HOST'] = 'localhost'

app.config['MYSQL_USER'] = 'root'

app.config['MYSQL_PASSWORD'] = ''

app.config['MYSQL_DB'] = 'dbMediclin'

app.secret_key= 'llave'

mysql = MySQL(app)

# index Login ----------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/')
def index():
    return render_template('login.html')


# verificar usuario Login ----------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/login', methods=['POST'])
def login():
    rfc = request.form['txtRFC']
    passw = request.form['txtPass']
    
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('select id,nombreCompleto from medicos where RFC = %s and pass = %s', (rfc, passw))
        resultado = cursor.fetchone()
        
        if resultado:
            response = make_response(redirect(url_for('home')))
            response.set_cookie('AuthId', str(resultado[0]))
            response.set_cookie('AuthName', resultado[1])
            
            return response
        else:
            return render_template('login.html', error="Usuario o contraseña incorrectos")
    
    except Exception as e:
        print("Exception:", e)
        return render_template('login.html', error="Ocurrió un error")


# index home ----------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/home')
def home():
    try:
        idA = request.cookies.get('AuthId')
        name = request.cookies.get('AuthName')
        
        if idA or name:
            return render_template('vistas/home.html', usuario=[idA, name])
        else:
            return redirect(url_for('index'))
    
    except Exception as e:
        print("Exception:", e)
        return render_template('login.html', error="Ocurrió un error")


# index Recetas ----------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/rec')
def rec():
    return render_template('vistas/recetasAdmin.html')

# index Usuarios ----------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/usu')
def usu():
    try: 
        cursor = mysql.connection.cursor()
        cursor.execute('select medicos.id,medicos.RFC,medicos.nombreCompleto,medicos.cedula,medicos.correo,medicos.pass,medicos.rol,consultorios.nombre from medicos inner join consultorios on medicos.id_consultorio = consultorios.id')
        listaMedicos = cursor.fetchall()
        
        cursor = mysql.connection.cursor()
        cursor.execute('select * from consultorios')
        listaConsultorios = cursor.fetchall()
        
        return render_template('vistas/usuariosAdmin.html',medicos=listaMedicos,consultorios=listaConsultorios)
    
    except Exception as e :
        listaMedicos = []
        listaConsultorios = []
        
        return render_template('vistas/usuariosAdmin.html',medicos=listaMedicos,consultorios=listaConsultorios)

# crear Usuarios ----------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/crearUsuario',methods=['POST'])
def crearUsuario():
    
    Rfc = request.form['txtRFC']
    Correo = request.form['txtCorreo']
    NombreC = request.form['txtNombreC']
    Pass = request.form['txtPass']
    Cedula = request.form['txtCedula']
    Consultorio = request.form['txtConsultorio']
    Rol = request.form['txtRol']
    
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('insert into medicos(RFC,nombreCompleto,cedula,correo,pass,rol,id_consultorio ) values (%s,%s,%s,%s,%s,%s,%s)', (Rfc,NombreC,Cedula,Correo,Pass,Rol,Consultorio))
        mysql.connection.commit()

        flash('Success')
        return redirect(url_for('usu'))
        
    except:
        flash('Error')
        return redirect(url_for('usu'))

# editar Usuarios ----------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/editarUsuario',methods=['POST'])
def editarUsuario():
    
    IdMedico = request.form['txtIdMedico']
    Rfc = request.form['txtRFC']
    Correo = request.form['txtCorreo']
    NombreC = request.form['txtNombreC']
    Pass = request.form['txtPass']
    Cedula = request.form['txtCedula']
    Consultorio = request.form['txtConsultorio']
    Rol = request.form['txtRol']
    
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('update medicos set RFC = %s , nombreCompleto = %s , cedula = %s , correo = %s , pass = %s , rol = %s , id_consultorio = %s where id = %s ',(Rfc,NombreC,Cedula,Correo,Pass,Rol,Consultorio,IdMedico))
        mysql.connection.commit()

        flash('EditS')
        return redirect(url_for('usu'))
        
    except:
        flash('EditE')
        return redirect(url_for('usu'))

# eliminar Usuarios ----------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/eliminarUsuario',methods=['POST'])
def eliminarUsuario():
    
    IdMedico = request.form['txtIdMedico']

    try:
        cursor = mysql.connection.cursor()
        cursor.execute('delete from medicos where id = %s ',(IdMedico))
        mysql.connection.commit()

        flash('DeleteS')
        return redirect(url_for('usu'))

    except:
        flash('DeleteE')
        return redirect(url_for('usu'))


# index Citas ----------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/citas')
def citas():
    return render_template('vistas/citasAdmin.html')

# index Expedientes ----------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/ex')
def ex():
    try: 
        idA = request.cookies.get('AuthId')
        name = request.cookies.get('AuthName')
        
        cursor = mysql.connection.cursor()
        cursor.execute('select * from pacientes where id_medico = %s',(idA))
        listaExpedientes = cursor.fetchall()
        
        
        if idA and name:
            return render_template('vistas/expedientesAdmin.html', usuario=[idA, name],expedientes=listaExpedientes)
        else:
            return redirect(url_for('index'))
    
    except Exception as e :
        
        listaExpedientes = []
        
        return render_template('vistas/expedientesAdmin.html',expedientes=listaExpedientes)

# crear Expedientes ----------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/crearPaciente',methods=['POST'])
def crearPaciente():
    IdMedico = request.form['txtIdMedico']
    Nombre = request.form['txtNombre']
    FechaN = request.form['txtFechaN']
    Alergias = request.form['txtAlergias']
    Enfermedades = request.form['txtEnf']
    Antecedentes = request.form['txtAnt']
    FechaC = datetime.datetime.now()
    
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('insert into pacientes(nombreCompleto,fechaNacimiento,antecedentes,alergias,enfermedades,fechaCreacion,id_medico) values (%s,%s,%s,%s,%s,%s,%s)', (Nombre,FechaN,Antecedentes,Alergias,Enfermedades,FechaC,IdMedico))
        mysql.connection.commit()

        flash('Success')
        return redirect(url_for('ex'))
        
    except:
        flash('Error')
        return redirect(url_for('ex'))
    
# editar Expediente ----------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/editarExpediente',methods=['POST'])
def editarExpediente():
    IdExp = request.form['txtIdExp']
    Nombre = request.form['txtNombre']
    FechaN = request.form['txtFechaN']
    Alergias = request.form['txtAlergias']
    Enfermedades = request.form['txtEnf']
    Antecedentes = request.form['txtAnt']
    
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('update pacientes set nombreCompleto = %s , fechaNacimiento = %s , antecedentes = %s , alergias = %s , enfermedades = %s where id = %s ',(Nombre,FechaN,Antecedentes,Alergias,Enfermedades,IdExp))
        mysql.connection.commit()

        flash('EditS')
        return redirect(url_for('ex'))
        
    except:
        flash('EditE')
        return redirect(url_for('ex'))
    
# eliminar Expediente ----------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/eliminarExpediente',methods=['POST'])
def eliminarExpediente():
    IdExp = request.form['txtIdExp']
    
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('delete from pacientes where id = %s ',(IdExp))
        mysql.connection.commit()

        flash('DeleteS')
        return redirect(url_for('ex'))
        
    except:
        flash('DeleteE')
        return redirect(url_for('ex'))


if __name__ == '__main__':  
    app.run(port=3000, debug=True)