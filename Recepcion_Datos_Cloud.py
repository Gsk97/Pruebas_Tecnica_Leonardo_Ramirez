"""
Script diseñado para la recepcion y respuesta de datos en un sistema Cloud

Concideraciones : 
El equipo que ejecute este script debe tener instalado flask,ejecute el siguiente comando para ello 
pip install Flask : https://pypi.org/project/Flask/

Documentacion investigada
https://chozinthet20602.medium.com/creating-http-request-and-response-with-python-flask-7190cc2b924a
https://flask.palletsprojects.com/en/3.0.x/api/

"""
# Importacion desde flask para manejar solicitudes HTTP
from flask import Flask ,request ,jsonify

from cryptography.fernet import Fernet
import json

# Clave secreta utilizada 
key_secret = b'1234'

#Se inicia la aplicacion con el nombre Datos_cloud
app = Flask('Datos_Cloud')



# Se define una funcion para descifrar el mensaje obtenido por el dispositivo IoT
def descifrado(mensaje):

    try:

        cipher_suite = Fernet(key_secret)
        mensaje_des= cipher_suite.decrypt(mensaje)
        return mensaje_des 
    except Exception as e :
        print(f"Error para descifrar el mensaje : {str(e)}")
        return None



@app.route("/", methods=['POST'])
def recepcion_datos():
    print(request.method)
    # Datos en bytes 
    datos_cifrados = request.get_data()

    #dato = request.get_json()
    descifrado = descifrado(datos_cifrados)

    if descifrado :
        print(f"Datos recibidos :{descifrado}")
        datos = json.loads(descifrado)
        res ={
            "Estado":"success",
            "mensaje":"data recevied",
            "data": datos
        }
        #Retorna un codigo 200(ok) con los datos recibidos
        return jsonify(res), 200
    else :
        # Si no se recien datos ,se responde con el codigo de error 400 (Bad Request)
        return jsonify({"Error en los datos recibidos"}), 400
    
    

if __name__ == "__main__":

    #Direccion IP propuesta para las pruebas
    app.run(host='192.168.1.100', port=4000)
