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


@app.route('/test')
def test():
    return render_template('modales/EditYElimUsuarios.html')

if __name__ == '__main__':
    app.run(port=3000, debug=True)