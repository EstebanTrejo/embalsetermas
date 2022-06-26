
from flask import Flask, render_template, request,redirect, url_for,flash
from flask_mysqldb import MySQL

from config import config
app = Flask(__name__)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_PORT']= 3306
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='embalseTermasRioHondo'

mysql = MySQL(app)

app.secret_key = "mysecretkey"
#login
@app.route('/')
def index():

    return render_template('index.html')

#zona de administracion de mediciones
@app.route('/adminmedicion')
def adminmedicion():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM mediciones')
    datos = cur.fetchall()
    cur.close()
    return render_template('adminmedicion.html', mediciones=datos)

@app.route('/add_parametro', methods=['POST'])
def add_parametro():
    if request.method == 'POST':
        ph = request.form['Ph']
        Temperatura = request.form['Temperatura']
        turviedad = request.form['Turviedad']
        conductividad = request.form['Conductividad']
        oxigenoDisuelto = request.form['OxigenoDisuelto']
        PotencialRedox = request.form['PotencialRedox']
        SolidosDisueltos = request.form['SolidosDisueltos']
        Dqo = request.form['DQO']
        Na = request.form['NA']
        k = request.form['K']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO Mediciones(ph,Temperatura, turviedad,conductividad,oxigenoDisuelto,PotencialRedox, SolidosDisueltos,DQO,NA,k)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
        (ph,Temperatura, turviedad,conductividad,oxigenoDisuelto,PotencialRedox, SolidosDisueltos,Dqo,Na,k) )
        mysql.connection.commit()
        flash('Datos Guardados con Exito')
        return redirect(url_for('adminmedicion'))


@app.route('/editarmed/<id>', methods = ['POST', 'GET'])
def get_medicion(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM mediciones WHERE id_medicion = %s', (id))
    dato = cur.fetchall()
    cur.close()
    print(dato[0])
    return render_template('editar_medicion.html', medicion = dato[0])



@app.route('/updatemed/<id>', methods=['POST'])
def updatemed(id):
    if request.method == 'POST':
        ph = request.form['Ph']
        Temperatura = request.form['Temperatura']
        turviedad = request.form['Turviedad']
        conductividad = request.form['Conductividad']
        oxigenoDisuelto = request.form['OxigenoDisuelto']
        PotencialRedox = request.form['PotencialRedox']
        SolidosDisueltos = request.form['SolidosDisueltos']
        Dqo = request.form['DQO']
        Na = request.form['NA']
        k = request.form['K']
        cur = mysql.connection.cursor()
        cur.execute("""UPDATE mediciones 
        SET Ph=%s, Temperatura=%s, Turviedad=%s, Conductividad=%s, OxigenoDisuelto=%s, PotencialRedox=%s, 
        SolidosDisueltos=%s, DQO=%s, NA=%s, K=%s 
        WHERE id_medicion = %s""", 
        (ph, Temperatura, turviedad, conductividad,oxigenoDisuelto,PotencialRedox,SolidosDisueltos,Dqo,Na,k,id))
        flash('Datos modificados con exito')
        mysql.connection.commit()
        return redirect(url_for('adminmedicion'))




@app.route('/eliminarmed/<string:id>', methods = ['POST','GET'])
def eliminarmed(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM mediciones WHERE id_medicion = {0}'.format(id))
    mysql.connection.commit()
    flash('Se elimino correctamente')
    return redirect(url_for('adminmedicion'))


#zona de empleados
#pantalla principal de la zona de administracion de empleados

#mostrar todos los empleados
@app.route('/adminempleado')
def adminempleado():    
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM empleados')
    datos = cur.fetchall()
    cur.close()
    return render_template('adminempleado.html', empleados=datos)

#logica del formulario para insertar en la base de datos
@app.route('/add_empleado', methods=['POST'])
def add_empleado():
    if request.method == 'POST':
        dni = request.form['dni']
        nombre = request.form['nombre']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO empleados(DNI,Nombre) VALUES (%s,%s)',
        (dni,nombre))
        mysql.connection.commit()
        flash('Empleado Guardado con Exito')
        return redirect(url_for('adminempleado'))
    
#modificar un empleado
#prellenar los datos con el id
@app.route('/editaremp/<id>', methods = ['POST', 'GET'])
def get_empleado(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM empleados WHERE id_empleado = %s', (id))
    dato = cur.fetchall()
    cur.close()
    print(dato[0])
    return render_template('editar_empleado.html', empleado = dato[0])

#hacer el update a la db con los campos del formulario

@app.route('/updateemp/<id>', methods=['POST'])
def update_empleado(id):
    if request.method == 'POST':
        dni = request.form['dni']
        nombre = request.form['nombre']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE empleados SET dni=%s, nombre=%s WHERE id_empleado = %s",(dni,nombre,id))
        flash('empleado modificado con exito')
        mysql.connection.commit()
        return redirect(url_for('adminempleado'))
    
#eliminar un empleado
@app.route('/eliminaremp/<string:id>', methods = ['POST','GET'])
def eliminar_empleado(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM empleados WHERE id_empleado = {0}'.format(id))
    mysql.connection.commit()
    flash('Se elimino el empleado correctamente')
    return redirect(url_for('adminempleado'))

#ver si es un empleado o no

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        dni = request.form['dni']
        nombre = request.form['nombre']
        cur = mysql.connection.cursor()
        cur.execute('SELECt * FROM empleados WHERE dni = %s and nombre = %s',(dni,nombre))
        dato = cur.fetchone()
        
        if dato:
            return redirect(url_for('adminmedicion'))
        else:
            flash('el empleado no existe o contraseña incorrecta')
            return redirect(url_for('index'))


#ver si es un admin o no

@app.route('/iraladmin', methods=['POST'])
def iraladmin():
    if request.method == 'POST':
        dni = request.form['dni']
        nombre = request.form['nombre']
        cur = mysql.connection.cursor()
        cur.execute('SELECt * FROM administradores WHERE dni = %s and nombre = %s',(dni,nombre))
        dato = cur.fetchone()
        
        if dato:
            return redirect(url_for('adminempleado'))
        else:
            flash('Admin no permitido')
            return redirect(url_for('index'))

# aqui termina la zona de empleados owo






if __name__ == "__main__":
        app.config.from_object(config['desarrollo'])
        app.run(port=3000, debug=True)



