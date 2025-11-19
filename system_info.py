import platform
import socket


print("OS :", platform.system())


host_name = socket.gethostname()
print("Nom de la machine :", host_name)


adresse_ip = socket.gethostbyname(host_name)
print("Adresse IP :", adresse_ip)