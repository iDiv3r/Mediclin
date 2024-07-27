from flask import Flask, request, render_template, url_for, redirect, flash, make_response,jsonify
from flask_mysqldb import MySQL
from datetime import datetime,date
from generadorRecetas import *
import json
import string
import math
import os

app = Flask(__name__)



app.config['MYSQL_HOST'] = 'localhost'

app.config['MYSQL_USER'] = 'root'

app.config['MYSQL_PASSWORD'] = ''

app.config['MYSQL_DB'] = 'dbMediclin'

app.secret_key= 'llave'

mysql = MySQL(app)

def verificarVacios(palabra):
    letras = string.ascii_letters
    numeros = string.digits
    
    numL = 0
    
    for caracter in str(palabra):
        if caracter in letras or caracter in numeros:
            numL += 1
            break
    
    if numL > 0:
        return False
    else:
        return True

def verificarUsuario():
    try:
        idA = request.cookies.get('AuthId')
        name = request.cookies.get('AuthName')
        usuario = []
        
        if idA and name:
            usuario = [idA, name]
            return usuario
        else:
            return None
        
    except:
        flash('Error')
        return redirect(url_for('index'))

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
            
            flash('SuccIni')
            
            return response
        else:
            flash('Error')
            return render_template('login.html')
    
    except Exception as e:
        print("Exception:", e)
        return redirect(url_for(index))


# index home ----------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/home')
def home():
    
    usu = verificarUsuario()
    
    if not usu:
        flash('NoVer')
        return redirect(url_for('index'))

    return render_template('vistas/home.html', usuario=usu)

@app.route('/cerrarSesion',methods=['POST'])
def cerrarSesion():
    try:
        response = make_response(redirect(url_for('index')))
        response.delete_cookie('AuthId')
        response.delete_cookie('AuthName')
        return response
        
    except Exception as e:
        print(e)

# RECEtAS ###########################################################################################################################################################################

# index Recetas ----------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/rec')
def rec():
    
    usu = verificarUsuario()
    
    if not usu:
        flash('NoVer')
        return redirect(url_for('index'))
    
    return render_template('vistas/recetasAdmin.html',usuario=usu)

# index Usuarios ----------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/usu')
def usu():
    try: 
        
        usu = verificarUsuario()
    
        if not usu:
            flash('NoVer')
            return redirect(url_for('index'))
        
        cursor = mysql.connection.cursor()
        cursor.execute('select medicos.id,medicos.RFC,medicos.nombreCompleto,medicos.cedula,medicos.correo,medicos.pass,medicos.rol,consultorios.nombre from medicos inner join consultorios on medicos.id_consultorio = consultorios.id')
        listaMedicos = cursor.fetchall()
        
        cursor = mysql.connection.cursor()
        cursor.execute('select * from consultorios')
        listaConsultorios = cursor.fetchall()
        
        return render_template('vistas/usuariosAdmin.html',medicos=listaMedicos,consultorios=listaConsultorios,usuario=usu)
    
    except Exception as e :
        listaMedicos = []
        listaConsultorios = []
        
        return render_template('vistas/usuariosAdmin.html',medicos=listaMedicos,consultorios=listaConsultorios,usuario=usu)

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
    
    datos = [Rfc,Correo,NombreC,Pass,Cedula]
    
    for campo in datos:
        x = verificarVacios(campo)
        if x is True:
            flash('Error')
            return redirect(url_for('usu'))
    
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
    
    datos = [Rfc,Correo,NombreC,Pass,Cedula]
    
    for campo in datos:
        x = verificarVacios(campo)
        if x is True:
            flash('Error')
            return redirect(url_for('usu'))
    
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

# Citas ############################################################################################################################################################

# index Citas ----------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/citas')
def citas():
    
    try:
        
        usu = verificarUsuario()
    
        if not usu:
            flash('NoVer')
            return redirect(url_for('index'))
        
        
        cursor = mysql.connection.cursor()
        cursor.execute('select * from consultorios')
        listaConsultorios = cursor.fetchall()
        
        idA = usu[0]
        
        cursor = mysql.connection.cursor()
        cursor.execute('select * from pacientes where id_medico = %s',(idA))
        listaExpedientes = cursor.fetchall()
        
        cursor = mysql.connection.cursor()
        cursor.execute('select c.id,c.fecha,c.hora,c.peso,c.altura,c.temperatura,c.bpm,c.oxigenacion,c.glucosa,c.edad,c.sintomas,c.diagnostico,c.tratamiento,c.estudios,p.nombreCompleto,co.nombre,c.nombrePDF,c.estado from citas c inner join pacientes p on p.id = c.id_paciente inner join consultorios co on co.id = c.id_consultorio where p.id_medico = %s',(idA))
        listaCitas = cursor.fetchall()
        
        return render_template('vistas/citasAdmin.html',consultorios=listaConsultorios,pacientes=listaExpedientes,citas=listaCitas,usuario=usu)
    
    except:
        return render_template('vistas/citasAdmin.html',consultorios=[],usuario=usu)



# crear Cita ------------------------------------------------------------------------------------------------------------------------------------------------

@app.route('/registrarCita', methods=['POST'])
def registrarCita():
    
    fecha = request.form['txtFecha']
    hora = request.form['txtHora']  
    peso = request.form['txtPeso']
    altura = request.form['txtAlt']
    temp = request.form['txtTemp']
    lpm = request.form['txtLpm']
    saturacion = request.form['txtSat']
    glucosa = request.form['txtGlucosa']
    edad = 0
    sintomas = request.form['txtSin']
    diagnostico = request.form['txtDiagnostico']
    tratamiento = request.form['txtInd']
    estudios = request.form['txtEstudios']
    idConsultorio = request.form['txtCon']
    idPaciente = request.form['txtPac']
    
    
    try:
        
        cursor = mysql.connection.cursor()
        cursor.execute('select fechaNacimiento from pacientes where id = %s',[idPaciente])
        
        fechaN = cursor.fetchone()
        fechaNS = str(fechaN[0])
        
        fechaS = datetime.strptime(fechaNS, "%Y-%m-%d")
        yearN = fechaS.year
        
        fechaA = date.today()
        yearT = fechaA.year   
        
        edad = math.floor(yearT - yearN)
        
        horaF = datetime.strptime(hora, '%H:%M')
        horaN = horaF.strftime('%H-%M')
        nombreArchivo = "Receta" + idPaciente + "-" + fecha + "-" + horaN + ".pdf"

        cursor = mysql.connection.cursor()
        cursor.execute('select nombre from consultorios where id = %s',[idConsultorio])
        nombreConsultorio = cursor.fetchone()
        
        cursor = mysql.connection.cursor()
        cursor.execute('select nombreCompleto from pacientes where id = %s',[idPaciente])
        nombrePaciente = cursor.fetchone()
        
        
        datos = [fecha,hora,nombreConsultorio[0],nombrePaciente[0],altura,peso,edad,temp,saturacion,glucosa,lpm,sintomas,diagnostico,tratamiento,estudios]
        
        for campo in datos:
            x = verificarVacios(campo)
            if x is True:
                print('Campos Vacios')
                flash('Error')
                return redirect(url_for('citas'))
        
        genPDF = GeneradorRecetas()
        
        genPDF.add_page()
        genPDF.chapter_body(datos)
        
        rutaPDF = os.path.join("static/PDFs/", nombreArchivo)
        
        genPDF.output(rutaPDF)
        
        cursor = mysql.connection.cursor()
        cursor.execute('insert into citas(fecha,hora,peso,altura,temperatura,bpm,oxigenacion,glucosa,edad,sintomas,diagnostico,tratamiento,estudios,id_consultorio,id_paciente,nombrePDF,estado) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (fecha,hora,peso,altura,temp,lpm,saturacion,glucosa,edad,sintomas,diagnostico,tratamiento,estudios,idConsultorio,idPaciente,nombreArchivo,1))
        mysql.connection.commit()
        
        flash('Success')
        return redirect(url_for('citas'))
        
    except Exception as e:
        print(e)
        flash('Error')
        return redirect(url_for('citas'))
        

# Actualizar Estado Cita -------------------------------------------------------------------------------------------------------------------------------------
@app.route('/actualizarEstadoCita', methods=['POST'])
def actualizarEstadoCita():
    
    estado = request.form['txtEstado']
    idCita = request.form['txtIdCita']
    
    try:
        
        cursor = mysql.connection.cursor()
        cursor.execute('update citas set estado = %s where id = %s',(estado,idCita))
        mysql.connection.commit()
        
        flash('SuccessE')
        return redirect(url_for('citas'))
        
    except Exception as e:  
        print(e)
        flash('ErrorE')
        return redirect(url_for('citas'))
    
# EXPEDIENTES ################################################################################################################################################################################
    
# index Expedientes ----------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/ex')
def ex():
    try:
        
        usu = verificarUsuario()
    
        if not usu:
            flash('NoVer')
            return redirect(url_for('index'))
        
        idA = usu[0]
        name = usu[1]
        
        cursor = mysql.connection.cursor()
        cursor.execute('select * from pacientes where id_medico = %s',(idA))
        listaExpedientes = cursor.fetchall()
        
        
        
        return render_template('vistas/expedientesAdmin.html', usuario=usu,expedientes=listaExpedientes)
        
    
    except Exception as e :
        
        listaExpedientes = []
        
        return render_template('vistas/expedientesAdmin.html',expedientes=listaExpedientes,usuario=usu)

# crear Expedientes ----------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/crearPaciente',methods=['POST'])
def crearPaciente():
    IdMedico = request.form['txtIdMedico']
    Nombre = request.form['txtNombre']
    FechaN = request.form['txtFechaN']
    Alergias = request.form['txtAlergias']
    Enfermedades = request.form['txtEnf']
    Antecedentes = request.form['txtAnt']
    FechaC = datetime.now()
    
    
    x = verificarVacios(Nombre)
    if x is True:
        flash('Error')
        return redirect(url_for('ex'))
    
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
    

    x = verificarVacios(Nombre)
    if x is True:
        flash('EditE')
        return redirect(url_for('ex'))
    
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