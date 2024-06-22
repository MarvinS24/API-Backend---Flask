from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from config import config

app = Flask(__name__)

conexion=MySQL(app)

@app.route('/cursos', methods=['GET'])
def listar_cursos():
    try:
        cursor= conexion.connection.cursor()
        sql="SELECT codigo, nombre, creditos FROM curso"
        cursor.execute(sql)
        datos=cursor.fetchall()
        cursos=[]
        for fila in datos:
            curso = {'codigo': fila[0], 'nombre': fila[1], 'creditos': fila[2]}
            cursos.append(curso)
        return jsonify({'cursos': cursos, 'mensaje': "Cursos listados.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})
    
    
@app.route('/cursos/<codigo>', methods=['GET'])
def leer_curso(codigo):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT codigo, nombre, creditos FROM curso WHERE codigo = '{0}'".format(codigo)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos != None:
            curso = {'codigo': datos[0], 'nombre': datos[1], 'creditos': datos[2]}
            return jsonify({'curso': curso, 'mensaje': "Curso encontrados.", 'exito': True})
        else:
            return jsonify({'mensaje': "curso no encontrado", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})


@app.route('/cursos', methods=['POST'])
def registrar_cursos():
    try:
        # print(request.json)
        cursor = conexion.connection.cursor()
        sql = """INSERT INTO curso (codigo, nombre, creditos) 
                VALUES ('{0}', '{1}', {2})""".format(request.json['codigo'],
                                                     request.json['nombre'], request.json['creditos'])
        cursor.execute(sql)
        conexion.connection.commit()  # Confirma la acción de inserción.
        return jsonify({'mensaje': "Curso resgistrado.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})


@app.route('/cursos/<codigo>', methods=['PUT'])
def actualizar_curso(codigo):
    try:
        # print(request.json)
        cursor = conexion.connection.cursor()
        sql = """UPDATE curso SET nombre = '{0}', creditos = {1} 
                WHERE codigo = '{2}'""".format(request.json['nombre'], request.json['creditos'], codigo)
        cursor.execute(sql)
        conexion.connection.commit()  # Confirma la acción de inserción.
        return jsonify({'mensaje': "Curso actualizado.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})
    

@app.route('/cursos/<codigo>', methods=['DELETE'])
def eliminar_curso(codigo):
    try:
        # print(request.json)
        cursor = conexion.connection.cursor()
        sql = "DELETE FROM curso WHERE codigo = '{0}'".format(codigo)
        cursor.execute(sql)
        conexion.connection.commit()  # Confirma la acción de inserción.
        return jsonify({'mensaje': "Curso eliminado.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})
    
        

def pagina_no_encontrada(error):
    return "<h1>La página qu eintestas buscar no existe</h1>", 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()