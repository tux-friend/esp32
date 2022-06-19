import socket
from machine import Pin, SoftI2C
from bme280_float import BME280    #Nötige Module und Funktionien laden

i2c=SoftI2C(scl=Pin(22),sda=Pin(21),freq=10000) #Definieren des I2C-Kanals für den BME280
bme=BME280(i2c=i2c)                             #I2C zum BME280 zuordnen

#Webserver starten
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1] 
s = socket.socket()
s.bind(addr)
s.listen(1)

#HTML-Code für die Webseite mit den Messdaten als Tabelle
html = """<!DOCTYPE html>                       
<html>
<head> 
<style type="text/css">
html {
    margin-left: 1em;
}
body {
    font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
}
table {
    border-collapse: collapse;
}
td, th {
    border: 1px solid #ddd;
    padding: 8px;
}
tr:nth-child(even){background-color: #f2f2f2;}
th {
    padding-top: 12px;
    padding-bottom: 12px;
    text-align: left;
    background-color: #4d94ff;
    color: white;
}
td {
    text-align: center;
}
</style>
<meta http-equiv="refresh" content="10">
<title>IoT Sensor</title> 
</head>
<body>
<h3>Messwerte des BME280</h3>
<p> IoT-Ger&auml;t </p>
<table> 
 <tr>
   <th>Temperatur</th>
   <th>Druck</th>
   <th>Feuchtigkeit</th>
  </tr>
  %s
</table>
</body>
<br>
xx. Juni 2022
</html>
"""
print('listening on', addr)

#Warten auf einen Aufruf des Webservers durch einen Klient (z.B. Smartphone)
#Anschliessend: BME280-Messwerte in Tabelle schreiben
while True:
    cl, addr = s.accept()
    print('Klient verbunden von', addr)
    cl_file = cl.makefile('rwb', 0)
    a = bme.values[0]
    b = bme.values[1]
    c = bme.values[2]
    while True:
        line = cl_file.readline()
        if not line or line == b'\r\n':
            break
    row = ['<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % (a, b, c)]
    response = html % '\n'.join(row)
    cl.send(response)
    cl.close()
