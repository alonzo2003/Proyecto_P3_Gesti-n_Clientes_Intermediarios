from flask import Flask, render_template, request, redirect, flash, url_for, session
from flaskext.mysql import MySQL



app=Flask(__name__) 
app.secret_key= 'correajacc'
USER = {'username': 'admin', 'password': 'admin123'}

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'sistema'
mysql.init_app(app)

from flask import session, redirect, url_for

def login_required(func):
    def wrapper(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))   # si no hay sesión, va al login
        return func(*args, **kwargs)            # si hay sesión, ejecuta la función
    wrapper.__name__ = func.__name__            # evita conflictos internos de Flask
    return wrapper



#rUTA DE LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USER['username'] and password == USER['password']:
            session['user'] = username
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials. Please try again.')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


#Ruta principal
@app.route('/')
@login_required
def index():

    sql = "SELECT * FROM `clientes`;"
    conn= mysql.connect()
    cursor= conn.cursor()
    cursor.execute(sql)

    clientes= cursor.fetchall()
    print(clientes)

    conn.commit()
    return render_template('clientes/index.html', clientes=clientes)

#Eliminar cliente
@app.route('/eliminar/<int:id>')
@login_required
def eliminar(id):

    conn= mysql.connect()
    cursor= conn.cursor()
    cursor.execute("DELETE FROM `clientes` WHERE id=%s", (id,))
    clientes= cursor.fetchall()
    conn.commit()
    return redirect('/')


#Editar cliente
@app.route('/editar/<int:id>')
@login_required
def editar(id):
    conn= mysql.connect()
    cursor= conn.cursor()
    cursor.execute("SELECT * FROM `clientes` WHERE id=%s", (id,))
    clientes= cursor.fetchall()
    print(clientes)
    conn.commit()
    return render_template('clientes/editar.html', clientes=clientes)

#Actualizar cliente
@app.route('/update', methods=['POST'])
@login_required
def update():
    _nombre=request.form['txtNombre']
    _gmail=request.form['txtGmail'] 
    _poliza=request.form['txtPoliza']
    _numero=request.form['txtNumero']
    id=request.form['txtID']
    
    
    sql = "UPDATE `clientes` SET `nombre`=%s, `gmail`=%s, `Póliza`=%s, `numero`=%s WHERE id=%s;"
    datos=(_nombre,_gmail,_poliza,_numero,id)

    conn= mysql.connect()
    cursor= conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    return redirect('/')

#Crear cliente
@app.route('/crear')
@login_required
def crear():
    return render_template('clientes/crear.html')

@app.route('/store', methods=['POST'])
@login_required
def store():

    _nombre=request.form['txtNombre']
    _gmail=request.form['txtGmail'] 
    _poliza=request.form['txtPoliza']
    _numero=request.form['txtNumero']

    if _nombre=='' or _gmail=='' or _poliza=='' or _numero=='':
        flash('Todos los campos son obligatorios, por favor llenelos')
        return redirect(url_for('crear'))

    
    sql = "INSERT INTO `clientes` (`id`, `nombre`, `gmail`, `Póliza`, `numero`) VALUES (NULL, %s, %s, %s, %s);"

    datos=(_nombre,_gmail,_poliza,_numero)


    conn= mysql.connect()
    cursor= conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)