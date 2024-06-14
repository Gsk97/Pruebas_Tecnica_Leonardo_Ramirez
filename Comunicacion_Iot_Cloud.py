"""
Script diseñado para el envio de datos de un dispositivo IoT a un servidor o Cloud 

***Envio de datos por medio de HTTP ***
Concideraciones :
- Tener instalado request en el dispositivo IoT
    ejecute el siguiente comando para ello 
    pip install requests : https://pypi.org/project/requests/

    El dispositivo de adquisicion de datos de variables electricas tendra un protocolo de comunicacion serial ,el cual estara 
    conectado al dispositivo IoT

"""



import serial, json, logging
from time import sleep
import requests

"""
# Modulos de cifrado de datos obtenidos
# https://pypi.org/project/pycrypto/

"""
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes 
from crytography.fernet import Fernet
import base64

# Peticion de las tramas que se solicitaran al dispositivo de adquisicion de datos

# Tension de red	EDBB b'\:7BBED00A6\n'
# Potencia de red 	EDBC b'\:7BCED00A5\n'
# Corriente de red 	EDBD b'\:7BDED00A4\n'

# Direcciones de los diveros modulos de adquisicion,estas direcciones las proporciona el fabricante 

dic_Device ={
    'MPPT7015':b'\0300', # Modulo monofasico
    'MPPT7550':b'\A040',  # Modulo bifasico
    'MPPT15035':b'\A041', # Modulo trifasico
}


# La clase Modulo_Adquisicion define metodos para la comunicacion serial,extraccion de datos,creacion de archivos json,
# envio de datos mediante HTTP
#  
class Modulo_Adquisicion:

    def __init__(self, Pt='COM101', Bd=19200, Tout=10, address='MPPT15045',url='http://ejemplo1.com/api/value'):

        self.Reg1 = []

        self.Pt = Pt
        self.Bd = Bd
        self.Tout = Tout
        self.address = address
        self.ser = None
        self.url = url 

    # Esta funcion esta diseñada para capturar mensajes durante la ejecucion del programa ,se utilizan debug(),info(),error()
    def startlogging(self, status = False):
        if status:
            format = "%(asctime)s: %(message)s"
            logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
            logging.getLogger().setLevel(logging.DEBUG)
        else:
            format = "%(asctime)s: %(message)s"
            logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
            logging.getLogger().setLevel(logging.INFO)

    # Funcion que realiza la conexion serial al dispositivo de adquisicion de datos 
    def start_serial_connection(self):
        try:
            self.ser = serial.Serial(port=self.Pt, baudrate=self.Bd, timeout=self.Tout)
            logging.debug("Open serial port")

            if self.ser.is_open:
                return True
            else:
                return False

        except Exception as e:
            logging.error(e)
            return False
    # Funcion que realiza el cierr de la conexion serial al dispositivo de adquisicion de datos 
    def close_serial(self):
        self.ser.close()
        logging.debug("Serial port closed")

    # Funcion encargada de realizar las peticiones de variables electricas el dispositivo de adquisicion de datos
    def Secuencia_Extraccion_Datos(self):  
        try:

            # Tension de red EDBB
            add=dic_Device[self.address]
            fram =add + b'\:7BBED00A6\n' #variable que concatena la direccion y el registro
            self.ser.write(fram) #envio por serial de (fram)
            res=self.ser.readline() #recepcion de respuesta
            response=res[2:6] #rebanada que se compara con un byte especifico
            if response == b'BBED': # si se cumple la condicion entra al ciclo
                value=res # (value) toma la respuesta obtenida anteriormente
                v=value[8:-3] # se rebana la informacion para obtener el valor del registro pedido anteriormente 
                a = int(v[2:4:] + v[:2], 16)
                #print("VPV",a)
                self.Reg1.append(a)
            
            # Potencia de red	EDBC
            add=dic_Device[self.address]
            #fram=b'\A04D' + b'\:7BCED00A5\n'
            fram =add + b'\:7BCED00A5\n'
            self.ser.write(fram)
            res=self.ser.readline()
            response=res[2:6]
            if response == b'BCED':
                value=res
                v=value[8:-3]
                b = int(v[2:4:] + v[:2], 16)
                self.Reg1.append(b)

            # Corriente de red	EDBD
            add=dic_Device[self.address]
            #fram = b'\A04D' + b'\:7BDED00A4\n'
            fram =add + b'\:7BDED00A4\n'
            self.ser.write(fram)
            res=self.ser.readline()
            response=res[2:6]
            if response == b'BDED':
                value=res
                v=value[8:-3]
                c= int(v[2:4:] + v[:2], 16)
                self.Reg1.append(c)

        except Exception as e :
            logging.error("error en Secuencia_Extraccion_Datos. Error :" +str(e))
            return None
        
    # En base a la funcion de Secuencia_Extraccion_Datos se crea un archivo json para el posterior envio al servidor
    def Save_json(self):
        try:
            
            monitoreo={"tframe":"Variables AC",
                    "id_sede":"Prueba",
                    "payload":{
                                "Tension AC":str(self.Reg1[0]),# Tension AC
                                "Corriente AC":str(self.Reg1[2]),# Corriente AC
                                "Potencia AC":str(self.Reg1[1]),#Potencia AC
                                }}

            monitoreoJ=json.dumps(monitoreo)

            # Se genera una clave 
            key_secret = Fernet(1234)

            # se cifra el archivo json que tiene por nombre monitoreoJ
            mensaje_cripto = cipher_suite.encrypt(monitoreoJ.encode())


            self.Reg1.clear()
            
            #return monitoreoJ   
            return mensaje_cripto

        except Exception as e :
            logging.error(e)
            return None
        
    # Funcion encargada del envio al servidor de un archivo json ,creado en la funcion Save_json
    def send_http (self,data):
        try:
            # Se establece un diccionario que contiene un archivo json ,con esto se le indica al servidor que se realiza un 
            # envio de datos json
            headers = {'Content-Type': 'application/json'} 
            res= requests.post(self.url ,data=data,headers=headers)
            if res.status_code == 200 :
                logging.info("Datos enviados")
                logging.debug(f"{res.status_code}")
            else: 
                logging.error(f"Fallo al enviar datos {res.status_code}")


        except Exception as e:
                logging.error("Error en HTTP: " + str(e))

    # Funcion de arranque para la extraccion de datos 
    def run(self):
        if self.start_serial_connection():
            try:
                self.Secuencia_Extraccion_Datos()
                data = self.Save_json() # Se obtiene un mensaje cifrado ,el cual se envia en la funcio send_http
                logging.debug(data)
                self.send_http(data)
                return data
            except Exception as e:
                logging.error("Error en la ejecución: " + str(e))
            finally:
                self.close_serial()
        else:
            logging.error("No fue posible establecer una comunicación serial con el puerto " + str(self.Pt))

        

if "__main__"==__name__:
    try:
        vic = Modulo_Adquisicion(Pt='COM101', Bd=19200, Tout=10, address='MPPT15045',url='http://ejemplo1.com')
        
        vic.startlogging(True)
        vic.run()
        sleep(2)
        logging.info("------------------------------------------------------")
    except KeyboardInterrupt:
        logging.info("stop")




