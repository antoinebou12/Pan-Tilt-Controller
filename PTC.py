import serial
from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition



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


class Controller(Screen):
    def do_move(self, panText, tiltText):
        app = App.get_running_app()
        app.pan = panText
        app.tilt = tiltText
        panInput = str('pp' + panText)
        tiltInput = str('tp' + tiltText)
        print panInput
        print tiltInput
        print  panText
        print tiltText
        ser.write(panInput + '\r\n')
        ser.write(tiltInput + '\r\n')

    def do_reset(self, panText, tiltText):
        app = App.get_running_app()
        app.pan = panText
        app.tilt = tiltText
        print  panText
        print tiltText
        ser.write('pp0' + '\r\n')
        ser.write('tp0' + '\r\n')

class PTC(App):
    pan = StringProperty(None)
    tilt = StringProperty(None)
    def build(self):
        manager = ScreenManager()
        manager.add_widget(Controller(name='tilt'))
        manager.add_widget(Controller(name='pan'))
        return manager
if __name__ == '__main__':
    PTC().run()



