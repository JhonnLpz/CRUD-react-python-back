from flask import Flask, jsonify, request
from config import config
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin

app = Flask(__name__)

CORS(app)
# CORS(app, resources={r"/personajes/*":{"origins":"http://localhost"}})

conexion = MySQL(app)


@cross_origin
@app.route('/personajes', methods=['GET'])
def listar_personajes():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM personajes"
        cursor.execute(sql)
        datos = cursor.fetchall()
        personajes = []
        for fila in datos:
            personaje = {
                'id': fila[0],
                'nombre': fila[1],
                'edad': fila[2],
                'raza': fila[3],
                'descripcion': fila[4],
                'imagen': fila[5],
                'poder': fila[6],
                'velocidad': fila[7],
                'ataque': fila[8],
            }
            personajes.append(personaje)
        return jsonify({'personajes': personajes})
    except Exception as ex:
        return jsonify({'mensaje': 'error'})


@cross_origin
@app.route('/personajes/<codigo>', methods=['GET'])
def mostrar_personaje(codigo):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM personajes WHERE id = '{0}'".format(codigo)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos != None:
            personaje = {
                'id': datos[0],
                'nombre': datos[1],
                'edad': datos[2],
                'raza': datos[3],
                'descripcion': datos[4],
                'imagen': datos[5],
                'poder': datos[6],
                'velocidad': datos[7],
                'ataque': datos[8],
            }
            return jsonify({'personajes': personaje})

        else:
            return jsonify({'mensaje': "Personaje no encontrado"})

    except Exception as ex:
        return jsonify({'mensaje': "Error"})


@cross_origin
@app.route('/insertaPj', methods=['POST'])
def agregar_personaje():
    try:
        cursor = conexion.connection.cursor()
        sql = """INSERT INTO personajes(id,nombre,edad,raza,descripcion,imagen,poder,velocidad,ataque)
        VALUES ( '{0}', '{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}')""".format(
            request.json['id'],
            request.json['nombre'],
            request.json['edad'],
            request.json['raza'],
            request.json['descripcion'],
            request.json['imagen'],
            request.json['poder'],
            request.json['velocidad'],
            request.json['ataque']
        )
        cursor.execute(sql)
        cursor.commit()
    except Exception as ex:
        return jsonify({'mensaje': "Error"})


def not_found_page(error):
    return "<h1>Pagina no encontrada</h1>"


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, not_found_page)
    app.run(port=3000)
