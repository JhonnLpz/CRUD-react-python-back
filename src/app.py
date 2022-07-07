from flask import Flask, jsonify
from config import config
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin

app = Flask(__name__)

CORS(app)

conexion = MySQL(app)

@cross_origin
@app.route('/personajes',methods = ['GET'])
def listar_personajes():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT nombre, edad, raza,descripcion FROM personajes"
        cursor.execute(sql)
        datos = cursor.fetchall()
        personajes = []
        for fila in datos:
            personaje = {
                'nombre': fila[0],
                'edad': fila[1],
                'raza': fila[2],
                'descripcion':fila[3]
            }
            personajes.append(personaje)
        return jsonify({'personajes':personajes})
    except Exception as ex:
        return jsonify({'mensaje':'error'})

@app.route('/personajes/<codigo>',methods =['GET'] )
def mostrar_personaje(codigo):
    cursor = conexion.connection.cursor()
    sql = "SELECT nombre, edad, raza, descripcion FROM personajes WHERE id = `{0}`".format(id)
    cursor.execute(sql)
    cursor.fetchone()
def not_found_page(error):
    return "<h1>Pagina no encontrada</h1>"


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, not_found_page)
    app.run()
