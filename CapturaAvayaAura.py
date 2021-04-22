import sys, re, os
import socket
import time

class Main:

    baud = 512
    rutaSalida = "CDR/"
    nombreArchivo = 'AvayaX'

    def Main(self):
        try:
            aux     = sys.argv
            host    = aux[1]
            port    = int(aux[2])
            if self.ValidateIsIp(host):
                # print (f"\n\t> Ejecutando:{aux[0]} captura por ip:{host} puerto:{port}")
                Datos   = []
                toDay   =  time.strftime("%Y-%m-%d")
                sock    = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # cereamos el soket
                server_address = (host, port)
                sock.bind(server_address) # print ('starting up on %s port %s' % server_address)
                sock.listen(1)
                while True:
                    # print ('\n\twaiting for a connection')
                    connection, client_address = sock.accept()
                    try:
                        # print ('cliente conectado : ', client_address)
                        while True:
                            tempDate = time.strftime("%Y-%m-%d")
                            if toDay != tempDate: toDay = tempDate
                            data = connection.recv(self.baud)
                            auxData =  data
                            auxData = re.sub('n\'', '', str(auxData))
                            auxData = re.sub('b\'', '', str(auxData))
                            auxData = re.sub('\\\\', '', str(auxData))
                            if data:
                                Datos.append(auxData)
                                if(len(Datos) == 5):
                                    self.EscribirArchivoActual(Datos, toDay)
                                    Datos = []
                            else:
                                break
                    finally:
                        connection.close()
        except (Exception, e):
            print ("Error en Main\n" % str(e))
            return

    def ValidateIsIp(self, ip):
        try:
            socket.inet_aton(ip)
            return True
        except socket.error:
            print (f'\n\t- Necesitamos una IP válida esto: {ip} no es una ip :(')
            False

    def EscribirArchivoActual(self, lista, toDay):
        try:
            if os.path.exists(self.rutaSalida) == False:
                print (f'\n\t- La ruta no existe:{self.rutaSalida}')
                return
            pathFile = os.path.join(self.rutaSalida, toDay + self.nombreArchivo + '.csv')
            fileWrite = open(pathFile,'a')
            # print (f"Escribiendo en archivo: {fileWrite.name}")
            for line in lista: fileWrite.write(line + "\n")
            fileWrite.close()
        except (Exception, e):
            print ("Error en EscribirArchivoActual\n" % str(e))
            return

Obj = Main()
Obj.Main()
# https://pymotw.com/2/socket/tcp.html