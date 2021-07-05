#flask o django son frameworks o bibliotecas. vamos a usar FLASK
#la carpeta template va a tener todos los archivos html las vistas, lo que el usuario va a ver


from flask import Flask, render_template, request, redirect, url_for, flash   #estamos llamando al framework
from flask_mysqldb import MySQL

#redirect-> redirecciona a otra ruta
#url_for-> darle una url y redireccionar a donde querramos
#flash-> permite mandar mensajes entre vistas

app = Flask (__name__) #asi lo inicializamos, este es el archivo principal. la variable NAME te la brinda python. este archivo arranca la app
#lo guardamos en una variable, con ella vamos a crear las rutas del servidor, para crear las url

#para conectarnos a la base de datos:
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'contactos'

mysql = MySQL(app) 


#iniciar una sesion: datos que guarda la app de servidor para luego volver a utilizarlos
app.secret_key = "mysecretkey"

#crear una ruta. @app.route() es un decordador y el metodo ROUTE
#ROUTE: dice que podemos pasarle un nombre para poder crear una url. seria lo primero que aparece cuando alguien entra a la pagina

@app.route('/') #la pagina principal 
def index():  #tiene que retornar algo al navegador
    cur = mysql.connection.cursor()
    cur.execute('SELECT contacts.id, contacts.fullname, contacts.phone, contacts.email FROM  contacts') #la consulta. quiero obtener los datos dentro de la tabla contacts 
    data = cur.fetchall()  #ejecutar y obtener los datos
    #si imprimis, ves que en DATA queda una tupla con toda la tabla. print (data)
    return  render_template('index.html', contacts = data) #le pasas los datos al html asi.




@app.route('/add_contact' , methods=['POST']) #recibe los datos de la ruta principal
def add_contact():
    if request.method == 'POST': 
        fullname = request.form['fullname'] #Maneja los datos recibidos
        phone = request.form['phone']
        email = request.form['email']
        
        cur = mysql.connection.cursor()  #permite ejecutar las consultas de sql. obtenes la conexion
        cur.execute('INSERT INTO contacts (fullname, phone, email)  VALUES (%s, %s, %s)', (fullname, phone, email) )  #CONTACTS es el nombre de la tabla. en una tupla mando los valores, en orden. ya guarde los datos
        mysql.connection.commit() #arriba escribis la consulta, aca la ejecutamos.
        
        flash('Contact Added Successfully') #para mostrar el texto hay que hacer una comprobacion en nuestra vista
        #queremos que cuando termine de ingresar un contacto, redireccione al inicio   
        return redirect(url_for('index'))




@app.route('/edit/<id>') #hay que crear otro formulario que reciba los datos, y desde ese formulario cambiarlos y mandarlos a otra ruta
def get_contact(id):
    cur = mysql.connection.cursor()

    cur.execute('SELECT contacts.id, contacts.fullname, contacts.phone, contacts.email FROM contacts WHERE contacts.id = %s', (id)) #va a seleccionar el contacto con el mismo ID que le estas pasando
    data = cur.fetchall()
    
    #le pasamos como parametro la variable contact que tiene una lista, con los datos del contacto que el usuario selecciono para editar.    #print(data[0])

    return render_template('editcontact.html', contact = data[0])



@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']

        cur = mysql.connection.cursor()
        cur.execute("""UPDATE contacts SET fullname =  %s, email = %s, phone = % WHERE id = %s """,(fullname, email, phone, (id)) )
        mysql.connection.commit()
        flash ("Contact Updated Successfully!")
        return redirect(url_for('index'))




@app.route('/delete/<string:id>') #un parametro recibe, que es el ID
def delete_contact(id):
    #hay que mandarle el id a una consulta de sql para que elimine el dato
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash("Contact Removed Successfully")
    return redirect(url_for('index'))



if __name__ == '__main__':  #para validar si estamos en el archivo principal
    app.run(port = 3000, debug = True)  #para que cada vez que hagamos algun cambio, se cambie solo
    #app.run()  #este metodo permite ejecutar nuestra aplicacion  .  si lo hacemos de esta manera, a cada cambio que hacemos en el codigo tenemos que actualizar desde la consola.


