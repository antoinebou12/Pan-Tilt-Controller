import serial
import time

global ser
ser = serial.Serial('COM3', 9600, timeout=1)
ser.xonxoff = True
ser.isOpen()
ser.write('pp0' + '\r\n')
ser.write('tp0' + '\r\n')
ser.write('pxu1500' + '\r\n')
ser.write('pnu-1000' + '\r\n')
ser.write('tn-900' + '\r\n')
ser.write('tx900' + '\r\n')


ser.isOpen()

print 'Enter your commands below.\r\n'

input=1
while 1 :
    input = raw_input("")
    if input == 'exit':
        ser.close()
        exit()
    else:
        ser.write(input + '\r\n')
        out = ''
        time.sleep(1)
        while ser.inWaiting() > 0:
            out += ser.read(1)

        if out != '':
            print ">>" + out


